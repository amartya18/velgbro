# Generated by Django 3.0 on 2020-01-07 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20200107_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wheel',
            name='condition',
            field=models.CharField(choices=[('NEW', 'New'), ('USED', 'Used')], default='blank', max_length=4),
        ),
    ]