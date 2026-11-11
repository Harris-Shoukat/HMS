from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctors", "0002_surgery"),
    ]

    operations = [
        migrations.AddField(
            model_name="surgery",
            name="cost",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
