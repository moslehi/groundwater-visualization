# These scripts are to generate the HTML file that visualizes the groundwater dataset on Google maps.

import pandas as pd


# Read data 
file = "final.xlsx"
df = pd.read_excel(file)


# Creating an HTML HEADER FILE
headV="""
<!DOCTYPE html>
<html>
  <head>
  <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>groundwater-depletion</title>
    <style>
      html, body {
      height: 100%;
      margin: 0;
      padding: 0;
      }
      #map {
      height: 100%;
      }
    </style>
  </head>
  <body>
      <div id="map"></div>
    <script>
"""

tailV="""function initMap() {
      var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 4,
      center: {lat: 40.571575, lng: -106.452197}
     
      });

      markers = setMarkers(map);
      

      map.addListener('zoom_changed', function() {

    var pixelSizeAtZoom0 = 2; //the size of the icon at zoom level 0
    var maxPixelSize = 600; //restricts the maximum size of the icon, otherwise the browser will choke at higher zoom levels trying to scale an image to millions of pixels

    var zoom = map.getZoom();
    var relativePixelSize = Math.round(pixelSizeAtZoom0*Math.pow(1.6,zoom)); // use 2 to the power of current zoom to calculate relative pixel size.  Base of exponent is 2 because relative size should double every time you zoom in

    if(relativePixelSize > maxPixelSize) //restrict the maximum size of the icon
        relativePixelSize = maxPixelSize;
    //change the size of the icon
    
    for (var i = 0; i < markers.length; i++) {
    point = points[i]
       markers[i].setIcon({
                                  path: google.maps.SymbolPath.CIRCLE,
                                  fillColor: point[4],
                                  fillOpacity: 0.8,
                                  scale: relativePixelSize,
                                  strokeColor: 'white',
                                  strokeWeight: .5
                                })
      
                          
                          }
                          });
                          

} 
       function setMarkers(map) {
      // Adds markers to the map.

    
  
      var markers = []
       for (var i = 0; i < points.length; i++) {
                          var point = points[i];
                          var marker = new google.maps.Marker({
                          position: {lat: point[1], lng: point[2]},
                          map: map,
                          icon: {
                                  path: google.maps.SymbolPath.CIRCLE,
                                  fillColor: point[4],
                                  fillOpacity: 0.8,
                                  scale: 2*Math.pow(1.6,map.getZoom()),
                                  strokeColor: 'white',
                                  strokeWeight: .5
                                },
                          
                          draggable: false,
                          title: point[0],
                          zIndex: point[3]
                          });
                          markers.push(marker)
                          }
                          
                          return markers;
                          }

                          </script>

        <script async defer
            src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCR2Qp3o5fgCFd4WtF68x4j7yeSJ8oUhlY&callback=initMap"></script>

  </body>
</html>
      

""" 

# creating the data for markers on the map
s=' var points = [\n'


title=[]
for i in df['name'].tolist():
    title.append("Area Name: %s," % i)

desc=[]
for i in df['depl'].tolist():
    desc.append(" Depletion avg rate(km^3/year): %s" %i)
    
    

lat = df['lat'].tolist()
lng = df['lng'].tolist()
color_h = df['color_h'].tolist()
color_s = df['color_s'].tolist()
color_l = df['color_l'].tolist()
color=[]
for i in range(len(color_l)):
  color.append("'hsl("+str(color_h[i])+", "+str(round(color_s[i]))+"%, "+str(round(color_l[i]))+"%)'")


for i in range(0,len(lat)):
    displayTitle="%s %s" % (title[i],desc[i])
    displayTitle=displayTitle.replace('\n',' ')
    s+="['%s', %s, %s, %s, %s],\n" % (displayTitle,lat[i],lng[i],i,color[i])


s+='];'


f=open('output.html','w')
f.write(headV)
f.write(s)
f.write(tailV)
f.close()
