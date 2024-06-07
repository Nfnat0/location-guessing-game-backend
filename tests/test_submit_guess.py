import json
from unittest.mock import patch
from src.submit_guess.app import lambda_handler


@patch('src.submit_guess.app.gmaps')
@patch('src.submit_guess.app.boto3.resource')
def test_lambda_handler(mock_dynamodb, mock_gmaps):
    # Mock the response from Google Maps API
    mock_gmaps.distance_matrix.return_value = {
        'rows': [{
            'elements': [{
                'distance': {
                    'value': 5000  # 5 km
                }
            }]
        }]
    }

    # Mock DynamoDB table
    mock_table = mock_dynamodb.return_value.Table.return_value
    mock_table.put_item.return_value = {}

    event = {
        'body': json.dumps({
            'actual_lat': 35.6895,
            'actual_lng': 139.6917,
            'guessed_lat': 35.6890,
            'guessed_lng': 139.6920,
            'player_id': 'player1'
        })
    }
    context = {}
    response = lambda_handler(event, context)

    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'distance' in body
    assert body['distance'] == 5000  # 5 km
    assert 'score' in body
    assert body['score'] == 500  # 1000 - (5000 / 10)

    # Ensure DynamoDB put_item was called
    mock_table.put_item.assert_called_once_with(Item={
        'player_id': 'player1',
        'score': 500,
        'distance': 5000
    })

# TODO: Add more comprehensive tests
