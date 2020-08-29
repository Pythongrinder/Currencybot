from django.shortcuts import render
from django import forms
import sqlite3
from django.http import HttpResponse, HttpResponseRedirect
#from .models import Notifications
from sqlite3 import Error



class InputForm(forms.Form):
    Link = forms.CharField(required=True, max_length=200, label="link")
    Name = forms.CharField(required=True, max_length=200, label="Name")
    BiggerThan = forms.FloatField(required=True, label="bigger than")
    SmallerThan = forms.FloatField(required=True, label="bigger than")

def create_connection(db_file):

    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn



"""
def inserting():
    conn = create_connection(r'/home/jan/Desktop/python/currenciesbot/currency/db.sqlite3')
    cur = conn.cursor()
    global Link 
    global BiggerThan 
    global SmallerThan
    #textchecker(name, description, auctiondate, propertylink, voivodeship, city, price, meterage, propertytype, imglink)
    sql = f"INSERT INTO Notifications (Link, Biggerthan, Smallerthan) VALUES (%s,%s,%s)"
    records_to_insert = (Link, Biggerthan, Smallerthan) 
    cur = conn.cursor()
    cur.execute(sql,records_to_insert)
"""
def mainpage(request):
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        print("Database Successfully Connected to SQLite")
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    global Link
    global Name
    global BiggerThan
    global SmallerThan
    global Notifications
    if 'adding' in request.POST:
        form = InputForm(request.POST)
        if form.is_valid():
            Link = form.cleaned_data['Link']
            Name = form.cleaned_data['Name']
            BiggerThan = form.cleaned_data['BiggerThan']
            SmallerThan = form.cleaned_data['SmallerThan']
            #textchecker(name, description, auctiondate, propertylink, voivodeship, city, price, meterage, propertytype, imglink)
            #cur = conn.cursor()
            #sqlite_delete_table_query2 = '''DROP TABLE Notifications   '''
            #cursor.execute(sqlite_delete_table_query2)
            sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS Notifications (
                                id INTEGER PRIMARY KEY,
                                Name Text NOT NULL,
                                Link TEXT NOT NULL,
                                BiggerThan FLOAT(16,2),
                                SmallerThan FLOAT(16,2));'''
            cursor.execute(sqlite_create_table_query)
            cursor.execute(f"""INSERT INTO Notifications (Link, Name, BiggerThan, SmallerThan) VALUES (?,?,?,?);""", (Link, Name, BiggerThan, SmallerThan))
            conn.commit()
            return HttpResponseRedirect('/')
    cursor.execute("""SELECT * From Notifications""")
    Notifications = cursor.fetchall()
    print(Notifications)

    if 'delete' in request.POST: 
        iddel = request.POST['delete']
        print(iddel)
        cursor.execute(f"DELETE FROM Notifications WHERE id = {iddel}")
        conn.commit()
        return HttpResponseRedirect('/')
    for row in Notifications:
        print(row)

    return render(request, 'mainpage.html', {'form': InputForm, 'Notifications': Notifications})

