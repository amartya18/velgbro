# Generated by Django 3.0 on 2020-01-07 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20200107_0728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wheel',
            name='offset',
            field=models.IntegerField(blank=True),
        ),
    ]