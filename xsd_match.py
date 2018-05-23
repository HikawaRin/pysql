#!/usr/bin/env python
#coding=utf8
from lxml import etree
import timeit

def CheckXML():
    xmlschema_doc = etree.parse("SaturationCharacteristicsSchema.xsd")
    xmlschema = etree.XMLSchema(xmlschema_doc)
    doc = etree.parse("test1.xml")
    
    if(xmlschema.validate(doc)):
        print('True')
    else:
        print('False')


