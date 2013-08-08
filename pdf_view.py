#!/usr/bin/env python
# -*- coding: utf-8 -*-

import model
from PIL import Image
import ImageDraw
import ImageFont
import tempfile
import os
import datetime

backgroundImage = 'res/images/background.bmp'
fonts = {   'body':'res/fonts/din.ttf',
            'body1':'res/fonts/ITC_Caslon_224_Book.ttf',
            'header':'res/fonts/ITC_Caslon_224_Black.ttf',
            'header1':'res/fonts/ITC_Caslon_224_Bold.ttf' }
sizeA4 = (2288, 3306)

# Header params:
header_xpadding = 128
header_height = 502
header_type_fontsize = 93
header_fontsize = 43

# bodyInfo params:
bodyInfo_height = 398 # + header_height => bodyStartY
bodyInfo_fontsize = 41
bodyInfo_fontsize_header = 43

# body params:
body_xpadding = 150
body_fontsize = 41

# footer params:
footer_height = 363



def _toSEK(val): return val

def _toAmount(val): return val

def _currentDate():
    now = datetime.datetime.now()
    result = str(now.year)+'-'
    month = str(now.month)
    if len(str(month)) == 1: result += '0'+str(month)+'-'
    else: result += month+'-'
    day = now.day
    if len(str(day)) == 1: result += '0'+str(day)
    else: result += day
    return result

def _drawHeader(im, pageOfPages = (1,1), date = None, headerType = 'OFFERT'):
    global header_height
    global sizeA4
    global header_xpadding
    global header_type_fontsize
    global header_fontsize
    if date == None: date = _currentDate()

    right_xpos = sizeA4[0]-header_xpadding
    _drawText(im, 'Sida '+str(pageOfPages[0])+' av '+str(pageOfPages[1]), header_fontsize, (right_xpos, 163), fonts['body1'], True)
    _drawText(im, 'Datum: '+date, header_fontsize, (right_xpos, 220), fonts['body1'], True)
    _drawText(im, headerType, header_type_fontsize, (right_xpos, 276), fonts['header'], True)

    # Seperator line
    ImageDraw.Draw(im).line((0, header_height, sizeA4[0], header_height), (0, 0, 0, 16), 1)

def _drawBodyInfo(im, infoType, data):
    if infoType == 'OFFERT': _drawBodyInfoOffert(im, data)
    elif infoType == 'FAKTURA': _drawBodyInfoFaktura(im, data)

def _drawBodyInfoOffert(im, data):
    global bodyInfo_fontsize_header
    # Collumn 1
    ystart = 580
    col1 = ['Projekt:',
            u'Vår referens:',
            u'Offerten gäller t.o.m.:',
            'Kund e-mail:',
            'Kund telefon:']
    for itm in col1:
        fname = 'body1'
        font = ImageFont.truetype(fonts[fname], bodyInfo_fontsize_header)
        size = font.getsize(itm)
        _drawText(im, itm, bodyInfo_fontsize_header, (150, ystart), fonts[fname])
        ystart += size[1]+12

    # Collumn 2
    ystart = 580
    col2 = [data['projekt'].decode('UTF-8'),
            data['ref'].decode('UTF-8'),
            data['expires'].decode('UTF-8'),
            data['email'].decode('UTF-8'),
            data['telefon'].decode('UTF-8')]
    for itm in col2:
        fname = 'body'
        font = ImageFont.truetype(fonts[fname], bodyInfo_fontsize)
        size = font.getsize(itm)
        _drawText(im, itm, bodyInfo_fontsize, (624, ystart), fonts[fname])
        ystart += size[1]+16

    # Collumn 3
    ## Kund:
    ystart = 580
    xstart = sizeA4[0] / 2 + 150

    fname = 'body1'
    font = ImageFont.truetype(fonts[fname], bodyInfo_fontsize_header)
    size = font.getsize('Kund:')
    _drawText(im, 'Kund:', bodyInfo_fontsize_header, (xstart, ystart), fonts[fname])
    ystart += size[1]+12

    ## data['kund']:
    col3 = []
    for itm in data['kund'].decode('UTF-8').split('\n'):
        col3.append(itm)
    #col3 = ['Maria Linden', u'Laxvägen 47', u'181 30 LIDINGÖ', u"äöå"]
    for itm in col3:
        fname = 'body'
        font = ImageFont.truetype(fonts[fname], bodyInfo_fontsize)
        size = font.getsize(itm)
        _drawText(im, itm, bodyInfo_fontsize, (xstart, ystart), fonts[fname])
        ystart += size[1]+16

