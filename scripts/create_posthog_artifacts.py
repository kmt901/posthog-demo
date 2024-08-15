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
            "name": "Subscription Cancelled",
            "tags": ['demo'],
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
            "name": "Paid Plan Purchase",
            "tags": ['demo'],
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
            "name": "Watched a movie",
            "tags": ['demo'],
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

cohorts_ids = {}
cohorts_endpoint = '/cohorts/'
cohorts_data = [
        {
            "name": "Adult Subscribers",
            "description": "All Subscribers who are adults and thus can watch action movies",
            "filters": {
                "properties": {
                    "type": "OR",
                    "values": [
                        {
                            "type": "OR",
                            "values": [
                                {
                                    "key": "is_adult",
                                    "type": "person",
                                    "value": [
                                        "Yes"
                                    ],
                                    "negation": False,
                                    "operator": "exact"
                                }
                            ]
                        }
                    ]
                }
            }
        },
        {
            "name": "Max-imal users who watched a movie in the last 30 days",
            "description": "",
            "filters": {
                "properties": {
                    "type": "AND",
                    "values": [
                        {
                            "type": "AND",
                            "values": [
                                {
                                    "type": "behavioral",
                                    "value": "performed_event",
                                    "negation": False,
                                    "event_type": "actions",
                                    "explicit_datetime": "-30d"
                                },
                                {
                                    "key": "plan",
                                    "type": "person",
                                    "value": [
                                        "Max-imal"
                                    ],
                                    "negation": False,
                                    "operator": "exact"
                                }
                            ]
                        }
                    ]
                }
            }
        },
        {
            "name": "People who watched 5 movies recently",
            "filters": {
                "properties": {
                    "type": "OR",
                    "values": [
                        {
                            "type": "OR",
                            "values": [
                                {
                                    "type": "behavioral",
                                    "value": "performed_event_multiple",
                                    "negation": False,
                                    "operator": "gte",
                                    "event_type": "actions",
                                    "operator_value": 5,
                                    "explicit_datetime": "-30d"
                                }
                            ]
                        }
                    ]
                }
            }
        }
    ]

insights_endpoint = '/insights/'

movie_views_trend_data = {
    "name":"Movie Views by Plan Type",
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
 "saved": True,
 "tags": ["demo"]
}

purchase_funnel_data = {
    "name": "Paid plan purchase funnel",
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
"saved": True,
 "tags": ["demo"]
}

movie_retention_data = {
    "name": "Weekly Movie Watch Retention",
    "query":{
  "kind": "InsightVizNode",
  "source": {
    "kind": "RetentionQuery",
    "retentionFilter": {
      "retentionType": "retention_first_time",
      "totalIntervals": 5,
      "returningEntity": {
        "id": 42493,
        "name": "Watched a movie (Test)",
        "type": "actions",
        "order": 0,
        "uuid": "fafa227f-4eed-4dd6-b007-63f748129444"
      },
      "targetEntity": {
        "id": 42493,
        "name": "Watched a movie (Test)",
        "type": "actions",
        "order": 0,
        "uuid": "7a9325b9-85df-44d7-a06e-b62cec8e7bb9"
      },
      "period": "Week"
    }
  },
  "full": True
},
"saved": True,
 "tags": ["demo"]
}

path_data = {
    "name": "Where do people go after visiting the homepage",
    "query": {
  "kind": "InsightVizNode",
  "source": {
    "kind": "PathsQuery",
    "pathsFilter": {
      "includeEventTypes": [
        "$pageview"
      ],
      "pathGroupings": [
        "/movie/*"
      ]
    }
  },
  "full": True
},
"saved": True,
 "tags": ["demo"]
}

feature_flag_endpoint = '/feature_flags/'
feature_flag_data = {
            "name": "Turns Hogflix from family friendly to action movies.",
            "key": "action_mode_on",
            "tags": ["demo"],
            "filters": {
                "groups": [
                    {
                        "variant": None,
                        "properties": [
                            {
                                "key": "id",
                                "type": "cohort",
                            }
                        ],
                        "rollout_percentage": 100
                    }
                ],
                "payloads": {},
                "multivariate": None
            }
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

cohorts_data[1]['filters']['properties']['values'][0]['values'][0]['key'] =  actions_ids.get('Watched a movie')
cohorts_data[2]['filters']['properties']['values'][0]['values'][0]['key'] =  actions_ids.get('Watched a movie')

for data in cohorts_data:
    response = make_posthog_api_request(cohorts_endpoint, data)
    cohorts_ids[data['name']] = response['id']

movie_views_trend_data['query']['source']['series'][0]['id'] = actions_ids.get('Watched a movie')
response = make_posthog_api_request(insights_endpoint, movie_views_trend_data)

purchase_funnel_data['query']['source']['series'][3]['id'] = actions_ids.get('Paid Plan Purchase')
response = make_posthog_api_request(insights_endpoint, purchase_funnel_data)

movie_retention_data['query']['source']['retentionFilter']['targetEntity']['id'] = actions_ids.get('Watched a movie')
movie_retention_data['query']['source']['retentionFilter']['returningEntity']['id'] = actions_ids.get('Watched a movie')

response = make_posthog_api_request(insights_endpoint, movie_retention_data)

response = make_posthog_api_request(insights_endpoint, path_data)

feature_flag_data['filters']['groups'][0]['properties'][0]['value'] = cohorts_ids.get('Adult Subscribers')

response = make_posthog_api_request(feature_flag_endpoint, feature_flag_data)


