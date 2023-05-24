import urllib.request
from ast import literal_eval
from geopy.distance import geodesic as GD
import numpy as np


# Calculate geodesic distance given a pair or latitute and longitude coordinates
def calculate_distance(lon_origin, lat_origin, lon_dest, lat_dest):
    origin = (lat_origin , lon_origin)
    destination = (lat_dest , lon_dest)

    calculated_distance = round(GD(origin, destination).km, 1)

    get_distance = str(calculated_distance) + " km"

    return get_distance

# Get nearby places
def get_places(longitude, latitude):

    # Grid search
    step = 0.01
    lonmin = longitude - 0.05
    lonmax = longitude + 0.05
    latmin = latitude - 0.05
    latmax = latitude + 0.05

    grid = []
    # Generate grid search
    for row in np.arange(lonmin, lonmax, step):
        for col in np.arange(latmin, latmax, step):
            grid.append([row, col])

    info_place = []
    # Iterate over the grid search to get nearby places
    for i in range(len(grid)):
        lon = grid[i][0]
        lat = grid[i][1]

        # Nominatim API
        api = "https://nominatim.openstreetmap.org/reverse?format=geojson&lat=" + str(lat) + "&lon=" + str(lon)

        try:
            # Make request to Nominatim
            contents_url = urllib.request.urlopen(api).read()
            contents_dict = literal_eval(contents_url.decode('utf-8'))

            # Properties of nearby places
            type_place = contents_dict["features"][0]["properties"]["type"]
            name_place = contents_dict["features"][0]["properties"]["name"]
            lon_place = contents_dict["features"][0]["geometry"]["coordinates"][0]
            lat_place = contents_dict["features"][0]["geometry"]["coordinates"][1]
            distance = calculate_distance(longitude, latitude, lon_place, lat_place)

            # We are interested in mall places (restaurant was not available)
            if type_place == "mall":
                info_place.append([type_place, name_place, lon_place, lat_place, distance])

        except:
            print("Unable to geocode")

    return info_place



# # Call the function (test) to get nearby places
# latitude = 20.6691008
# longitude = -103.3822989
# get_places(longitude,latitude)




