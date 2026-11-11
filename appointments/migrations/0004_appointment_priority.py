from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appointments", "0003_alter_appointment_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="priority",
            field=models.CharField(
                choices=[("High", "High"), ("Medium", "Medium"), ("Low", "Low")],
                default="Low",
                max_length=10,
            ),
        ),
    ]