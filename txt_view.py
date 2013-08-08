#!/usr/bin/env python
# -*- coding: utf-8 -*-
import model


def main():
    kf = model.KundFaktura()
    kf.referens = "SUPER LONG REFERENS"
    kf.rotAvdrag1.persnummer = '1'
    kf.rotAvdrag2.persnummer = '2'
    kf.rotAvdrag1.brf = "565655-2525"
    kf.rotAvdrag2.brf = "565655-2525"
    kf._recalcSumma()

    print "="*80
    print " "*35+"FAKTURA"+" "*27+kf.datum.strftime("%Y-%m-%d")
    print ""
    print "Referns:          %-28s Kund:" % ( kf.referens )
    print "Faktura nr.:      %-28s %s"    % ( kf.faktnr, kf.kund.namn )
    print "Betalningsvilkor: %-28s %s"    % ( (str(kf.vilkor)+" dagar"), kf.kund.adress.splitlines()[0] )
    print "Förfallodatum:    %-28s %s"    % ( kf.expires.strftime("%Y-%m-%d"), kf.kund.adress.splitlines()[1] )
    print "prc:              %-28s "      % ( str(kf.prc) )
    print "-"*80
    print "%-36s %-15s %-20s %s" % ( "Benanming", "mangd", "a-pris", "summa" )
    print "-"*80

    for itm in kf.body:
        string = "%-36s" % itm[0]
        if len(itm) == 4:
            string += "%-15s" % str(itm[1])
            string += "%-20s" % str(itm[2])
            string += str(itm[3]) + " kr"
        print string
    print ""
    print ""
    print kf.fakturaNotes
    print "-"*80

    if not kf.rotAvdrag1.persnummer == '':
        print "%-34s" % ( "Person 1: " ) + "( " +str(kf.rotAvdrag1.summa) + " )"
        print "%-34s" % ( "pers.nr.: " ) + kf.rotAvdrag1.persnummer
        print "%-34s" % ( "fastighet: " ) + kf.rotAvdrag1.fastighet
        if not kf.rotAvdrag1.brf == "":
            print "%-34s" % ( "Bostadsrättsföreningens org.nr.: " ) + kf.rotAvdrag1.brf
        print ""

    if not kf.rotAvdrag1.persnummer == '':
        print "%-34s" % ( "Person 2: " ) + "( " +str(kf.rotAvdrag2.summa) + " )"
        print "%-34s" % ( "pers.nr.: " ) + kf.rotAvdrag2.persnummer
        print "%-34s" % ( "fastighet: " ) + kf.rotAvdrag2.fastighet
        if not kf.rotAvdrag1.brf == "":
            print "%-34s" % ( "Bostadsrättsföreningens org.nr.: " ) + kf.rotAvdrag2.brf
        print ""

    print "-"*80
    print " "*40 + "%-20s" % ( "Summa exkl. moms: " )+ str(kf.summaExklMoms) + " kr"
    print " "*40 + "%-20s" % ( "Moms: " ) + str(kf.moms) + " kr"
    if not kf.rotAvdrag1.persnummer == '':
        print " "*40 + "%-20s" % ( "ROT-Avdrag: " ) + "-" + str(kf.rotAvdrag1.summa + kf.rotAvdrag2.summa) + " kr"
    print " "*40 + "%-20s" % ( "Summa att betala: " )+ str(kf.summa) + " kr"
    print "="*80
if __name__ == '__main__':
    main()
