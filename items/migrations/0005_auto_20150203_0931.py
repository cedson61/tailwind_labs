# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_auto_20150202_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(default=datetime.datetime(2015, 2, 3, 17, 30, 51, 360000, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='url',
            field=models.URLField(default='www.null.net', blank=True),
            preserve_default=False,
        ),
    ]
