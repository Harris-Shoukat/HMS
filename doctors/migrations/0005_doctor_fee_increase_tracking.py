from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctors", "0004_doctor_fee"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctor",
            name="last_fee_increase_amount",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=10,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="doctor",
            name="last_fee_increase_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]