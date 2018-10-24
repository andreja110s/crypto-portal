# -*- coding: utf-8 -*-
from flask import *
from database import database
from datetime import datetime, tzinfo
import random
import json
import re
import hashlib
import numpy as np
import string

try:
    basestring
    decode = lambda x: x.decode("utf-8")
except NameError:
    decode = lambda x: x

app = Blueprint('transposition', __name__)

level_trans = {2: 0, -1: 1}

def getText(id):
    db = database.dbcon()
    cur = db.cursor()
    cur.execute("SELECT text, language FROM substitution WHERE id = %s", [id])
    txt = cur.fetchone()
    cur.close()
    return txt
    
def indices(level, language=None):
    db = database.dbcon()
    cur = db.cursor()
    if language == None:
        cur.execute("SELECT id FROM substitution WHERE level = %s ORDER BY id",
                    [level_trans.get(level, level)])
    else:
        cur.execute("SELECT id FROM substitution WHERE level = %s AND language = %s ORDER BY id",
                    [level_trans.get(level, level), language])
    ids = [x[0] for x in cur.fetchall()]
    cur.close()
    if level in level_trans:
        random.seed("Random seed:)%d" % level)
        random.shuffle(ids)
        random.seed()
    return ids
    
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
        
def izberiBesedilo2():
    besedilo= indices (1, language)
    
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
        
    kljuc=str(kljuc)
    return tajnopis, kljuc
    
def narediNakljucnoSteviloDolzine(n):
    tab= np.arange(1,n+1)
    np.random.shuffle(tab)
    
    kljucLepse=(' '.join(map(str, tab)))
    
    return tab, kljucLepse
    

def transpozicijaStolpcev (text):
    dolzinaBesedila=len(text)
    kljuc= random.randint(2, int (dolzinaBesedila/2))
    visina=int (dolzinaBesedila/kljuc) + 1
    tajnopis= ""
    
    dodatek=""
    dimenzija= visina*kljuc
    
    if dimenzija > dolzinaBesedila: 
        ostanek= dimenzija - dolzinaBesedila
        abeceda="abcdefghijklmnoprstuvz"
        for i in range(ostanek):
            crka=random.randint(0, 21)
            dodatek= abeceda[crka]
            dodatek=dodatek.upper()
            text+=dodatek
    
    text=list(text)
    text=np.reshape(text, (visina, kljuc))
    
    kljuc2, kljuc3= narediNakljucnoSteviloDolzine(kljuc)                                #naredi random število dolgo toliko, kolikor je stolpcev
    
    for x in range(kljuc):                                                      #beri tiste stolpce, daj jih v spremenljivko tajnopis
        stStolpcaKiGaBeremo=kljuc2[x]-1
        for y in range (visina):
            tajnopis+=text[y][stStolpcaKiGaBeremo]
    
    return (tajnopis, kljuc3)
    
def transpozicijaVrstic (text):
    dolzinaBesedila=len(text)
    kljuc= random.randint(2, int (dolzinaBesedila/2))
    visina= int(dolzinaBesedila/kljuc) + 1
    tajnopis=""
    
    dodatek=""
    dimenzija= visina*kljuc
    
    if dimenzija > dolzinaBesedila: 
        ostanek= dimenzija - dolzinaBesedila
        abeceda="abcdefghijklmnoprstuvz"
        for i in range(ostanek):
            crka=random.randint(0, 21)
            dodatek= abeceda[crka]
            dodatek=dodatek.upper()
            text+=dodatek
    
    text=list(text)
    text=np.reshape(text, (visina, kljuc))
    text=np.transpose(text)
    
    kljuc2, kljuc3= narediNakljucnoSteviloDolzine(kljuc)                                #naredi random stevilo dolgo toliko, kolikor je vrstic
    for x in range(kljuc):                                                      #beri tiste vrstice, daj jih v spremenljivko tajnopis
        stVrsticeKiJoBeremo=kljuc2[x]-1
        for y in range (visina):
            tajnopis+=text[stVrsticeKiJoBeremo][y]
        
    return (tajnopis, kljuc3)

@app.route('/')
def index():
    return redirect('transposition/play')

