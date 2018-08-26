#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Created on Wed Aug 17 22:12:07 2018

http://geopython.github.io/OWSLib

@author: JaniePG

"""
from owslib.wfs import WebFeatureService

# Connect to a WFS and inspect its capabilities.
wfs20 = WebFeatureService(url='https://dservices.arcgis.com/EguFTd9xPXEoDtC7/arcgis/services/TestShareAsWebLayer_FS_WFS/WFSServer', version='2.0.0')
wfs20.identification.title
[operation.name for operation in wfs20.operations]

# List FeatureTypes
list(wfs20.contents)

# Download GML using typename, bbox and srsname
response = wfs20.getfeature(typename='TestShareAsWebLayer_FS_WFS:cities_cx',bbox=(-157.8, 22.3, -67.8, 58.3))
out=open(r'c:/temp/getFeature0.gml','wb')
out.write(bytes(response.read(),'UTF-8'))
out.close()

# Download GML using typename and filter. OWSLib currently only support filter
#  building for WFS 1.1 (FE.1.1)
from owslib.fes import *
from owslib.etree import etree
from owslib.wfs import WebFeatureService
wfs11 = WebFeatureService(url='https://serverhostds.ags.esri.com:6443/arcgis/services/mil_wfs_CA_GlobalId_VerArc2/MapServer/WFSServer', version='1.1.0')
filter = PropertyIsLike(propertyname='STATE_CITY', literal='Ingolstadt', wildCard='*')
filterxml = etree.tostring(filter.toXML()).decode("utf-8")
response = wfs11.getfeature(typename='mil_wfs_CA_GlobalId_VerArc2:CA_Cities_GlobalIDs_ArchivedVersioned', filter=filterxml)
out=open(r'c:/temp/getFeature0_filtered.gml','wb')
out.write(bytes(response.read(),'UTF-8'))
out.close()

# Download GML using StoredQueries(only available for WFS 2.0 services)
from owslib.wfs import WebFeatureService
wfs20 = WebFeatureService(url='https://serverhostds.ags.esri.com:6443/arcgis/services/mil_wfs_CA_GlobalId_VerArc2/MapServer/WFSServer', version='2.0.0')
[storedquery.id for storedquery in wfs20.storedqueries]
for parameter in wfs20.storedqueries[1].parameters
	print(parameter.name )

response = wfs20.getfeature(storedQueryID='urn:ogc:def:query:OGC-WFS::GetFeatureById', storedQueryParams={'ID':'5786CC46-E0C2-4F84-9B45-C6039C46896F'})
