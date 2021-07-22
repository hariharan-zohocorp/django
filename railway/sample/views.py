from datetime import datetime, date
from decimal import Context
from typing import List
from django.db.backends.utils import format_number
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_control
from sample.models import *
from django.contrib import messages
from decouple import config
import random
from django.http import HttpResponse

from django.db import connection
# Create your views here.

class_mapping = {"seat1A": "AC First Class(1A)",
                 "seat2A": "AC 2 Tier(2A)",
                 "seatFC": "First Class(FC)",
                 "seat3A": "AC 3 Tier(3A)",
                 "seat3E": "AC 3 Economy(3E)",
                 "seatCC": "AC Chair Car(CC)",
                 "seatSL": "Sleeper(SL)",
                 "seat2S": "Second Sitting(2S)"}


def deleteTicket(request, pnr):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM sample_ticket WHERE pnr=%s", [pnr])
    cursor.execute("DELETE FROM sample_passengers WHERE pnr_number=%s", [pnr])
    cursor.close()
    messages.info(request, 'Refund Successfull!!!')
    return render(request, 'index.html')


def refund(request, pnr):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT baseRate,date FROM sample_ticket WHERE pnr=%s", [pnr])
    inst = cursor.fetchall()
    price = inst[0][0]
    journey_date = inst[0][1]
    current_date = date.today()
    deduction = 0
    if((journey_date - current_date).days >= 2):
        deduction = price*(0.25)
    price = price - deduction
    request.session['track'] = {'price': price,
                                'pnr': pnr,
                                'deduction': deduction}
    context = {
        "price": price,
        "pnr": pnr,
        "deduction": deduction
    }
    return render(request, 'refundPage.html', context)


