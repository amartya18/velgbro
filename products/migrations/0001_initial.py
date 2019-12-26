# Generated by Django 3.0 on 2019-12-26 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0003_wheelimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wheel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.Post')),
            ],
        ),
    ]
