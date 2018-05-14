#!/usr/bin/env python
#coding=gb2312
from lxml import etree
import timeit

def CheckXML():
    xmlschema_doc = etree.parse("E://xml//SaturationCharacteristicsSchema.xsd")
    xmlschema = etree.XMLSchema(xmlschema_doc)
    doc = etree.parse("E://xml//test1.xml")
    
    if(xmlschema.validate(doc)):
        print('True')
    else:
        print('False')