def _drawBodyInfoFaktura(im, data):
    global bodyInfo_fontsize_header
    # Collumn 1
    ystart = 580
    col1 = [u'Er referens:',
            u'Fakt. nr / kundnr.:',
            u'Betalningsvillkor:',
            u'Förfallodatum:',
            u'Dröjsmålsränta:']
    for itm in col1:
        fname = 'body1'
        font = ImageFont.truetype(fonts[fname], bodyInfo_fontsize_header)
        size = font.getsize(itm)
        _drawText(im, itm, bodyInfo_fontsize_header, (150, ystart), fonts[fname])
        ystart += size[1]+12

    # Collumn 2
    ystart = 580
    col2 = [data['ref'].decode('UTF-8'),
            data['faktnr'].decode('UTF-8'),
            data['villkor'].decode('UTF-8'),
            data['expires'].decode('UTF-8'),
            data['prc'].decode('UTF-8')]
    col2X = 524
    for itm in col2:
        fname = 'body'
        font = ImageFont.truetype(fonts[fname], bodyInfo_fontsize)
        size = font.getsize(itm)
        _drawText(im, itm, bodyInfo_fontsize, (col2X, ystart), fonts[fname])
        ystart += size[1]+16

    # Collumn 3
    ## Kund:
    ystart = 580
    xstart = sizeA4[0] / 2 + 150

    fname = 'body1'
    font = ImageFont.truetype(fonts[fname], bodyInfo_fontsize_header)
    size = font.getsize('Kund:')
    _drawText(im, 'Kund:', bodyInfo_fontsize_header, (xstart, ystart), fonts[fname])
    ystart += size[1]+12

    ## data['kund']:
    col3 = []
    for itm in data['kund'].decode('UTF-8').split('\n'):
        col3.append(itm)
    #col3 = ['Maria Linden', u'Laxvägen 47', u'181 30 LIDINGÖ', u"äöå"]
    for itm in col3:
        fname = 'body'
        font = ImageFont.truetype(fonts[fname], bodyInfo_fontsize)
        size = font.getsize(itm)
        _drawText(im, itm, bodyInfo_fontsize, (xstart, ystart), fonts[fname])
        ystart += size[1]+16

def _drawBodyContent(im, contentType, data):
    global sizeA4
    global header_height
    global bodyInfo_height
    global body_xpadding
    contentEndPos = (sizeA4[0]-body_xpadding, header_height+bodyInfo_height)
    if contentType == 'OFFERT':
        contentEndPos = _drawBodyContentOffert(im, data, contentEndPos[1])
    return contentEndPos

def _drawBodyContentOffert(im, data, y):
    global body_xpadding
    global sizeA4
    global bodyInfo_fontsize
    xStart = body_xpadding
    yStart = y

    amountXpos = 1200
    aprisXpos = 1700


    # Begin header:
    boxHeight = 46
    draw = ImageDraw.Draw(im)
    draw.rectangle((xStart, yStart, sizeA4[0]-body_xpadding, yStart+boxHeight), (211,211,211,1), None)
    draw.line((xStart, yStart, sizeA4[0]-body_xpadding, yStart), (0,0,0,255), 1)
    height = 43
    fname = 'body1'
    font = ImageFont.truetype(fonts[fname], height)
    size = font.getsize('test')
    _drawText(im, u'Benämning', height, (xStart, yStart+3), fonts[fname])
    _drawText(im, u'mängd', height, (amountXpos, yStart+3), fonts[fname], True)
    _drawText(im, u'á-pris', height, (aprisXpos, yStart+3), fonts[fname], True)
    _drawText(im, 'summa', height, (sizeA4[0]-body_xpadding, yStart+3), fonts[fname], True)
    draw.line((body_xpadding, boxHeight+yStart, sizeA4[0]-body_xpadding, boxHeight+yStart), (0,0,0,255), 1)
    yStart += boxHeight+16

    # Data print out:
    for line in data:
        fname = 'body'
        font = ImageFont.truetype(fonts[fname], bodyInfo_fontsize)
        size = font.getsize(line)
        collumns = line.decode('UTF-8').split('\t')
        collumnsXStart =[xStart, amountXpos, aprisXpos, sizeA4[0]-body_xpadding]
        collumnsRightAlign = [False, True, True, True]
        for collumnIndex in range(0, len(collumns)):
            _drawText(im,
                     collumns[collumnIndex],
                     bodyInfo_fontsize,
                     (collumnsXStart[collumnIndex], yStart),
                     fonts[fname],
                     collumnsRightAlign[collumnIndex])
        yStart += size[1]+16

    # End line:
    draw.line((body_xpadding, yStart, sizeA4[0]-body_xpadding, yStart), (0,0,0,255), 1)

    yStart += 3

    return (sizeA4[0]-body_xpadding, yStart)

def _drawBodySummaryOffert(im, data, rightTopCorner):
    global body_fontsize
    aprisXpos = 1700
    fontSize = body_fontsize
    yStart = rightTopCorner[1]+16
    fname = 'body'
    if len(data) == 1:
        _drawText(im, data[0].decode('UTF-8'), fontSize, (sizeA4[0]-body_xpadding, yStart), fonts[fname], True)
        return
    collumnsXStart = [aprisXpos, sizeA4[0]-body_xpadding]
    counter = 0
    for line in data:
        if 'Summa inkl. moms:' in line:
            fontSize = 48
            fname = 'header1'
            font = ImageFont.truetype(fonts[fname], fontSize)
        else:
            font = ImageFont.truetype(fonts[fname], fontSize)
        size = font.getsize(line)
        for collumn in line.decode('UTF-8').split('\t'):
            counter += 1
            #print collumn + str(collumnsXStart[counter % 2])
            _drawText(im,
                     collumn,
                     fontSize,
                     (collumnsXStart[(counter % 2)-1], yStart),
                     fonts[fname],
                     True)
        yStart += size[1]+16

