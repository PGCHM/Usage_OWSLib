#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Created on Wed Aug 17 22:12:07 2018

http://geopython.github.io/OWSLib

@author: JaniePG

"""
# Inspect a remote WPS and retrieve the supported processes:
from owslib.wps import WebProcessingService
wps = WebProcessingService('http://cida.usgs.gov/climate/gdp/process/WebProcessingService', verbose=False, skip_caps=True)
wps.getcapabilities()
wps.identification.type

wps.identification.title

wps.identification.abstract

for operation in wps.operations:
    operation.name

for process in wps.processes:
    process.identifier, process.title

# Determine how a specific process needs to be invoked - i.e. what are its input
# parameters, and output result:
from owslib.wps import printInputOutput
process = wps.describeprocess('gov.usgs.cida.gdp.wps.algorithm.FeatureWeightedGridStatisticsAlgorithm')
process.identifier

process.title

process.abstract

for input in process.dataInputs:
    printInputOutput(input)

# Submit a processing request (extraction of a climate index variable over a
# specific GML polygon, for a given period of time), monitor the execution
# until complete:
from owslib.wps import GMLMultiPolygonFeatureCollection
polygon = [(-102.8184, 39.5273), (-102.8184, 37.418), (-101.2363, 37.418), (-101.2363, 39.5273), (-102.8184, 39.5273)]
featureCollection = GMLMultiPolygonFeatureCollection( [polygon] )
processid = 'gov.usgs.cida.gdp.wps.algorithm.FeatureWeightedGridStatisticsAlgorithm'
inputs = [ ("FEATURE_ATTRIBUTE_NAME","the_geom"),
           ("DATASET_URI", "dods://cida.usgs.gov/qa/thredds/dodsC/derivatives/derivative-days_above_threshold.pr.ncml"),
           ("DATASET_ID", "ensemble_b1_pr-days_above_threshold"),
           ("TIME_START","2010-01-01T00:00:00.000Z"),
           ("TIME_END","2011-01-01T00:00:00.000Z"),
           ("REQUIRE_FULL_COVERAGE","false"),
           ("DELIMITER","COMMA"),
           ("STATISTICS","MEAN"),
           ("GROUP_BY","STATISTIC"),
           ("SUMMARIZE_TIMESTEP","false"),
           ("SUMMARIZE_FEATURE_ATTRIBUTE","false"),
           ("FEATURE_COLLECTION", featureCollection)
          ]
output = "OUTPUT"
execution = wps.execute(processid, inputs, output = "OUTPUT")

from owslib.wps import monitorExecution
monitorExecution(execution)

# Alternatively, define the feature through an embedded query to a WFS server:
from owslib.wps import WFSQuery, WFSFeatureCollection
wfsUrl = "http://cida.usgs.gov/climate/gdp/proxy/http://igsarm-cida-gdp2.er.usgs.gov:8082/geoserver/wfs"
query = WFSQuery("sample:CONUS_States", propertyNames=['the_geom',"STATE"], filters=["CONUS_States.508","CONUS_States.469"])
featureCollection = WFSFeatureCollection(wfsUrl, query)

# You can also submit a pre-made request encoded as WPS XML:
request = open('/Users/cinquini/Documents/workspace-cog/wps/tests/resources/wps_USGSExecuteRequest1.xml','rb').read()
execution = wps.execute(None, [], request=request)

monitorExecution(execution)
