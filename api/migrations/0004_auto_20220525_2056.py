# Generated by Django 3.2.13 on 2022-05-25 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_users_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='body',
            name='id',
        ),
        migrations.RemoveField(
            model_name='categories',
            name='id',
        ),
        migrations.RemoveField(
            model_name='post',
            name='id',
        ),
        migrations.RemoveField(
            model_name='users',
            name='id',
        ),
        migrations.AlterField(
            model_name='body',
            name='bodyId',
            field=models.TextField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='categories',
            name='categoryId',
            field=models.TextField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='postId',
            field=models.TextField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='users',
            name='userId',
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]