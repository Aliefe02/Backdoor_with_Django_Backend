# Generated by Django 4.2 on 2023-10-02 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_command_command_to_exec_timestamp_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='Files/')),
                ('filename', models.CharField(max_length=255)),
            ],
        ),
    ]