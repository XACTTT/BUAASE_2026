from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_subdetectionresult_method'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationDetectionConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detect_type', models.CharField(choices=[('image', '图片检测'), ('paper', '论文文本'), ('review', '综述文本'), ('multi', '多材料综合')], max_length=20)),
                ('method', models.CharField(choices=[('urn', 'URN'), ('bert_text', 'BERT'), ('fast_detect_gpt', 'Fast-DetectGPT')], max_length=40)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detection_configs', to='core.organization')),
            ],
            options={
                'db_table': 'organization_detection_config',
                'ordering': ['detect_type'],
                'unique_together': {('organization', 'detect_type')},
            },
        ),
    ]
