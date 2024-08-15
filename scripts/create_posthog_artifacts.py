import requests
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-k", "--personal_api_key",
                    help="PostHog Personal API Key", required=True)
parser.add_argument("-p", "--posthog_api_base_url",
                    help="PostHog API Host", required=True)
args = parser.parse_args()

# The URL to which you want to send the POST request
url = args.posthog_api_base_url

# The Bearer token for authentication
token = args.personal_api_key

# Headers including the Bearer token for authorization
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# The JSON payload to be sent in the POST request
actions_ids = {}
actions_endpoint = '/actions/'
actions_data = [
        {
            "name": "Subscription Cancelled (Test)",
            "steps": [
                {
                    "event": "plan_changed",
                    "properties": [
                        {
                            "key": "new_plan",
                            "type": "event",
                            "value": [
                                "Free"
                            ],
                            "operator": "exact"
                        }
                    ]
                }
            ]
        },
        {
            "name": "Paid Plan Purchase (Test)",
            "steps": [
                {
                    "event": "plan_changed",
                    "properties": [
                        {
                            "key": "new_plan",
                            "type": "event",
                            "value": [
                                "Premium",
                                "Max-imal"
                            ],
                            "operator": "exact"
                        }
                    ]
                }
            ]
        },
        {
            "name": "Watched a movie (Test)",
            "description": "Watched a movie",
            "steps": [
                {
                    "event": "$pageview",
                    "url": "movie/",
                    "url_matching": "contains"
                }
            ]
        }
    ]

insights_endpoint = '/insights/'

movie_views_trend_data = {
    "name":"Movie Views by Plan Type 2.0",
     "query": {
  "kind": "InsightVizNode",
  "source": {
    "kind": "TrendsQuery",
    "properties": {
      "type": "AND",
      "values": [
        {
          "type": "AND",
          "values": [
            {
              "key": "plan",
              "type": "person",
              "value": "is_set",
              "operator": "is_set"
            }
          ]
        }
      ]
    },
    "dateRange": {
      "date_to": None,
      "date_from": "-30d"
    },
    "series": [
      {
        "kind": "ActionsNode",
        "math": "total"
      }
    ],
    "interval": "week",
    "breakdownFilter": {
      "breakdowns": [
        {
          "type": "person",
          "property": "plan"
        }
      ]
    },
    "trendsFilter": {
      "display": "ActionsLineGraph"
    }
  },
  "full": True
},
 "saved": True
}

purchase_funnel_data = {
    "name": "Paid plan purchase funnel 2.0",
    "query": {
  "kind": "InsightVizNode",
  "source": {
    "kind": "FunnelsQuery",
    "dateRange": {
      "date_from": "-30d"
    },
    "series": [
      {
        "kind": "EventsNode",
        "event": "$pageview",
        "name": "$pageview",
        "custom_name": "Home Page",
        "properties": [
          {
            "key": "$pathname",
            "type": "event",
            "value": [
              "/"
            ],
            "operator": "exact"
          }
        ]
      },
      {
        "kind": "EventsNode",
        "event": "$pageview",
        "name": "$pageview",
        "custom_name": "Plans Page",
        "properties": [
          {
            "key": "$pathname",
            "type": "event",
            "value": [
              "/plans"
            ],
            "operator": "exact"
          }
        ]
      },
      {
        "kind": "EventsNode",
        "event": "$pageview",
        "name": "$pageview",
        "custom_name": "Signup Page",
        "properties": [
          {
            "key": "$pathname",
            "type": "event",
            "value": [
              "/signup"
            ],
            "operator": "exact"
          }
        ]
      },
      {
        "kind": "ActionsNode",
        "name": "Paid Plan Purchase"
      }
    ],
    "funnelsFilter": {
      "funnelVizType": "steps"
    }
  },
  "full": True
},
"saved": True
}

def make_posthog_api_request(endpoint, data):
    response = requests.post(url + endpoint, headers=headers, json=data)
    # Checking the status code and response
    if response.status_code == 201:
        print("Request was successful!")
        print("Response:", response.json())  # Assuming the response is JSON
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Response:", response.text)
    return response.json()

# Making the POST request

for data in actions_data:
    response = make_posthog_api_request(actions_endpoint, data)
    actions_ids[data['name']] = response['id']

movie_views_trend_data['query']['source']['series'][0]['id'] = actions_ids.get('Watched a movie (Test)')
response = make_posthog_api_request(insights_endpoint, movie_views_trend_data)

purchase_funnel_data['query']['source']['series'][3]['id'] = actions_ids.get('Paid Plan Purchase (Test)')
response = make_posthog_api_request(insights_endpoint, purchase_funnel_data)

