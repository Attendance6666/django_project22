from django.db import migrations


def create_admin(apps, schema_editor):
    User = apps.get_model("auth", "User")

    username = "admin"
    password = "Admin123!"  # можешь поменять

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email="admin@example.com",
            password=password,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("attendance_tracker", "0002_alter_attendance_student_alter_grou"),  # <-- поправишь строку ниже
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]
from django.db import migrations


def create_admin(apps, schema_editor):
    User = apps.get_model("auth", "User")

    username = "admin"
    password = "Admin123!"  # можешь поменять

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email="admin@example.com",
            password=password,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("attendance_tracker", "0002_alter_attendance_student_alter_group_description"), 
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]
