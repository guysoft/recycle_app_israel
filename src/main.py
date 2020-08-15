from kivy_garden.mapview import MapView, MapMarker
from kivy_garden.mapview.clustered_marker_layer import ClusteredMarkerLayer
from kivy.app import App
import json
from urllib.request import urlopen
import ssl
from plyer import gps
from kivy.utils import platform
try:
    import android
except ModuleNotFoundError:
    android = None



def get_geo_data():
    link = "https://mai.org.il/weee_map_israel/"

    f = urlopen(link,  context=ssl._create_unverified_context())
    data = f.read().decode()

    # If you want to try a cache, uncomment this
    # with open("page.html") as f:
    #     data = f.read()

    data_1 = data.split('var map1 = $("#map1").maps(')[1]

    data_2 = data_1.split(').data("wpg')[0]

    json_data = json.loads(data_2)
    return json_data
    

def request_android_permissions():
    """
    Since API 23, Android requires permission to be requested at runtime.
    This function requests permission and handles the response via a
    callback.
    The request will produce a popup if permissions have not already been
    been granted, otherwise it will do nothing.
    """
    from android.permissions import request_permissions, Permission

    def callback(permissions, results):
        """
        Defines the callback to be fired when runtime permission
        has been granted or denied. This is not strictly required,
        but added for the sake of completeness.
        """
        if all([res for res in results]):
            print("callback. All permissions granted.")
        else:
            print("callback. Some permissions refused.")

        request_permissions([Permission.ACCESS_COARSE_LOCATION,
                                Permission.ACCESS_FINE_LOCATION], callback)
    # # To request permissions without a callback, do:
    # request_permissions([Permission.ACCESS_COARSE_LOCATION,
    #                      Permission.ACCESS_FINE_LOCATION])


class mapviewApp(App):
    
    def storeLocation(self, **kwargs):
        locationData = kwargs
        print("WEEEE")
        print(locationData)
        gps.stop()
        
        self.mapview.center_on(locationData["lat"], locationData["lon"])
        return locationData


    def getLocation(self):
        gps.configure(on_location=self.storeLocation)
        gps.start(minTime=1000, minDistance=1)
    
    
    def build(self):
        layer = ClusteredMarkerLayer()
        
        a = MapMarker()
        # self.mapview.add_marker(, cls=MapMarker)
        layer.add_marker(lon=32.092, lat=34.807, cls=MapMarker)
        
        self.mapview = MapView(zoom=15, lat=32.092, lon=34.807)
        self.mapview.map_source.min_zoom = 14
        # self.mapview.add_widget(layer)
        
        data = get_geo_data()
        
        places = data["places"]

        for place in places:
            if place["categories"][0]["id"] == "45":
                pin_color = "data/pin-red.png"
                
            else:
                pin_color = "data/pin-blue.png"
            marker = MapMarker(lat=float(place["location"]["lat"]), lon=float(place["location"]["lng"]),source=pin_color)
            # layer.add_marker(marker)
            self.mapview.add_marker(marker)
            
        
        if platform == "android":
            print("gps.py: Android detected. Requesting permissions")
            request_android_permissions()

        
        try:
            print(self.getLocation())
        except NotImplementedError:
            print("location not NotImplemented")

        return self.mapview

mapviewApp().run()
