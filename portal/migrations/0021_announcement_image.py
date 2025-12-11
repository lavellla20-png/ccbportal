# Generated migration for adding image field to Announcement model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0020_event_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='image',
            field=models.ImageField(blank=True, help_text='Announcement image', null=True, upload_to='announcements/'),
        ),
    ]

