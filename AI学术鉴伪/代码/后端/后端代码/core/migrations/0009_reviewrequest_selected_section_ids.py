from django.db import migrations, models


def _column_names(schema_editor, table_name):
    with schema_editor.connection.cursor() as cursor:
        description = schema_editor.connection.introspection.get_table_description(cursor, table_name)
    return {getattr(column, 'name', column[0]) for column in description}


def add_selected_section_ids(apps, schema_editor):
    ReviewRequest = apps.get_model('core', 'ReviewRequest')
    table_name = ReviewRequest._meta.db_table
    if 'selected_section_ids' in _column_names(schema_editor, table_name):
        return

    field = models.JSONField(blank=True, default=list)
    field.set_attributes_from_name('selected_section_ids')
    field.model = ReviewRequest
    schema_editor.add_field(ReviewRequest, field)


def remove_selected_section_ids(apps, schema_editor):
    ReviewRequest = apps.get_model('core', 'ReviewRequest')
    table_name = ReviewRequest._meta.db_table
    if 'selected_section_ids' not in _column_names(schema_editor, table_name):
        return

    field = models.JSONField(blank=True, default=list)
    field.set_attributes_from_name('selected_section_ids')
    field.model = ReviewRequest
    schema_editor.remove_field(ReviewRequest, field)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_reviewrequest_detection_task'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(add_selected_section_ids, remove_selected_section_ids),
            ],
            state_operations=[
                migrations.AddField(
                    model_name='reviewrequest',
                    name='selected_section_ids',
                    field=models.JSONField(blank=True, default=list),
                ),
            ],
        ),
    ]
