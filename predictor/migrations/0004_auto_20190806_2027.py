# Generated by Django 2.2.3 on 2019-08-06 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0003_auto_20190806_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='categoryId',
            field=models.PositiveIntegerField(default=175673, unique=True),
        ),
    ]
