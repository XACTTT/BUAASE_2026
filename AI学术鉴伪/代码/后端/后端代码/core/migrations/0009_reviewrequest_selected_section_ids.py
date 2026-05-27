from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_reviewrequest_detection_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewrequest',
            name='selected_section_ids',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
