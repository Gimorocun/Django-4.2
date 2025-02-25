"""
在不使用 manage.py migrate 的情况下
通过 syncdb 命令,实现将各个 app 的权限注册到 permission 和 contenttype 内

执行方法
python manage.py syncdb [--database]

注意: 此操作并不会创建任何表,需要提前手动执行 sql 创建
注意: 仅适用于高版本 django
"""

import django
from django.core.management.base import BaseCommand
from django.contrib.auth.management import create_permissions
from django.db import DEFAULT_DB_ALIAS


class Command(BaseCommand):
    help = 'Manually create permissions for models in the given app.'

    def add_arguments(self, parser):
        parser.add_argument('app_label', nargs='?', help='App label of an application to create permissions for.')
        parser.add_argument('--database', default=DEFAULT_DB_ALIAS,
                            help='Nominates a database to synchronize. Defaults to the "default" database.')

    def handle(self, *args, **options):
        app_label = options['app_label']
        database = options['database']
        if database and database == django.conf.settings.DATABASES['default']['NAME']:
            database = 'default'

        if app_label:
            app_config = django.apps.apps.get_app_config(app_label)
            create_permissions(app_config, using=database)
            self.stdout.write(self.style.SUCCESS(f"Permissions created above for app '{app_label}'."))
        else:
            self.stdout.write(self.style.WARNING("Please provide the app label as argument."))
