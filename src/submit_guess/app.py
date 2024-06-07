import json
import os
from googlemaps import Client as GoogleMaps
import boto3
import logging

# Initialize Google Maps client
gmaps = GoogleMaps(key=os.getenv('GOOGLE_MAPS_API_KEY'))


def lambda_handler(event, context):
    body = json.loads(event['body'])
    actual_lat = body['actual_lat']
    actual_lng = body['actual_lng']
    guessed_lat = body['guessed_lat']
    guessed_lng = body['guessed_lng']

    # Calculate the distance
    distance = gmaps.distance_matrix((actual_lat, actual_lng), (guessed_lat, guessed_lng))[
        'rows'][0]['elements'][0]['distance']['value']

    # Calculate the score based on distance
    score = max(0, 1000 - distance / 10)

    # Update score in DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PlayerScores')
    table.put_item(Item={
        'player_id': body['player_id'],
        'score': score,
        'distance': distance
    })

    logging.info(f"Player ID: {body['player_id']}, Distance: {
                 distance}, Score: {score}")

    return {
        'statusCode': 200,
        'body': json.dumps({
            'distance': distance,
            'score': score
        })
    }

# TODO: Add error handling and logging
