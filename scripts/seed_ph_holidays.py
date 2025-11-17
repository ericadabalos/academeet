# Seed Philippines fixed-date national holidays (recurring yearly)
# Run with: python manage.py shell < scripts/seed_ph_holidays.py
from core.models import Holiday

def seed():
    holidays = [
        (1, 1, "New Year's Day"),
        (1, 23, "First Philippine Republic Day"),
        (1, 29, "Chinese New Year"),
        (2, 2, "Constitution Day"),
        (2, 25, "EDSA Revolution Anniversary"),
        (4, 9, "Day of Valor"),
        (4, 27, "Lapu-Lapu Day"),
        (5, 1, "Labour Day"),
        (6, 12, "Independence Day"),
        (6, 19, "José Rizal's Birthday"),
        (7, 27, "Iglesia ni Cristo Day"),
        (8, 21, "Ninoy Aquino Day"),
        (8, 25, "National Heroes' Day"),
        (11, 1, "All Saints' Day"),
        (11, 2, "All Souls' Day"),
        (11, 30, "Bonifacio Day"),
        (12, 8, "Feast of the Immaculate Conception"),
        (12, 24, "Christmas Eve"),
        (12, 25, "Christmas Day"),
        (12, 30, "Rizal Day"),
        (12, 31, "New Year's Eve"),
    ]

    created = 0
    for month, day, name in holidays:
        obj, created_flag = Holiday.objects.get_or_create(
            month=month,
            day=day,
            defaults={
                'name': name,
                'description': ''
            }
        )
        if created_flag:
            created += 1
            print(f"Created: {obj}")
        else:
            print(f"Exists: {obj}")

    print(f"Seed complete. New holidays created: {created}")

if __name__ == '__main__':
    seed()