def _drawFooter(im):
    global sizeA4
    global footer_height
    draw = ImageDraw.Draw(im)
    draw.line((0,sizeA4[1]-footer_height,sizeA4[0],sizeA4[1]-footer_height), (0,255,0,16), 1)

def _drawText(im, text, fsize = 40, pos = (0,0), font = fonts['body'], rightAlign=False):
    font = ImageFont.truetype(font, fsize)
    size = font.getsize(text)
    #im = Image.new('RGBA', (2288, 3306), (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)
    if rightAlign:
        draw.text((pos[0]-size[0], pos[1]), text, font=font, fill='Black')
    else:
        draw.text(pos, text, font=font, fill='Black')

def _saveToPdf(im, destFile):
    tmp = tempfile.NamedTemporaryFile(suffix='.png')
    tmp.close()
    im.save(tmp.name, 'PNG')
    os.system('convert "'+tmp.name+'" "'+destFile+'"')
    os.remove(tmp.name)


def make_faktura(outPdf, date, headerData, bodyData, sumData):
    im = Image.open(open(backgroundImage))
    _drawHeader(im, pageOfPages = (1,1), date = date, headerType = 'FAKTURA')
    _drawBodyInfo(im, infoType = 'FAKTURA', data = headerData)
    end = _drawBodyContent(im, contentType='OFFERT', data=bodyData)
    _drawBodySummaryOffert(im, data=sumData, rightTopCorner=end)
    _drawFooter(im)
    _saveToPdf(im, outPdf)



def fromModel(kf = model.KundFaktura(), filename = "output.pdf"):
    im = Image.open(backgroundImage)


    #--OFFERT-----------------------
    # Header:
    _drawHeader(im, pageOfPages = (1,1), date = kf.datum.strftime("%Y-%m-%d"), headerType = 'FAKTURA')

    # Content header:
    _drawBodyInfo(im, infoType = 'FAKTURA', data = {    'ref' : kf.referens,
                                                        'faktnr' : kf.faktnr,
                                                        'villkor' : str(kf.vilkor) + ' dagar',
                                                        'expires' : kf.expires.strftime("%Y-%m-%d"),
                                                        'prc': str(kf.prc) + ' %',
                                                        'kund' : kf.kund.namn+'\n'+kf.kund.adress })

    # Main Body:
    end = _drawBodyContent(im, contentType='OFFERT', data=['',
                                                    'Renovering av lägenhet',
                                                    '',
                                                    'Arbeten enl Magnus Ståhls beskrivning\t\t\t106 900,00 kr',
                                                    '',
                                                    '',
                                                    '',
                                                    '',
                                                    '',
                                                    '',
                                                    '',
                                                    'All meterial levererades av kund.',
                                                    '',
                                                    'OBS! Summor ovan är inkl moms.',
                                                    '',
                                                    'ROT-avdrag uppgifter:',
                                                    '',
                                                    'Objekt 1: (-26 725,00 kr)',
                                                    'Fastighet: "Kantarellen 3, Lidingö"',
                                                    'Perosn 1 - 740108-0217',
                                                    'Brf orgnr 769607-7531',
                                                    '',
                                                    'Objekt 2: (-26 725,00 kr)',
                                                    'Fastighet: "Kantarellen 3, Lidingö"',
                                                    'Perosn 2 - 720225-9763',
                                                    'Brf orgnr 769607-7531',
                                                    '',
                                                    'OBS! Denna faktura avser husarbete för fastigheten "Kantarellen 3, Lidingö".',
                                                    'Enligt dig som köpare finns det möjlighet till preliminär skattereduktion på 53 450,00 kr.',
                                                    'För att vi ska kunna göra ansökan till Skatteverket, ska du betala 53 450,00 kr.',
                                                    'Om ansökan om skattereduktion avslås, ska bellopet 106 900,00 kr betalas av dig som köpare.'])


    # Summry
    _drawBodySummaryOffert(im, data=['Summa exkl. moms.:\t ' + str(kf.summaExklMoms) + " kr",
                                         'Moms (25%):\t ' + str(kf.moms) + " kr",
                                         'ROT-Avdrag:\t-' + str(kf.rotAvdrag1.summa + kf.rotAvdrag2.summa) + " kr",
                                         'Summa inkl. moms:\t ' + str(kf.summa) + " kr"], rightTopCorner=end)

    # Footer
    _drawFooter(im)
    _saveToPdf(im, "pdf/" + filename)

if __name__ == "__main__":
    fromModel()
