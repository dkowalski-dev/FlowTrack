# Generated by Django 5.1.7 on 2025-04-06 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0009_alter_companyclient_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyclient',
            name='address',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
        migrations.AlterField(
            model_name='companyclient',
            name='company_name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='companyclient',
            name='contact_person',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='companyclient',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
        migrations.AlterField(
            model_name='companyclient',
            name='nip',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='companyclient',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=16),
        ),
        migrations.AlterField(
            model_name='individualclient',
            name='address',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
        migrations.AlterField(
            model_name='individualclient',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
        migrations.AlterField(
            model_name='individualclient',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='individualclient',
            name='name',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='individualclient',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=16),
        ),
    ]
