# Manual migration to alter Holiday.date to be nullable
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_add_month_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holiday',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
