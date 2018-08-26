#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Created on Wed Aug 17 22:12:07 2018

http://geopython.github.io/OWSLib

@author: JaniePG

"""
#Connect to a CSW, and inspect its properties:
from owslib.csw import CatalogueServiceWeb
csw = CatalogueServiceWeb('http://geodiscover.cgdi.ca/wes/serviceManagerCSW/csw')
csw.identification.type
[op.name for op in csw.operations]

# Get supported resultType’s:
csw.getdomain('GetRecords.resultType')
csw.results

# Search for bird data:
from owslib.fes import PropertyIsEqualTo, PropertyIsLike, BBox
birds_query = PropertyIsEqualTo('csw:AnyText', 'birds')
csw.getrecords2(constraints=[birds_query], maxrecords=20)
csw.results
for rec in csw.records:
    print(csw.records[rec].title)

# Search for bird data in Canada
bbox_query = BBox([-141,42,-52,84])

csw.getrecords2(constraints=[birds_query, bbox_query])

csw.results

# Search for keywords like ‘birds’ or ‘fowl’
birds_query_like = PropertyIsLike('dc:subject', '%birds%')
fowl_query_like = PropertyIsLike('dc:subject', '%fowl%')
csw.getrecords2(constraints=[birds_query_like, fowl_query_like])
csw.results

# Search for a specific record:
csw.getrecordbyid(id=['9250AA67-F3AC-6C12-0CB9-0662231AA181'])
c.records['9250AA67-F3AC-6C12-0CB9-0662231AA181'].title

# Search with a CQL query

csw.getrecords(cql='csw:AnyText like "%birds%"')

csw.transaction(ttype='insert', typename='gmd:MD_Metadata', record=open("file.xml").read())

# update ALL records
csw.transaction(ttype='update', typename='csw:Record', propertyname='dc:title', propertyvalue='New Title')
# update records satisfying keywords filter
csw.transaction(ttype='update', typename='csw:Record', propertyname='dc:title', propertyvalue='New Title', keywords=['birds','fowl'])
# update records satisfying BBOX filter
csw.transaction(ttype='update', typename='csw:Record', propertyname='dc:title', propertyvalue='New Title', bbox=[-141,42,-52,84])

# delete ALL records
csw.transaction(ttype='delete', typename='gmd:MD_Metadata')
# delete records satisfying keywords filter
csw.transaction(ttype='delete', typename='gmd:MD_Metadata', keywords=['birds','fowl'])
# delete records satisfying BBOX filter
csw.transaction(ttype='delete', typename='gmd:MD_Metadata', bbox=[-141,42,-52,84])

# Harvest a resource
csw.harvest('http://host/url.xml', 'http://www.isotc211.org/2005/gmd')
