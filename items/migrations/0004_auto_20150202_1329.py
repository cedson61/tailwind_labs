# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_auto_20150130_1122'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-modified']},
        ),
        migrations.RenameField(
            model_name='item',
            old_name='last_updated',
            new_name='modified',
        ),
    ]
