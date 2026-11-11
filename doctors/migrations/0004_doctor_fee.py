from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctors", "0003_surgery_cost"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctor",
            name="fee",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