def deleteAfter(request, id):
    cursor = connection.cursor()
    cursor.execute("SELECT baseRate,ticketCost FROM sample_ticket WHERE pnr=%s", [
                   request.session['temp']['pnr']])
    inst = cursor.fetchall()
    rate = inst[0][0]
    tc = inst[0][1]
    print(rate, tc)
    cursor.execute("DELETE FROM sample_passengers WHERE id=%s", [id])
    cursor.execute("SELECT * FROM sample_ticket WHERE pnr=%s",
                   [request.session['temp']['pnr']])
    ticket = cursor.fetchall()
    cursor.execute("SELECT * FROM sample_passengers WHERE pnr_number=%s",
                   [request.session['temp']['pnr']])
    passengers = cursor.fetchall()
    if(len(passengers) == 0):
        return refund(request, request.session['temp']['pnr'])
    else:
        cursor.execute("UPDATE sample_ticket SET ticketCost=%s WHERE pnr=%s", [
            (tc-rate), request.session['temp']['pnr']])
        context = {
            "ticket": ticket,
            "members": passengers,
        }
        return render(request, 'pnr.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteIndividual(request, id):
    cursor = connection.cursor()
    result = 0
    cursor.execute("SELECT * FROM sample_passengers WHERE id=%s", [id])
    result = len(cursor.fetchall())
    if(result != 0):
        cursor.execute("DELETE FROM sample_passengers WHERE id=%s", [id])
    # Getting Seat Count
        cursor.execute("SELECT "+str(request.session['temp']['class'])+" FROM sample_train WHERE name=%s AND date=%s", [
            request.session['temp']['train_name'], request.session['temp']['date']])
        seats = cursor.fetchone()[0]
        cursor.execute("UPDATE sample_train SET "+str(request.session['temp']['class'])+"=%s WHERE name=%s AND date=%s", [
            (seats+1), request.session['temp']['train_name'], request.session['temp']['date']])

    # Again Checking For Seat Count From DB to update the webpage
    cursor.execute("SELECT "+str(request.session['temp']['class'])+" FROM sample_train WHERE name=%s AND date=%s", [
        request.session['temp']['train_name'], request.session['temp']['date']])
    seats = cursor.fetchone()[0]
    trigger = True
    if(seats == 0):
        trigger = False
    else:
        trigger = True
    messages.info(request, 'Deleted Successfully!')
    cursor.execute("SELECT * FROM sample_passengers WHERE pnr_number=%s",
                   [request.session['temp']['pnr']])
    passengers = cursor.fetchall()

    context = {
        "created": passengers,
        "train_name": request.session['temp']['train_name'],
        "berth": class_mapping[request.session['temp']['class']],
        "train_number": request.session['temp']['train_number'],
        "available": seats,
        "trigger": trigger,
        "ticket_cost": request.session['temp']['ticket_cost']
    }
    cursor.close()
    return render(request, 'book.html', context)


def pnr(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sample_ticket WHERE pnr=%s AND ticket_no=%s", [request.POST.get(
        "PNR"), request.POST.get("ticket_number")])
    ticket = cursor.fetchall()
    print(ticket)
    cursor.execute("SELECT * FROM sample_passengers WHERE pnr_number=%s", [request.POST.get(
        "PNR")])
    passengers = cursor.fetchall()
    request.session['temp'] = {
        "pnr": request.POST.get(
            "PNR"),
        "ticket": request.POST.get("ticket_number")
    }
    context = {
        "ticket": ticket,
        "members": passengers,
    }
    cursor.close()
    return render(request, 'pnr.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    return render(request, 'index.html')


@cache_control(no_cache=True, no_store=True)
def book(request):
    train_name = ""
    train_number = 0
    base_price = 0
    cursor = connection.cursor()
    cursor.execute("SELECT train FROM (SELECT DISTINCT A.train,A.start,B.end FROM sample_routes A CROSS JOIN sample_routes B) as a WHERE start=%s AND end=%s", [
        str(request.POST.get('from')).upper(), str(request.POST.get('destination')).upper()])
    train_name = cursor.fetchone()[0]
    cursor.execute("SELECT id,rate FROM sample_routes WHERE train=%s AND start=%s", [
                   train_name, request.POST.get('from')])
    start_position = cursor.fetchall()
    cursor.execute("SELECT id,rate FROM sample_routes WHERE train=%s AND end=%s", [
                   train_name, request.POST.get('destination')])
    end_position = cursor.fetchall()
    if(start_position[0][0] == end_position[0][0]):
        base_price = start_position[0][1]
    else:
        base_price = abs(start_position[0][1]-end_position[0][1])
    print(base_price)
    cursor.execute(
        'SELECT train_number FROM sample_train_seats WHERE train_name=%s', [train_name])
    train_number = cursor.fetchone()[0]
    ticket_no = 11111+random.randint(1, 100)
    pnr = 1123436511+random.randint(1, 100)
    request.session['temp'] = {
        "train_name": train_name,
        "from": request.POST.get("from"),
        "destination": request.POST.get("destination"),
        "date": request.POST.get("date"),
        "time": request.POST.get("time"),
        "train_number": train_number,
        "class": request.POST.get("class"),
        "ticket_no": ticket_no,
        "pnr": pnr,
        "base_price": base_price,
    }
    cursor.execute("SELECT "+request.session['temp']['class']+" FROM sample_berth_cost WHERE train_name=%s", [
        request.session['temp']['train_name']])
    add_on = cursor.fetchone()[0]
    request.session['temp']['add_on'] = add_on
    cursor.execute(
        'SELECT * FROM sample_train WHERE name=%s AND date=%s;', [train_name, request.POST.get('date')])
    instance = cursor.fetchone()
    ticket_cost = base_price + (base_price*(add_on/100))
    request.session['temp']['ticket_cost'] = ticket_cost
    if(instance != None):
        request.session['temp']['class'] = request.POST.get("class")
        cursor.execute("SELECT "+request.session['temp']['class']+" FROM sample_train WHERE name=%s AND date=%s;", [
            train_name, request.POST.get('date')])
        available = cursor.fetchall()[0]
        trigger = True
        if(available == 0):
            trigger = False
        else:
            trigger = True
        context = {
            "train_name": instance[1].upper(),
            "train_number": instance[2],
            "berth": class_mapping[request.POST.get("class")],
            "available": available,
            "trigger": trigger,
            "ticket_cost": ticket_cost}
    else:
        cursor.execute(
            "SELECT * FROM sample_train_seats WHERE train_name=%s", [train_name])
        nested_values = cursor.fetchall()
        print(nested_values)
        cursor.execute("INSERT INTO sample_train(name,number,date,seat1A,seat2A,seat2S,seat3A,seat3E,seatCC,seatFC,seatSC,total_seats) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                       [train_name, train_number, request.POST.get("date"),
                        nested_values[0][3],
                        nested_values[0][4],
                        nested_values[0][5],
                        nested_values[0][6],
                        nested_values[0][7],
                        nested_values[0][8],
                        nested_values[0][9],
                        nested_values[0][10],
                        nested_values[0][11]])
        cursor.execute("SELECT * FROM sample_train WHERE name=%s AND date=%s",
                       [request.session['temp']['train_name'], request.session['temp']['date']])
        instance = cursor.fetchall()[0]
        cursor.execute("SELECT "+request.POST.get("class")+" FROM sample_train WHERE name=%s AND date=%s", [
            train_name, request.POST.get('date')])
        available = cursor.fetchone()[0]
        trigger = True
        if(available == 0):
            trigger = False
        else:
            trigger = True
        context = {
            "train_name": instance[1].upper(),
            "train_number": instance[2],
            "berth": class_mapping[request.POST.get("class")],
            "available": available,
            "trigger": trigger,
            "ticket_cost": ticket_cost
        }
        cursor.close()
    return render(request, 'book.html', context)


