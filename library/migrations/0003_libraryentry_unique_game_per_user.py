from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0002_libraryentry_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="libraryentry",
            name="external_game_id",
            field=models.CharField(max_length=100),
        ),
        migrations.AddConstraint(
            model_name="libraryentry",
            constraint=models.UniqueConstraint(
                fields=("user", "external_game_id"),
                name="unique_library_game_per_user",
            ),
        ),
    ]