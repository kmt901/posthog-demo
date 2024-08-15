from posthog import Posthog
from datetime import datetime,timedelta
from faker import Faker
from argparse import ArgumentParser
import random
from argparse import ArgumentParser

days_to_generate = 30
number_of_iterations = 100

parser = ArgumentParser()
parser.add_argument("-d", "--number_of_days",
                    help="Number of days before today to generate data from",default=30, required=False)
parser.add_argument("-i", "--number_of_iterations",
                    help="Number of iterations of the data generator",default=100, required=False)
parser.add_argument("-k", "--posthog_api_key",
                    help="PostHog Project API Key", required=True)
parser.add_argument("-p", "--posthog_host",
                    help="PostHog Host", required=True)
args = parser.parse_args()

# PostHog Python Client
posthog = Posthog(args.posthog_api_key, 
  host=args.posthog_host,
  debug=True,
  historical_migration=True,
  disable_geoip=False
)

fake = Faker() 

device_properties = [
    {
       "$os": "Mac OS X",
      "$browser": "Chrome",
      "$device_type": "Desktop"
    },
    {
       "$os": "Mac OS X",
      "$browser": "Firefox",
      "$device_type": "Desktop"
    },
    {
       "$os": "Mac OS X",
      "$browser": "Safari",
      "$device_type": "Desktop"
    },{
       "$os": "Windows",
      "$browser": "Chrome",
      "$device_type": "Desktop"
    },
    {
       "$os": "Windows",
      "$browser": "Edge",
      "$device_type": "Desktop"
    },
    {
       "$os": "Windows",
      "$browser": "Firefox",
      "$device_type": "Desktop"
    },
    {
       "$os": "iOS",
      "$browser": "Mobile Safari",
      "$device_type": "Mobile"
    },
    {
       "$os": "Android",
      "$browser": "Android Mobile",
      "$device_type": "Mobile"
    }]

plans = ['Free', 'Premium', 'Max-imal']

def get_random_time():
    random_seconds = random.randint(0,args.number_of_days * 86400)

    random_timestamp = datetime.now() - timedelta(seconds = random_seconds)

    return(random_timestamp)

def capture_pageview(url, timestamp, client_properties, distinct_id):
   properties = {
      "$current_url": url,
      "$host": 'hogflix.net',
      "$pathname": url.replace('https://hogflix.net', ''),
      **client_properties
   }
   capture_event('$pageview',properties,timestamp, distinct_id)
   
   
# Convert and capture Amplitude data
def capture_event(event, extra_properties, timestamp, distinct_id):

  payload = {
    "event": event,
    "distinct_id": distinct_id,
    "properties": {
      "timestamp": timestamp,
      **extra_properties
    },
    "timestamp": timestamp
  }

  posthog.capture(
    event=payload["event"],
    distinct_id=payload["distinct_id"],
    properties=payload["properties"],
    timestamp=payload["timestamp"]
  )

def get_client_properties():
   properties= {
      **random.choice(device_properties),
      "$ip": fake.ipv4_public(),
      "$session_id": fake.uuid4(),
      "active_feature_flags": ["action_mode_on"],
      "$feature/action_mode_on": random.choice([True,False])
   }
   return properties

def browse_and_watch_movie(number = 1):
    client_properties = get_client_properties()
    client_properties = { **client_properties,
                         '$set': {
                            'plan': random.choice(plans)
                         }}
    distinct_id = fake.ascii_email()
    print(distinct_id)

    for i in range(random.randint(1, number)):
        timestamp = get_random_time()
        client_properties["$session_id"]=fake.uuid4()
        
        capture_event(event='user_logged_in', extra_properties=client_properties, timestamp=timestamp, distinct_id=distinct_id)

        timestamp = timestamp + timedelta(minutes=random.randint(1,5))

        capture_pageview(url='https://hogflix.net/', client_properties = client_properties,timestamp=timestamp, distinct_id = distinct_id)

        movie_id = random.randint(1,3)

        timestamp = timestamp + timedelta(minutes=random.randint(1,15))

        capture_pageview(url=f'https://hogflix.net/movie/{movie_id}', client_properties = client_properties, timestamp=timestamp, distinct_id = distinct_id)

def anon_browse_homepage_and_plans():
   client_properties = get_client_properties()
   distinct_id = fake.uuid4()
   print(distinct_id)

   timestamp = get_random_time()

   capture_pageview(url='https://hogflix.net/', client_properties = client_properties,timestamp=timestamp, distinct_id = distinct_id)
   
   timestamp = timestamp + timedelta(minutes=random.randint(1,10))
   
   capture_pageview(url=f'https://hogflix.net/plans', client_properties = client_properties, timestamp=timestamp, distinct_id = distinct_id)

   if random.randrange(100) < 40:
      return None

   timestamp = timestamp + timedelta(minutes=random.randint(1,10))
   
   capture_pageview(url=f'https://hogflix.net/signup', client_properties = client_properties, timestamp=timestamp, distinct_id = distinct_id)

def browse_plans_and_signup():
   client_properties = get_client_properties()
   distinct_id = fake.ascii_email()
   timestamp = get_random_time()
   print(distinct_id)
   capture_pageview(url='https://hogflix.net/', client_properties = client_properties,timestamp=timestamp, distinct_id = distinct_id)
   
   timestamp = timestamp + timedelta(minutes=random.randint(1,10))
   
   capture_pageview(url=f'https://hogflix.net/plans', client_properties = client_properties, timestamp=timestamp, distinct_id = distinct_id)

   timestamp = timestamp + timedelta(minutes=random.randint(1,10))
   
   capture_pageview(url=f'https://hogflix.net/signup', client_properties = client_properties, timestamp=timestamp, distinct_id = distinct_id)
   
   timestamp = timestamp + timedelta(minutes=random.randint(1,10))
   
   selected_plans = random.sample(plans,2)
   previous_plan = selected_plans[0]
   new_plan = selected_plans[1]
   client_properties = { **client_properties,
                        "previous_plan": previous_plan,
                        "new_plan": new_plan,
                        "$set": {
                           "plan": new_plan
                        }}
   print(client_properties)
   capture_event(event='plan_changed', extra_properties=client_properties, timestamp=timestamp, distinct_id=distinct_id)

for i in range(args.number_of_iterations):
   print(args)
   browse_and_watch_movie(number = 10)
   anon_browse_homepage_and_plans()
   browse_plans_and_signup()
   posthog.flush()