@app.route('/play')
def play():
    #language= None
    #texts = indices(1, language)
    #idx = random.randrange(len(texts))
    
    #zaCistopis= getText(texts[idx])[0]
    #zaCistopis= re.sub(r'[\W0-9_]', "", zaCistopis)            #zbrise locila
    #zaCistopis= zaCistopis.upper()                              #da vse v velike crke
    
    #toZakriptiramo= zaCistopis.replace(" ", "")                    #to damo v funkcije za sifriranje (ne sme imeti presledkov, locil, mora biti v uppercase)       #tukaj odstranimo presledke
    #toZakriptiramo= re.sub(r'[\W0-9_]', "", toZakriptiramo)          #tukaj odstranimo locila (za gvisno se 1x)
    #toZakriptiramo= toZakriptiramo.upper()                            #tukaj damo v upper
    ##text = re.sub(r'\s', '', text)
    #vrsta=""
    
    
    cistopis = izberiBesedilo()
    cistopis2= cistopis.upper()
    cistopis = dajVCaps(cistopis)
    
    
    #izberi=random.randint(1, 3)
    #if izberi == 1:
    #    tajnopis,kljuc = railCrypt(toZakriptiramo)
    #    vrsta= "Rail fence"
    #elif izberi ==2:
    #    tajnopis,kljuc = transpozicijaStolpcev(toZakriptiramo)
     #   vrsta= "Transpozicija stolpcev"
    #elif izberi ==3:
    #    tajnopis,kljuc = transpozicijaVrstic(toZakriptiramo)
    #    vrsta= "Transpozicija vrstic"
        
    izberi=random.randint(1, 3)
    if izberi ==1:
        tajnopis,kljuc = railCrypt(cistopis)
        vrsta= "Rail fence"
    if izberi ==2:
        tajnopis,kljuc = transpozicijaStolpcev(cistopis)
        vrsta= "Transpozicija stolpcev"
    elif izberi ==3:
        tajnopis,kljuc = transpozicijaVrstic(cistopis)
        vrsta= "Transpozicija vrstic"
        
    return render_template("transposition.play.html", name=tajnopis, key=kljuc, cistoo= cistopis2, vrstaa= vrsta)
    
    #return render_template("transposition.play.html", name=tajnopis, key=kljuc, cistoo= zaCistopis, vrstaa= vrsta)

@app.route('/description')
def description():
    return render_template("transposition.description.html")
    
@app.route('/izberi')
def izberi():
    return render_template("transposition.izberi.html")
    
@app.route('/RFH')
def rfh():
    language= None
    texts = indices(1, language)
    idx = random.randrange(len(texts))
    
    zaCistopis= getText(texts[idx])[0]
    zaCistopis= re.sub(r'[\W0-9_]', "", zaCistopis)            #zbrise locila
    zaCistopis= zaCistopis.upper()                              #da vse v velike crke
    
    toZakriptiramo= zaCistopis.replace(" ", "")                    #to damo v funkcije za sifriranje (ne sme imeti presledkov, locil, mora biti v uppercase)       #tukaj odstranimo presledke
    toZakriptiramo= re.sub(r'[\W0-9_]', "", toZakriptiramo)          #tukaj odstranimo locila (za gvisno se 1x)
    toZakriptiramo= toZakriptiramo.upper()                            #tukaj damo v upper
    vrsta=""
    
    tajnopis,kljuc = railCrypt(toZakriptiramo)
    
    zaNalogo="Naloga za vajo: Rail fence"
    TL="T"
    
    return render_template("transposition.play.html", name=tajnopis, key=kljuc, cistoo= zaCistopis, tezavnost=TL, imeNaloge= zaNalogo)
    
