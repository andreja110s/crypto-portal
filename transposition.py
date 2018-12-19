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
import sys

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
@app.route("/scoreboard/insert", methods=['POST'])
def scoreboard_insert():
    name = request.form['ime'].encode('UTF-8')
    difficulty = request.form['difficulty']
    st_namigov = request.form['st_namigov']
    st_zmot = request.form['st_zmot']
    st_tock = request.form['st_tock']
    prb_cs = request.form['prb_cs']
    cs_ura = request.form['cs_ura']
    
    db = database.dbcon()
    cur = db.cursor()
    
    #vpisemo povprecje
    #lhk = 'SELECT st_namigov FROM crypto_transposition where difficulty=%s;'
    #cur.execute(lhk, (difficulty, ))
    #records1 = cur.fetchall()
    #posodobi = 'UPDATE crypto_transposition SET st_namigov=%s where difficulty=%s and id<80'
    #cur.execute(posodobi, (povp, difficulty))
    
    #print("Ime: "+str(name)+", težavnost: "+str(difficulty)+", namigi: "+str(st_namigov)+", zmote: "+str(st_zmot)+", tocke "+str(st_tock), file=sys.stdout)
    query = 'INSERT INTO `crypto_transposition` (name, difficulty, st_namigov, st_zmot, prb_cs, cs_ura, st_tock) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    cur.execute(query, (name, difficulty, st_namigov, st_zmot, prb_cs, cs_ura, st_tock))
    db.commit()
    cur.close()
    return redirect('transposition/scoreboard/lahko')


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
    tt="lahko"
    zaNalogo="Tekmovanje: lahko"
    
    #vzamemo povprecja za prikaz
    db = database.dbcon()
    cur = db.cursor()
    nnamigov = 'SELECT AVG(st_namigov) FROM crypto_transposition where difficulty="lahko" and id>80;'
    cur.execute(nnamigov)
    records1 = int(cur.fetchall()[0][0])
    
    zzmot = 'SELECT AVG(st_zmot) FROM crypto_transposition where difficulty="lahko" and id>80;'
    cur.execute(zzmot)
    records2 = int(cur.fetchall()[0][0])
    
    ccasa = 'SELECT AVG(prb_cs) FROM crypto_transposition where difficulty="lahko" and id>80;'
    cur.execute(ccasa)
    records3 = int(cur.fetchall()[0][0])
    
    cur.close()
    
    return render_template("transposition.play.html", name=tajnopis, key=kljuc, cistoo= zaCistopis, tezavnost=TL, imeNaloge= zaNalogo, vrstaa= vrsta, tt=tt, nnamigov=records1, zzmot=records2, ccasa=records3)

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
    tt="srednje"
    zaNalogo="Tekmovanje: srednje"
    
    #vzamemo povprecja za prikaz
    db = database.dbcon()
    cur = db.cursor()
    nnamigov = 'SELECT AVG(st_namigov) FROM crypto_transposition where difficulty="srednje" and id>80;'
    cur.execute(nnamigov)
    v=cur.fetchall()[0][0]
    records1 = int(v)
    
    zzmot = 'SELECT AVG(st_zmot) FROM crypto_transposition where difficulty="srednje" and id>80;'
    cur.execute(zzmot)
    v=cur.fetchall()[0][0]
    records2 = int(v)
    
    ccasa = 'SELECT AVG(prb_cs) FROM crypto_transposition where difficulty="srednje" and id>80;'
    cur.execute(ccasa)
    v=cur.fetchall()[0][0]
    records3 = int(v)
    
    cur.close()
    
    
    return render_template("transposition.play.html", name=tajnopis2, key=kljuc, cistoo= zaCistopis, tezavnost=TL, imeNaloge= zaNalogo, vrstaa= vrsta, tt=tt)

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
    tt="tezko"
    
    #vzamemo povprecja za prikaz
    db = database.dbcon()
    cur = db.cursor()
    nnamigov = 'SELECT AVG(st_namigov) FROM crypto_transposition where difficulty="tezko" and id>80;'
    cur.execute(nnamigov)
    records1 = int(cur.fetchall()[0][0])
    
    zzmot = 'SELECT AVG(st_zmot) FROM crypto_transposition where difficulty="tezko" and id>80;'
    cur.execute(zzmot)
    records2 = int(cur.fetchall()[0][0])
    
    ccasa = 'SELECT AVG(prb_cs) FROM crypto_transposition where difficulty="tezko" and id>80;'
    cur.execute(ccasa)
    records3 = int(cur.fetchall()[0][0])
    
    cur.close()
    
    return render_template("transposition.play.html", name=tajnopis3, key=kljuc, cistoo= zaCistopis, tezavnost=TL, imeNaloge= zaNalogo, vrstaa= vrsta, tt=tt)
    
#@app.route('/scoreboard')
#def scoreboard():
#    return render_template("transposition.scoreboard.html")
    
@app.route("/scoreboard/<difficulty>")
def scoreboard(difficulty):
    db = database.dbcon()
    cur = db.cursor()
    table = 'SELECT * FROM crypto_transposition where difficulty=%s and id>80 ORDER BY st_tock DESC;'
    cur.execute(table, (difficulty, ))
    records = cur.fetchall()
    
    #uporabniki=np.array([])
    
    #for row in records:
        #if row[2] == difficulty:
        #    uporabniki=np.concatenate([uporabniki, [row[0]]])
        #print(row[1])
    cur.close();
    
    #print (uporabniki)
    
    tez=difficulty;
    
    if difficulty == 'tezko':
        tez="težko"
    
    return render_template("transposition.scoreboard.html", users=records, tez=tez)