from django.core.management.base import BaseCommand, CommandError
from django.db import connection

from core.models import AIModelSource, OrganizationModelConfig, ProviderModel


class Command(BaseCommand):
    help = (
        "Validate model-management tables and optionally auto-create missing tables. "
        "This prevents runtime 500 errors caused by migration/table drift."
    )

    ordered_models = [AIModelSource, ProviderModel, OrganizationModelConfig]

    def add_arguments(self, parser):
        parser.add_argument(
            "--auto-fix",
            action="store_true",
            help="Create missing tables automatically in dependency order.",
        )

    def handle(self, *args, **options):
        auto_fix = options["auto_fix"]
        missing_models = self._get_missing_models()

        if not missing_models:
            self.stdout.write(
                self.style.SUCCESS(
                    "Model-management schema check passed: all required tables exist."
                )
            )
            return

        missing_tables = [model._meta.db_table for model in missing_models]
        self.stdout.write(
            self.style.WARNING(
                "Missing model-management tables: " + ", ".join(missing_tables)
            )
        )

        if not auto_fix:
            raise CommandError(
                "Schema check failed. Re-run with --auto-fix to create missing tables."
            )

        self.stdout.write("Auto-fix enabled. Creating missing tables...")
        with connection.schema_editor() as schema_editor:
            for model in missing_models:
                table_name = model._meta.db_table
                if table_name in connection.introspection.table_names():
                    continue
                schema_editor.create_model(model)
                self.stdout.write(self.style.SUCCESS(f"Created table: {table_name}"))

        remaining_missing = self._get_missing_models()
        if remaining_missing:
            names = [model._meta.db_table for model in remaining_missing]
            raise CommandError(
                "Auto-fix incomplete. Still missing tables: " + ", ".join(names)
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Model-management schema auto-fix completed successfully."
            )
        )

    def _get_missing_models(self):
        existing_tables = set(connection.introspection.table_names())
        missing_models = []
        for model in self.ordered_models:
            if model._meta.db_table not in existing_tables:
                missing_models.append(model)
        return missing_models
