import json
from unittest.mock import patch
from src.get_random_location.app import lambda_handler


@patch('src.get_random_location.app.gmaps')
def test_lambda_handler(mock_gmaps):
    # Mock the response from Google Maps API
    mock_gmaps.streetview.return_value = 'mock_street_view_url'

    event = {}
    context = {}
    response = lambda_handler(event, context)

    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'latitude' in body
    assert 'longitude' in body
    assert 'street_view_url' in body
    assert body['street_view_url'] == 'mock_street_view_url'

# TODO: Add more comprehensive tests
