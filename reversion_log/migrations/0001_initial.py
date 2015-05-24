# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reversion', '0002_auto_20141216_1509'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogVersion',
            fields=[
            ],
            options={
                'verbose_name': 'Version',
                'verbose_name_plural': 'Versions',
                'proxy': True,
            },
            bases=('reversion.version',),
        ),
        migrations.CreateModel(
            name='RevisionLog',
            fields=[
            ],
            options={
                'verbose_name': 'Log',
                'ordering': ('-pk',),
                'verbose_name_plural': 'Log',
                'proxy': True,
            },
            bases=('reversion.revision',),
        ),
    ]
