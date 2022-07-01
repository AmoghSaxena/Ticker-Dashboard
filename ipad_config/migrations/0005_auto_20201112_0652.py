# Generated by Django 2.2.7 on 2020-11-12 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ipad_config', '0004_javaconfigchanges'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staticcontent',
            name='file_type',
            field=models.CharField(choices=[('FILE', 'FILE'), ('ZIP', 'ZIP')], help_text='Suggested zip file structure: service_dir>zip', max_length=30),
        ),
        migrations.CreateModel(
            name='IpadConfigChanges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('added', 'added'), ('deleted', 'deleted')], max_length=50)),
                ('type', models.CharField(choices=[('settings', 'settings'), ('language', 'language'), ('image', 'image')], max_length=50)),
                ('name', models.TextField()),
                ('table', models.CharField(max_length=100, null=True)),
                ('queue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='changes_queue', to='ipad_config.ExportQueue')),
            ],
            options={
                'db_table': 'ipad_config_changes',
            },
        ),
    ]
