from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateField, IntegerField, PositiveBigIntegerField, PositiveIntegerField, TimeField
from django.db.models.fields.json import JSONField
from django.db.models.fields.related import ForeignKey

# Create your models here.


class Ticket(models.Model):
    ticket_no = PositiveBigIntegerField(unique=True)
    train_name = CharField(max_length=50)
    train_number = PositiveIntegerField()
    pnr = PositiveBigIntegerField(unique=True)
    date = DateField()
    time = TimeField()
    seat_class = CharField(max_length=50)
    start = CharField(max_length=50)
    destination = CharField(max_length=50)
    baseRate = PositiveBigIntegerField(null=True)
    ticketCost = PositiveBigIntegerField(null=True)


class Train_Seats(models.Model):
    train_name = CharField(max_length=50)
    train_number = IntegerField(default=0)
    seat1A = PositiveIntegerField(null=True)
    seat2A = PositiveIntegerField(null=True)
    seatFC = PositiveIntegerField(null=True)
    seat3A = PositiveIntegerField(null=True)
    seat3E = PositiveIntegerField(null=True)
    seatCC = PositiveIntegerField(null=True)
    seatSC = PositiveIntegerField(null=True)
    seat2S = PositiveIntegerField(null=True)
    total_seats = PositiveIntegerField(null=True)


class Passengers(models.Model):
    class Meta:
        verbose_name_plural = 'Members'
    pnr_number = IntegerField()
    name = CharField(max_length=50)
    aadhar_no = PositiveBigIntegerField(unique=True)
    age = PositiveIntegerField()
    gender = CharField(max_length=50)
    food = CharField(max_length=10)


class Train(models.Model):
    name = CharField(max_length=50)
    number = PositiveIntegerField(default=0)
    date = DateField()
    seat1A = PositiveIntegerField(null=True)
    seat2A = PositiveIntegerField(null=True)
    seatFC = PositiveIntegerField(null=True)
    seat3A = PositiveIntegerField(null=True)
    seat3E = PositiveIntegerField(null=True)
    seatCC = PositiveIntegerField(null=True)
    seatSC = PositiveIntegerField(null=True)
    seat2S = PositiveIntegerField(null=True)
    total_seats = PositiveIntegerField(null=True)


class Routes(models.Model):
    train = CharField(max_length=50)
    start = CharField(max_length=50)
    end = CharField(max_length=50)
    rate = PositiveIntegerField(null=True)


class Berth_Cost(models.Model):
    train_name = CharField(max_length=50)
    seat1A = PositiveIntegerField(null=True)
    seat2A = PositiveIntegerField(null=True)
    seatFC = PositiveIntegerField(null=True)
    seat3A = PositiveIntegerField(null=True)
    seat3E = PositiveIntegerField(null=True)
    seatCC = PositiveIntegerField(null=True)
    seatSC = PositiveIntegerField(null=True)
    seat2S = PositiveIntegerField(null=True)
