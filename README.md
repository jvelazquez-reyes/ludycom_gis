# GIS web app in Django

## Run the project locally
To run the whole project locally, clone this repo:
```bash
git clone https://github.com/jvelazquez-reyes/ludycom_gis.git
```

In the local folder where you cloned the project, install the required packages from `requirements.txt` (in a virtual environment preferably)

```bash
pip install -r requirements.txt
```

Once you have all installed, set up the django project.

Run the `makemigrations` and `migrate` command to create the models and the SQL tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

To run the server:

```bash
python manage.py runserver
```

Go to the address `http://127.0.0.1:8000/` to interact with the app.


## Project features
- Register new user
- Login user
- If the user is authenticated:
  - The user can `POST` a new search of places ('mall') that are close to a given `latitude` and `longitude`.
  - This [file](https://github.com/jvelazquez-reyes/ludycom_gis/blob/main/geoapp/geolocalizer.py) contains the algorithm to locate nearby places:
    - Given the set of `latitude` and `longitude` coordinates, a grid search is generated.
    - The grid search contains pairs of `latitude - longitude` coordinates around the `latitude - longitude` pair that the user introduced manually.
    - For every coordinate pair in the grid search, a [Nominatim API](https://nominatim.org/release-docs/develop/api/Reverse/) is fetched to get a dictionary of nearby places.
    - This is an example of a fetched dictionary: `{"type":"FeatureCollection","licence":"Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright","features":[{"type":"Feature","properties":{"place_id":211857455,"osm_type":"way","osm_id":479407893,"place_rank":30,"category":"amenity","type":"place_of_worship","importance":0,"addresstype":"amenity","name":"Parroquia Madre del Redentor","display_name":"Parroquia Madre del Redentor, Calle Beira, Autocinema, Guadalajara, Jalisco, 44230, México","address":{"amenity":"Parroquia Madre del Redentor","road":"Calle Beira","neighbourhood":"Autocinema","city":"Guadalajara","state":"Jalisco","ISO3166-2-lvl4":"MX-JAL","postcode":"44230","country":"México","country_code":"mx"}},"bbox":[-103.3428644,20.7189696,-103.3424754,20.719223],"geometry":{"type":"Point","coordinates":[-103.34266219981436,20.7191026]}}]}`
    - From the dictionary, the `name`, `type` values are indexed to store them in the database.
  - The user can get the search history with the details of the nearby place found.
  - In addition, the distance between the place found and the original coordinates is calculated. This calculation is performed using the `geodesic` function from the `geopy` package.
- Logout user
