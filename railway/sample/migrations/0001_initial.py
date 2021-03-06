# Generated by Django 3.2.5 on 2021-07-20 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Berth_Cost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('train_name', models.CharField(max_length=50)),
                ('seat1A', models.PositiveIntegerField(null=True)),
                ('seat2A', models.PositiveIntegerField(null=True)),
                ('seatFC', models.PositiveIntegerField(null=True)),
                ('seat3A', models.PositiveIntegerField(null=True)),
                ('seat3E', models.PositiveIntegerField(null=True)),
                ('seatCC', models.PositiveIntegerField(null=True)),
                ('seatSC', models.PositiveIntegerField(null=True)),
                ('seat2S', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Passengers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pnr_number', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('aadhar_no', models.PositiveBigIntegerField(unique=True)),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(max_length=50)),
                ('food', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Members',
            },
        ),
        migrations.CreateModel(
            name='Routes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('train', models.CharField(max_length=50)),
                ('start', models.CharField(max_length=50)),
                ('end', models.CharField(max_length=50)),
                ('rate', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_no', models.PositiveBigIntegerField(unique=True)),
                ('train_name', models.CharField(max_length=50)),
                ('train_number', models.PositiveIntegerField()),
                ('pnr', models.PositiveBigIntegerField(unique=True)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('seat_class', models.CharField(max_length=50)),
                ('start', models.CharField(max_length=50)),
                ('destination', models.CharField(max_length=50)),
                ('baseRate', models.PositiveBigIntegerField(null=True)),
                ('ticketCost', models.PositiveBigIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('number', models.PositiveIntegerField(default=0)),
                ('date', models.DateField()),
                ('seat1A', models.PositiveIntegerField(null=True)),
                ('seat2A', models.PositiveIntegerField(null=True)),
                ('seatFC', models.PositiveIntegerField(null=True)),
                ('seat3A', models.PositiveIntegerField(null=True)),
                ('seat3E', models.PositiveIntegerField(null=True)),
                ('seatCC', models.PositiveIntegerField(null=True)),
                ('seatSC', models.PositiveIntegerField(null=True)),
                ('seat2S', models.PositiveIntegerField(null=True)),
                ('total_seats', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Train_Seats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('train_name', models.CharField(max_length=50)),
                ('train_number', models.IntegerField(default=0)),
                ('seat1A', models.PositiveIntegerField(null=True)),
                ('seat2A', models.PositiveIntegerField(null=True)),
                ('seatFC', models.PositiveIntegerField(null=True)),
                ('seat3A', models.PositiveIntegerField(null=True)),
                ('seat3E', models.PositiveIntegerField(null=True)),
                ('seatCC', models.PositiveIntegerField(null=True)),
                ('seatSC', models.PositiveIntegerField(null=True)),
                ('seat2S', models.PositiveIntegerField(null=True)),
                ('total_seats', models.PositiveIntegerField(null=True)),
            ],
        ),
    ]
