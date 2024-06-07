import json
import random
import os
from googlemaps import Client as GoogleMaps
import logging

# Initialize Google Maps client
gmaps = GoogleMaps(key=os.getenv('GOOGLE_MAPS_API_KEY'))


def lambda_handler(event, context):
    # Tokyo's geographical boundaries
    min_lat, max_lat = 35.60, 35.80
    min_lng, max_lng = 139.55, 139.85

    # Generate random coordinates within Tokyo
    latitude = random.uniform(min_lat, max_lat)
    longitude = random.uniform(min_lng, max_lng)

    # Get a Street View image URL
    street_view_url = gmaps.streetview(location=(latitude, longitude), size=(
        600, 400), key=os.getenv('GOOGLE_MAPS_API_KEY'))

    logging.info(f"Generated coordinates: latitude={
                 latitude}, longitude={longitude}")

    return {
        'statusCode': 200,
        'body': json.dumps({
            'latitude': latitude,
            'longitude': longitude,
            'street_view_url': street_view_url
        })
    }

# TODO: Add error handling and logging
