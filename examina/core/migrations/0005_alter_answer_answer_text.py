# Generated by Django 4.1.4 on 2022-12-10 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_question_question_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer_text',
            field=models.CharField(max_length=100),
        ),
    ]
