# Generated by Django 5.1.2 on 2024-12-16 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_course_name_alter_customuser_role_and_more'),
        ('examination', '0007_remove_question_exam_question_exam'),
    ]

    operations = [
        migrations.AddField(
            model_name='cbtcategory',
            name='school_branch',
            field=models.ManyToManyField(blank=True, null=True, related_name='cbt_categrories', to='base.schoolbranch'),
        ),
    ]