# Generated by Django 4.2.3 on 2023-09-07 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_category_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(max_length=50),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
