
from posthog import Posthog
from datetime import datetime,timedelta
from faker import Faker
import json
import os
import gzip
import random
import uuid


# PostHog Python Client
posthog = Posthog(os.getenv('PH_PROJECT_KEY'), 
  host=os.getenv('PH_HOST'),
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

def get_random_time(last_number_of_days = 7):
    random_seconds = random.randint(0,last_number_of_days * 86400)

    random_timestamp = datetime.now() - timedelta(seconds = random_seconds)

    return(random_timestamp)

#plan_changed
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
      "$session_id": fake.uuid4()
   }
   return properties

# Get Amplitude data from folder, unzip it, and use the capture function 
def browse_and_watch_movie(number = 1):
    client_properties = get_client_properties()
    distinct_id = fake.ascii_email()
    
    for i in range(random.randint(1, number)):
        print(i)
        start_timestamp = get_random_time(last_number_of_days=7)

        capture_pageview(url='https://hogflix.net/', client_properties = client_properties,timestamp=start_timestamp, distinct_id = distinct_id)

        movie_id = random.randint(1,3)

        next_timestamp = start_timestamp + timedelta(minutes=random.randint(1,15))

        capture_pageview(url=f'https://hogflix.net/movies/{movie_id}', client_properties = client_properties, timestamp=next_timestamp, distinct_id = distinct_id)

def anon_browse_homepage_and_plans():
   client_properties = get_client_properties()
   distinct_id = fake.uuid4()
   timestamp = get_random_time(last_number_of_days=7)

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
   timestamp = get_random_time(last_number_of_days=7)

   capture_pageview(url='https://hogflix.net/', client_properties = client_properties,timestamp=timestamp, distinct_id = distinct_id)
   
   timestamp = timestamp + timedelta(minutes=random.randint(1,10))
   
   capture_pageview(url=f'https://hogflix.net/plans', client_properties = client_properties, timestamp=timestamp, distinct_id = distinct_id)

   timestamp = timestamp + timedelta(minutes=random.randint(1,10))
   
   capture_pageview(url=f'https://hogflix.net/signup', client_properties = client_properties, timestamp=timestamp, distinct_id = distinct_id)
   
   timestamp = timestamp + timedelta(minutes=random.randint(1,10))
   
   capture_event(event='plan purchased', extra_properties=client_properties, timestamp=timestamp, distinct_id=distinct_id)

browse_and_watch_movie(number = 10)
anon_browse_homepage_and_plans()
browse_plans_and_signup()