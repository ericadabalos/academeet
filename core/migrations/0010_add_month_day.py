# Generated manual migration: add nullable month/day fields to Holiday
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_holiday'),
    ]

    operations = [
        migrations.AddField(
            model_name='holiday',
            name='month',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='holiday',
            name='day',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