@cache_control(no_cache=True, no_store=True)
def create(request):
    if(request.method == "POST"):
        name = request.POST.get("name")
        aadhar = request.POST.get("aadhar")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        food = request.POST.get("food").upper()
        if(len(name) <= 49 and len(str(aadhar)) == 12 and len(gender) < 49 and len(food) <= 10):
            cursor = connection.cursor()
            try:
                cursor.execute("INSERT INTO sample_ticket(ticket_no,train_name,train_number,pnr,date,time,seat_class,start,destination)  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                               [request.session['temp']['ticket_no'],
                                request.session['temp']['train_name'],
                                request.session['temp']['train_number'],
                                request.session['temp']['pnr'],
                                request.session['temp']['date'],
                                request.session['temp']['time'],
                                request.session['temp']['class'],
                                request.session['temp']['from'],
                                request.session['temp']['destination'],
                                ])
            except(Exception):
                pass
            cursor.execute("INSERT INTO sample_passengers(name,aadhar_no,age,gender,food,pnr_number) VALUES(%s,%s,%s,%s,%s,%s)",
                           [name, aadhar, age, gender, food, request.session["temp"]["pnr"]])
            cursor.execute("SELECT * FROM sample_passengers WHERE pnr_number=%s",
                           [request.session['temp']['pnr']])
            passengers = cursor.fetchall()
            cursor.execute("SELECT "+str(request.session['temp']['class'])+" FROM sample_train WHERE name=%s AND date=%s", [
                request.session['temp']['train_name'], request.session['temp']['date']])
            seats = cursor.fetchone()[0]
            cursor.execute("UPDATE sample_train SET "+str(request.session['temp']['class'])+"=%s WHERE name=%s AND date=%s", [
                (seats-1), request.session['temp']['train_name'], request.session['temp']['date']])
            cursor.execute("SELECT "+str(request.session['temp']['class'])+" FROM sample_train WHERE name=%s AND date=%s", [
                request.session['temp']['train_name'], request.session['temp']['date']])
            seats = cursor.fetchone()[0]
        trigger = True
        if(seats == 0):
            trigger = False
        else:
            trigger = True
        context = {
            "created": passengers,
            "train_name": request.session['temp']['train_name'],
            "berth": class_mapping[request.session['temp']['class']],
            "train_number": request.session['temp']['train_number'],
            "available": seats,
            "trigger": trigger,
            "ticket_cost": request.session['temp']['ticket_cost']
        }
        cursor.close()
        return render(request, 'book.html', context)

    return render(request, 'create.html')


def display(request):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM sample_passengers WHERE pnr_number=%s",
                   [request.session['temp']['pnr']])

    inst = cursor.fetchall()
    cursor.execute("UPDATE sample_ticket SET baseRate=%s,ticketCost=%s WHERE pnr=%s", [
                   request.session['temp']['ticket_cost'], (len(inst)*request.session['temp']['ticket_cost']), request.session['temp']['pnr']])
    if(len(inst) == 0):
        cursor.close()
        return HttpResponse("<html><body><h1>Cannot Book Ticket !!!</h1><br><h3>No Passengers Were Added</h3></body></html>")
    else:
        rate = float("{:.2f}".format(
            len(inst)*(request.session['temp']['ticket_cost'])))
        context = {
            "obj": request.session['temp'],
            "inst": inst,
            "rate": rate
        }
        cursor.close()
        return render(request, 'display.html', context)


'''
                                      cursor.execute("INSERT INTO sample_ticket(ticket_no,train_name,train_number,pnr,date,time,seat_class,start,destination)  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                               [request.session['temp']['ticket_no'],
                                request.session['temp']['train_name'],
                                request.session['temp']['train_number'],
                                request.session['temp']['pnr'],
                                request.session['temp']['date'],
                                request.session['temp']['time'],
                                request.session['temp']['class'],
                                request.session['temp']['from'],
                                request.session['temp']['destination'],
                                ])
                    '''
