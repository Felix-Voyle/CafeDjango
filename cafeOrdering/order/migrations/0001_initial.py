# Generated by Django 5.0.3 on 2024-03-18 07:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0009_remove_invoiceproduct_product_invoiceproduct_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line1', models.CharField(max_length=100)),
                ('address_line2', models.CharField(blank=True, max_length=100, null=True)),
                ('address_line3', models.CharField(blank=True, max_length=100, null=True)),
                ('postcode', models.CharField(max_length=10)),
                ('delivery_instructions', models.TextField(blank=True, max_length=150, null=True)),
                ('delivery_date', models.DateField()),
                ('delivery_time', models.TimeField()),
                ('order_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('order_id', models.TextField(editable=False, max_length=5, unique=True)),
                ('status', models.CharField(choices=[('ordered', 'Ordered'), ('sent', 'Sent'), ('invoiced', 'Invoiced')], default='ordered', max_length=20)),
                ('reported_problem', models.TextField(blank=True, max_length=200, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(through='order.OrderItem', to='products.product'),
        ),
    ]
