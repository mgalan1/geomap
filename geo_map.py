import folium, tkinter, csv

from tkinter import filedialog
from geopy.geocoders import Nominatim
from folium.plugins import MarkerCluster


class Node:
    # Describes a node (marker) with a person's name and coordinates
    def __init__(self, lat, long, name):
        self._lat = lat
        self._long = long
        self._name = name
    def lat(self):
        return self._lat
    def long(self):
        return self._long
    def name(self):
        return self._name
    def __str__(self):
        return str(self._name) + ' : ' + str(self._lat) + ',' + str(self._long)


def process_in():
    # Locates file in directory
    window = tkinter.Tk()
    window.withdraw()
    in_file = tkinter.filedialog.askopenfilename()

    # Opens file
    try:
        op_file = open(in_file)
    except IOError:
        print("Could not open file " + in_file)
        exit(1)
    
    center_lat = 0
    center_long = 0
    coord_lis = []
    
    # Geocoder from OpenStreetMap
    geolocate = Nominatim(user_agent= "YOUR EMAIL HERE")

    # Split name and location
    for line in op_file:
        data_list = []
        for char in line:
            if char == '"':
                data_list.append('')
            else:
                data_list.append(char)
        new_data = ''.join(data_list)
        sep = new_data.find(',')
        name = new_data[:sep]
        location = new_data[sep+1:]

        # Establishes latitude and longitude for location in file
        coord = geolocate.geocode(location, timeout = 10)

        # If the location exists, implement a Node object to be stored in a list
        if coord != None:
            lat = coord.latitude
            long = coord.longitude
            center_lat += int(lat)
            center_long += int(long)
            each_node = Node(lat, long, name)
            coord_lis.append(each_node)
        else:
            print("Could not find location " + location)

    # Take average latitude and longitude for all locations in file
    avg_lat = (center_lat / len(coord_lis))
    avg_long = (center_long / len(coord_lis))
    
    op_file.close()
    
    return coord_lis, avg_lat, avg_long
        
        
def basemap(coord_lis, avg_lat, avg_long):
    # Initialize a base map with the starting point as the average latitude,
    # longitude pair calculated for all locations in file
    base = folium.Map(location = [avg_lat, avg_long], tiles = 'cartodbpositron',
                      zoom_start = 2)

    # Create a cluster of markers within range of each other
    clust = MarkerCluster().add_to(base)

    # For each Node object, create a circle marker with the person's name as
    # a popup
    for i in range(len(coord_lis)):
        folium.CircleMarker(location = [coord_lis[i].lat(),
                                        coord_lis[i].long()],
                            popup = coord_lis[i].name()).add_to(clust)
        
    # Give the user the option to save the map as an html file
    output = input('Output file name: ')
    base.save(output)


def main():
    coord_lis, avg_lat, avg_long = process_in()
    basemap(coord_lis, avg_lat, avg_long)
    


main()
    
    
    
