import requests
import pprint

res = requests.post(
    # url='https://taken-model.herokuapp.com/predict',
    url='http://localhost:5000/predict',
    json=[
            {
                'order_id': 143648070,
                'store_id': 30000009,
                'to_user_distance': 29.4781006757058885,
                'to_user_elevation': 872.71936035156295,
                'total_earning': 4300,
                'created_at': '2017-12-09T20:02:17Z',
            },
            {
                'order_id': 36780258,
                'store_id': 900014452,
                'to_user_distance': 2.6714317179354317,
                'to_user_elevation': 1.72265625,
                'total_earning': 5400,
                'created_at': '2017-09-07T20:15:19Z',
            }
        ]
)

pprint.pprint(res.json())
