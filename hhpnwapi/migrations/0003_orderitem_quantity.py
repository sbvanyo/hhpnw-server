# Generated by Django 4.1.3 on 2024-01-17 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hhpnwapi', '0002_alter_orderitem_item_alter_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
