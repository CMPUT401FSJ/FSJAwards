# Generated by Django 2.0.2 on 2018-03-14 02:47

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('FSJ', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('committeeid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('committee_name', models.TextField(verbose_name='Committee Name')),
                ('adjudicators', models.ManyToManyField(to='FSJ.Adjudicator')),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='Code')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.RemoveField(
            model_name='award',
            name='programs',
        ),
        migrations.AlterField(
            model_name='student',
            name='program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='FSJ.Program'),
        ),
        migrations.AddField(
            model_name='committee',
            name='awards',
            field=models.ManyToManyField(to='FSJ.Award'),
        ),
        migrations.AddField(
            model_name='award',
            name='programs',
            field=models.ManyToManyField(blank=True, to='FSJ.Program'),
        ),
    ]
