#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date, timedelta
import time
import os
import jsonpickle

FILEPATH = '/home/karolis/Desktop/FakturaMaker/kundFaktoror/'



class KundInfo(object):
    def __init__(self):
        self.namn = 'Karolis Lukosius'
        self.adress = 'Skebokvarnsvägen 163, BV\n12452 Bandhagen\nkod:5801'
        self.telefon = '070-430 7489'
        self.email = 'karolis.lukosius@gmail.com'

class RotAvdrag(object):
    def __init__(self):
        self.summa = 50.0
        self.persnummer = '860409-4576'
        self.fastighet = 'HÖGDALEN'
        self.brf = ''

class KundFaktura(object):
    def __init__(self):
        self.datum = date(2013,12,1)
        self.referens = 'ALEX'
        self.faktnr = 'XxX-XxX'
        self.vilkor = 10
        self.expires = date(2013,9,11)
        self.prc = 24
        self.kund = KundInfo()
        self.body = [['Line one!'], [''], ['Arbete:'], ["Rivning","30","350 kr", 30*350],[''],['Material:'],['Badrums grund material','','',1600]]
        self.fakturaNotes = 'OBS! ALLA SUMMOR OVAN ÄR INKL. MOMS'
        self.rotAvdrag1 = RotAvdrag()
        self.rotAvdrag2 = RotAvdrag()

        self.omvByggmoms = False

        self.summaExklMoms = 0.0
        self.moms = 0.0
        self.summa = 0.0

    def saveToFile(self, filename):
        with open(filename, 'w') as f:
            f.write(self._toStringDict())

    def loadFromFile(self, filename):
        with open(filename, 'r') as f:
            _fromStringDict(f.read())

    def _toStringDict(self):
        return jsonpickle.encode(self)

    def _fromStringDict(self, string):
        obj = jsonpickle.decode(string)
        self.__dict__ = obj.__dict__

    def set_date(self, d):
        self.datum = d
        self.expires = d + timedelta(days = self.vilkor)

    def set_vilkor(self, d):
        self.vilkor = d
        self.expires = self.datum + timedelta(days = d)

    def add_body_line(self, columns):
        self.body.append(columns)
        self._recalcSumma()

    def _recalcSumma(self):
        itemSum = 0
        for itm in self.body:
            if len(itm) == 4:
                itemSum += itm[3]
        if not self.omvByggmoms:
            self.summaExklMoms = itemSum / 1.25
            self.moms = itemSum - itemSum / 1.25
            self.summa = itemSum - self.rotAvdrag1.summa - self.rotAvdrag2.summa
        else:
            self.summaExklMoms = itemSum
            self.moms = 0.0
            self.summa = itemSum

class KundFakturaManager(object):
    def __init__(object):
        self.faktoror = list(KundFaktura)


