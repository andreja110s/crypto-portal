# -*- coding: utf-8 -*-
from flask import *
from database import database
from datetime import datetime, tzinfo
import random
import json
import re
import hashlib
import numpy as np

try:
    basestring
    decode = lambda x: x.decode("utf-8")
except NameError:
    decode = lambda x: x

app = Blueprint('transposition', __name__)

def getText(id):
    db = database.dbcon()
    cur = db.cursor()
    cur.execute("SELECT text, language FROM substitution WHERE id = %s", [id])
    txt = cur.fetchone()
    cur.close()
    return txt
    
def dajVCaps (text):
    return text.upper().replace(" ", "")
    
def izberiBesedilo():
    prvo="Tukaj ni skrivnosti"
    drugo="Jaz sem stegozaver"
    tretje="Ljudje pišemo s svinčniki in kemiki"
    cetrto="Univerza v Ljubljani Fakulteta za računalništvo in informatiko"
    peto="V transpozicijski šifri ostanejo črke originalnega sporočila nespremenjene njihova mesta pa so pomešana na nek sistematičen način"
    sesto="Hackerji so osebe ki vdirajo v računalniške sisteme brez zahtevanih pooblastil z namenom da se okoristijo ali pa samo zato da dokažejo da je to mogoče"
    
    izberi=random.randint(1, 6)
    
    if izberi == 1:
        return prvo
    elif izberi ==2:
        return drugo
    elif izberi ==3:
        return tretje
    elif izberi ==4:
        return cetrto
    elif izberi ==5:
        return peto
    elif izberi ==6:
        return sesto
    
def railCrypt (text):
    dolzinaBesedila= len(text)
    kljuc= random.randint(2, int (dolzinaBesedila/2))
    tab=np.array([np.array(["" for i in range(dolzinaBesedila)]) for j in range(kljuc)])
    vis=0
    gorDol=0
    for i in range(dolzinaBesedila):
        tab[vis][i]=text[i]
        if gorDol == 0:
            if vis+1 == kljuc:
                vis-=1
                gorDol=1
            else:
                vis+=1
        else:
            if vis == 0:
                vis+=1
                gorDol=0
            else:
                vis-=1
    tajnopis=""
    
    for i in range(kljuc):
        tajnopis+= ''.join(tab[i])
    return tajnopis, kljuc
    
def narediNakljucnoSteviloDolzine(n):
    #zacetek= 10**(n-1)
    #konec= (10**n)-1
    #stevilo = random.randint(zacetek, konec)
    
    #POPRAVI IN NAREDI PRAV!!!!
    
    
    return stevilo
    

def transpozicijaStolpcev (text):
    dolzinaBesedila=len(text)
    kljuc= random.randint(2, int (dolzinaBesedila/2))
    visina=int (dolzinaBesedila/kljuc)
    tajnopis= ""
    tab=np.array([np.array(["" for i in range(kljuc)]) for j in range (visina)])
    vis=0
    dolz=0
    for i in range(dolzinaBesedila):
        tab[vis][dolz]=text[i]
        dolz+=1
        if dolz == kljuc:
            dolz=0
            vis+=1
    if visina * kljuc != dolzinaBesedila:
        ostanek= dolzinaBesedila- visina * kljuc
        #nafilaj tolko random črk notr
    #naredi random število dolgo toliko, kolikor je ključ                                   DONE
    kljuc2= narediNakljucnoSteviloDolzine(kljuc)
    #beri tiste stolpce, daj jih v spremenljivko tajnopis
    for x in range(kljuc):
        spr=str(kljuc2)[0]
        tajnopis=tab[:,int (spr)]
    
    return (tajnopis, kljuc2)
    
        
    

@app.route('/')
def index():
    return redirect('transposition/play')

@app.route('/play')
def play():
    cistopis = izberiBesedilo()
    cistopis = dajVCaps(cistopis)
    tajnopis,kljuc = railCrypt(cistopis)
    
    cistopis2= cistopis.upper().replace(" ", "")
    
    return render_template("transposition.play.html", name=tajnopis, key=kljuc)

@app.route('/description')
def description():
    return render_template("transposition.description.html")