@app.route('/RFE')
def rfe():
    language= None
    texts = indices(1, language)
    idx = random.randrange(len(texts))
    
    zaCistopis= getText(texts[idx])[0]
    zaCistopis= re.sub(r'[\W0-9_]', "", zaCistopis)            #zbrise locila
    zaCistopis= zaCistopis.upper()                              #da vse v velike crke
    
    toZakriptiramo= zaCistopis.replace(" ", "")                    #to damo v funkcije za sifriranje (ne sme imeti presledkov, locil, mora biti v uppercase)       #tukaj odstranimo presledke
    toZakriptiramo= re.sub(r'[\W0-9_]', "", toZakriptiramo)          #tukaj odstranimo locila (za gvisno se 1x)
    toZakriptiramo= toZakriptiramo.upper()                            #tukaj damo v upper
    vrsta=""
    
    tajnopis,kljuc = railCrypt(toZakriptiramo)
    
    zaNalogo="Naloga za vajo: Rail fence"
    TL="L"
    
    return render_template("transposition.play.html", name=tajnopis, key=kljuc, cistoo= zaCistopis, tezavnost=TL, imeNaloge= zaNalogo)
    
@app.route('/TSE')
def tse():
    language= None
    texts = indices(1, language)
    idx = random.randrange(len(texts))
    
    zaCistopis= getText(texts[idx])[0]
    zaCistopis= re.sub(r'[\W0-9_]', "", zaCistopis)            #zbrise locila
    zaCistopis= zaCistopis.upper()                              #da vse v velike crke
    
    toZakriptiramo= zaCistopis.replace(" ", "")                    #to damo v funkcije za sifriranje (ne sme imeti presledkov, locil, mora biti v uppercase)       #tukaj odstranimo presledke
    toZakriptiramo= re.sub(r'[\W0-9_]', "", toZakriptiramo)          #tukaj odstranimo locila (za gvisno se 1x)
    toZakriptiramo= toZakriptiramo.upper()                            #tukaj damo v upper
    vrsta=""
    
    tajnopis,kljuc = transpozicijaStolpcev(toZakriptiramo)
    
    zaNalogo="Naloga za vajo: Transpozicija stolpcev"
    TL="L"
    
    return render_template("transposition.play.html", name=tajnopis, key=kljuc, cistoo= zaCistopis, tezavnost=TL, imeNaloge= zaNalogo)

@app.route('/TSH')
def tsh():
    language= None
    texts = indices(1, language)
    idx = random.randrange(len(texts))
    
    zaCistopis= getText(texts[idx])[0]
    zaCistopis= re.sub(r'[\W0-9_]', "", zaCistopis)            #zbrise locila
    zaCistopis= zaCistopis.upper()                              #da vse v velike crke
    
    toZakriptiramo= zaCistopis.replace(" ", "")                    #to damo v funkcije za sifriranje (ne sme imeti presledkov, locil, mora biti v uppercase)       #tukaj odstranimo presledke
    toZakriptiramo= re.sub(r'[\W0-9_]', "", toZakriptiramo)          #tukaj odstranimo locila (za gvisno se 1x)
    toZakriptiramo= toZakriptiramo.upper()                            #tukaj damo v upper
    vrsta=""
    
    tajnopis,kljuc = transpozicijaStolpcev(toZakriptiramo)
    
    zaNalogo="Naloga za vajo: Transpozicija stolpcev"
    TL="T"
    
    return render_template("transposition.play.html", name=tajnopis, key=kljuc, cistoo= zaCistopis, tezavnost=TL, imeNaloge= zaNalogo)
    
@app.route('/TVE')
def tve():
    language= None
    texts = indices(1, language)
    idx = random.randrange(len(texts))
    
    zaCistopis= getText(texts[idx])[0]
    zaCistopis= re.sub(r'[\W0-9_]', "", zaCistopis)            #zbrise locila
    zaCistopis= zaCistopis.upper()                              #da vse v velike crke
    
    toZakriptiramo= zaCistopis.replace(" ", "")                    #to damo v funkcije za sifriranje (ne sme imeti presledkov, locil, mora biti v uppercase)       #tukaj odstranimo presledke
    toZakriptiramo= re.sub(r'[\W0-9_]', "", toZakriptiramo)          #tukaj odstranimo locila (za gvisno se 1x)
    toZakriptiramo= toZakriptiramo.upper()                            #tukaj damo v upper
    vrsta=""
    
    tajnopis,kljuc = transpozicijaVrstic(toZakriptiramo)
    
    zaNalogo="Naloga za vajo: Transpozicija vrstic"
    TL="L"
    
    return render_template("transposition.play.html", name=tajnopis, key=kljuc, cistoo= zaCistopis, tezavnost=TL, imeNaloge= zaNalogo)

