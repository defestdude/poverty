# Generated by Django 4.0.4 on 2022-09-14 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0007_inflation_alter_prophetdata_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProphetDataNoCovid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ds', models.DateField(null=True)),
                ('yhat', models.DecimalField(decimal_places=10, max_digits=21)),
                ('yhat_lower', models.DecimalField(decimal_places=10, max_digits=21)),
                ('yhat_upper', models.DecimalField(decimal_places=10, max_digits=21)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]