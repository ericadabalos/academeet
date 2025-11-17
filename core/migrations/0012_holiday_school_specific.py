from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0011_alter_holiday_date_nullable'),
    ]
    operations = [
        migrations.AddField(
            model_name='holiday',
            name='school_specific',
            field=models.BooleanField(default=False, help_text='Is this a school-declared date/event?'),
        ),
    ]