@app.route('/TVH')
def tvh():
    language= None
    texts = indices(1, language)
    idx = random.randrange(len(texts))
    
    zaCistopis= getText(texts[idx])[0]
    zaCistopis= re.sub(r'[\W0-9_]', "", zaCistopis)            #zbrise locila
    zaCistopis= zaCistopis.upper()                              #da vse v velike crke
    
    toZakriptiramo= zaCistopis.replace(" ", "")                    #to damo v funkcije za sifriranje (ne sme imeti presledkov, locil, mora biti v uppercase)       #tukaj odstranimo presledke
    toZakriptiramo= re.sub(r'[\W0-9_]', "", toZakriptiramo)          #tukaj odstranimo locila (za gvisno se 1x)
    toZakriptiramo= toZakriptiramo.upper()                            #tukaj damo v upper
    vrsta=""
    
    tajnopis,kljuc = transpozicijaVrstic(toZakriptiramo)
    
    zaNalogo="Naloga za vajo: Transpozicija vrstic"
    TL="T"
    
    return render_template("transposition.play.html", name=tajnopis, key=kljuc, cistoo= zaCistopis, tezavnost=TL, imeNaloge= zaNalogo)
    
    
#tekmovanje    

@app.route('/TL')
def tl():
    language= None
    texts = indices(1, language)
    idx = random.randrange(len(texts))
    
    zaCistopis= getText(texts[idx])[0]
    zaCistopis= re.sub(r'[\W0-9_]', "", zaCistopis)            #zbrise locila
    zaCistopis= zaCistopis.upper()                              #da vse v velike crke
    
    toZakriptiramo= zaCistopis.replace(" ", "")                    #to damo v funkcije za sifriranje (ne sme imeti presledkov, locil, mora biti v uppercase)       #tukaj odstranimo presledke
    toZakriptiramo= re.sub(r'[\W0-9_]', "", toZakriptiramo)          #tukaj odstranimo locila (za gvisno se 1x)
    toZakriptiramo= toZakriptiramo.upper()                            #tukaj damo v upper
    vrsta=""
    
    izberi=random.randint(1, 3)
    if izberi ==1:
        tajnopis,kljuc = railCrypt(toZakriptiramo)
        vrsta= "Rail fence"
    if izberi ==2:
        tajnopis,kljuc = transpozicijaStolpcev(toZakriptiramo)
        vrsta= "Transpozicija stolpcev"
    elif izberi ==3:
        tajnopis,kljuc = transpozicijaVrstic(toZakriptiramo)
        vrsta= "Transpozicija vrstic"
        
    TL="Tekmovanje"
    zaNalogo="Tekmovanje: lahko"
    
    return render_template("transposition.play.html", name=tajnopis, key=kljuc, cistoo= zaCistopis, tezavnost=TL, imeNaloge= zaNalogo, vrstaa= vrsta)

