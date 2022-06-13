# Generated by Django 3.2.13 on 2022-06-13 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StatictickerConfigfile',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('json_data', models.TextField()),
            ],
            options={
                'db_table': 'staticticker_configfile',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StatictickerStaticticker',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ticker_enabler', models.IntegerField()),
                ('background_color', models.CharField(max_length=18)),
                ('ticker_logo', models.CharField(blank=True, max_length=100, null=True)),
                ('ticker_msg', models.CharField(max_length=200)),
                ('text_color', models.CharField(max_length=40)),
                ('font_size', models.CharField(max_length=20)),
                ('font_type', models.CharField(max_length=40)),
                ('ticker_display_time', models.IntegerField()),
                ('position_box', models.CharField(max_length=12)),
                ('image', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'staticticker_staticticker',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TickerDetails',
            fields=[
                ('ticker_id', models.AutoField(primary_key=True, serialize=False)),
                ('ticker_type', models.CharField(max_length=40)),
                ('dated_on', models.DateTimeField()),
                ('ticker_json', models.TextField(blank=True, null=True)),
                ('created_for', models.CharField(max_length=300)),
                ('created_by', models.CharField(blank=True, max_length=50, null=True)),
                ('created_on', models.DateTimeField()),
                ('modified_by', models.CharField(blank=True, max_length=50, null=True)),
                ('modified_on', models.DateTimeField()),
                ('is_active', models.PositiveIntegerField()),
                ('is_deleted', models.PositiveIntegerField()),
                ('deleted_on', models.DateTimeField(blank=True, null=True)),
                ('reason_for_delete', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'db_table': 'ticker_details',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TickerHistory',
            fields=[
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('ticker_id', models.PositiveIntegerField()),
                ('ticker_type', models.CharField(max_length=40)),
                ('dated_on', models.DateTimeField()),
                ('ticker_json', models.TextField(blank=True, null=True)),
                ('created_for', models.CharField(max_length=300)),
                ('created_by', models.CharField(blank=True, max_length=50, null=True)),
                ('created_on', models.DateTimeField()),
                ('modified_by', models.CharField(blank=True, max_length=50, null=True)),
                ('modified_on', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.PositiveIntegerField()),
                ('is_deleted', models.PositiveIntegerField()),
                ('deleted_on', models.DateTimeField(blank=True, null=True)),
                ('reason_for_delete', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'db_table': 'ticker_history',
                'managed': False,
            },
        ),
    ]
