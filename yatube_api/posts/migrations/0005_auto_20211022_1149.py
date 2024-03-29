# Generated by Django 2.2.16 on 2021-10-22 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20211022_1144'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique_subscription',
        ),
        migrations.RenameField(
            model_name='follow',
            old_name='author',
            new_name='following',
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'following'), name='unique_subscription'),
        ),
    ]