@app.route('/TS')
def ts():
    language= None
    texts = indices(1, language)
    idx = random.randrange(len(texts))
    
    zaCistopis= getText(texts[idx])[0]
    zaCistopis= re.sub(r'[\W0-9_]', "", zaCistopis)            #zbrise locila
    zaCistopis= zaCistopis.upper()                              #da vse v velike crke
    
    toZakriptiramo= zaCistopis.replace(" ", "")                    #to damo v funkcije za sifriranje (ne sme imeti presledkov, locil, mora biti v uppercase)       #tukaj odstranimo presledke
    toZakriptiramo= re.sub(r'[\W0-9_]', "", toZakriptiramo)          #tukaj odstranimo locila (za gvisno se 1x)
    toZakriptiramo= toZakriptiramo.upper()                            #tukaj damo v upper
    vrsta=""
    kljuc=""
    
    izberi=random.randint(1, 3)                                     #kriptiramo prvič
    if izberi ==1:
        tajnopis,kljuc = railCrypt(toZakriptiramo)
        vrsta= "Rail fence"
    if izberi ==2:
        tajnopis,kljuc = transpozicijaStolpcev(toZakriptiramo)
        vrsta= "Transpozicija stolpcev"
    elif izberi ==3:
        tajnopis,kljuc = transpozicijaVrstic(toZakriptiramo)
        vrsta= "Transpozicija vrstic"
    
    izberi=random.randint(1, 3)                                     #kriptiramo drugič
    if izberi ==1:
        tajnopis2,kljuc2 = railCrypt(tajnopis)
        vrsta+= ", rail fence"
    if izberi ==2:
        tajnopis2,kljuc2 = transpozicijaStolpcev(tajnopis)
        vrsta+= ", transpozicija stolpcev"
    elif izberi ==3:
        tajnopis2,kljuc2 = transpozicijaVrstic(tajnopis)
        vrsta+= ", transpozicija vrstic"
    
    kljuc+="; "
    kljuc+=kljuc2
    TL="Tekmovanje"
    zaNalogo="Tekmovanje: srednje"
    
    return render_template("transposition.play.html", name=tajnopis2, key=kljuc, cistoo= zaCistopis, tezavnost=TL, imeNaloge= zaNalogo, vrstaa= vrsta)

@app.route('/TT')
def tt():
    language= None
    texts = indices(1, language)
    idx = random.randrange(len(texts))
    
    zaCistopis= getText(texts[idx])[0]
    zaCistopis= re.sub(r'[\W0-9_]', "", zaCistopis)            #zbrise locila
    zaCistopis= zaCistopis.upper()                              #da vse v velike crke
    
    toZakriptiramo= zaCistopis.replace(" ", "")                    #to damo v funkcije za sifriranje (ne sme imeti presledkov, locil, mora biti v uppercase)       #tukaj odstranimo presledke
    toZakriptiramo= re.sub(r'[\W0-9_]', "", toZakriptiramo)          #tukaj odstranimo locila (za gvisno se 1x)
    toZakriptiramo= toZakriptiramo.upper()                            #tukaj damo v upper
    vrsta=""
    kljuc=""
    
    izberi=random.randint(1, 3)                                         #kriptiramo prvič
    if izberi ==1:
        tajnopis,kljuc = railCrypt(toZakriptiramo)
        vrsta= "Rail fence"
    if izberi ==2:
        tajnopis,kljuc = transpozicijaStolpcev(toZakriptiramo)
        vrsta= "Transpozicija stolpcev"
    elif izberi ==3:
        tajnopis,kljuc = transpozicijaVrstic(toZakriptiramo)
        vrsta= "Transpozicija vrstic"
        
    izberi=random.randint(1, 3)                                         #kriptiramo drugič
    if izberi ==1:
        tajnopis2,kljuc2 = railCrypt(tajnopis)
        vrsta+= ", rail fence"
    if izberi ==2:
        tajnopis2,kljuc2 = transpozicijaStolpcev(tajnopis)
        vrsta+= ", transpozicija stolpcev"
    elif izberi ==3:
        tajnopis2,kljuc2 = transpozicijaVrstic(tajnopis)
        vrsta+= ", transpozicija vrstic"
        
    izberi=random.randint(1, 3)                                     #kriptiramo tretjič
    if izberi ==1:
        tajnopis3,kljuc3 = railCrypt(tajnopis2)
        vrsta+= ", rail fence"
    if izberi ==2:
        tajnopis3,kljuc3 = transpozicijaStolpcev(tajnopis2)
        vrsta+= ", transpozicija stolpcev"
    elif izberi ==3:
        tajnopis3,kljuc3 = transpozicijaVrstic(tajnopis2)
        vrsta+= ", transpozicija vrstic"
    
    kljuc+="; "
    kljuc+=kljuc2
    kljuc+="; "
    kljuc+=kljuc3
    
    TL="Tekmovanje"
    zaNalogo="Tekmovanje: težko"
    
    return render_template("transposition.play.html", name=tajnopis3, key=kljuc, cistoo= zaCistopis, tezavnost=TL, imeNaloge= zaNalogo, vrstaa= vrsta)
    
@app.route('/scoreboard')
def scoreboard():
    return render_template("transposition.scoreboard.html")
