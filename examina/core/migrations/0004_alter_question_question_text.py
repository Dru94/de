# Generated by Django 4.1.4 on 2022-12-10 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_test_question_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=200),
        ),
    ]
