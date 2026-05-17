from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detectiontask',
            name='container',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='detection_tasks',
                to='core.resourcecontainer',
            ),
        ),
        migrations.AddField(
            model_name='detectiontask',
            name='detect_type',
            field=models.CharField(
                choices=[
                    ('image', 'Image'),
                    ('paper', 'Paper'),
                    ('review', 'Review'),
                    ('multi', 'Multi Material'),
                ],
                db_index=True,
                default='image',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='detectiontask',
            name='extra_payload',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='detectiontask',
            name='failure_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='StructuredDetectionResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overall_is_fake', models.BooleanField(blank=True, null=True)),
                ('confidence_score', models.FloatField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, null=True)),
                ('result_payload', models.JSONField(blank=True, default=dict)),
                ('ai_response', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                (
                    'detection_task',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='structured_result',
                        to='core.detectiontask',
                    ),
                ),
            ],
            options={
                'indexes': [models.Index(fields=['created_at'], name='core_structu_created_324f6f_idx')],
            },
        ),
    ]
