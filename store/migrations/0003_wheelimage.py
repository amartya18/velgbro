# Generated by Django 3.0 on 2019-12-26 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_post_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='WheelImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Post')),
            ],
        ),
    ]