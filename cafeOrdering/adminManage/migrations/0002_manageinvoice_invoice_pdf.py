# Generated by Django 5.0.3 on 2024-04-06 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminManage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='manageinvoice',
            name='invoice_pdf',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
