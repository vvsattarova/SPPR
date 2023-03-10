# Generated by Django 4.1.5 on 2023-01-08 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pred1', models.TextField()),
                ('pred2', models.TextField()),
                ('pred3', models.TextField()),
                ('pred4', models.TextField()),
                ('pred5', models.TextField()),
                ('pred6', models.TextField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'verbose_name': 'Задача', 'verbose_name_plural': 'Задачи'},
        ),
        migrations.AddField(
            model_name='task',
            name='task',
            field=models.TextField(default='Текст', verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(default='0', max_length=50, verbose_name='Название'),
        ),
    ]
