#Find out what a WMS has to offer. Service metadata:
from owslib.wms import WebMapService
wms = WebMapService('http://wms.jpl.nasa.gov/wms.cgi', version='1.1.1')
wms.identification.type
wms.identification.title

# Available layers
list(wms.contents)

# Details of a layer
wms['global_mosaic'].title

wms['global_mosaic'].queryable

wms['global_mosaic'].opaque

wms['global_mosaic'].boundingBox

wms['global_mosaic'].boundingBoxWGS84

wms['global_mosaic'].crsOptions

wms['global_mosaic'].styles

# Available methods, their URLs, and available formats
[op.name for op in wms.operations]

wms.getOperationByName('GetMap').methods

wms.getOperationByName('GetMap').formatOptions

# That’s everything needed to make a request for imagery:
img = wms.getmap(   layers=['global_mosaic'],
                    styles=['visual_bright'],
                    srs='EPSG:4326',
                    bbox=(-112, 36, -106, 41),
                    size=(300, 250),
                    format='image/jpeg',
                    transparent=True
                    )
out = open('jpl_mosaic_visb.jpg', 'wb')
out.write(img.read())
out.close()
