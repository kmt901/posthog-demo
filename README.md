# HogFlix Demo 3000

This repository allows you to spin up a demo app which has been instrumented with PostHog, and seed PostHog historic data and artifacts to provide a full-featured demo environment showcasing all features.

## Prerequisites

To run the demo app on a Mac you'll need to set up Python 3 locally:

1. Install Xcode Command Line Tools if you haven't already: `xcode-select --install`.
2. Install the package manager Homebrew by following the [instructions here](https://brew.sh/).

After installation, make sure to follow the instructions printed in your terminal to add Homebrew to your $PATH. Otherwise the command line will not know about packages installed with brew.

3. Install Python: `brew install python`.
4. Upgrade pip to the latest version: `pip install -U pip`
5. From the root of this repository, install the requirements: `pip install -r requirements.txt`

## Running the app

There are two ways to run the app - locally using Python or via Docker.  When we've found a place to store the built container image Docker will be easier, but for now just use the Python approach.

### Option 1 - run locally with Python

Before running the app for the first time you'll need to create and seed the local Sqlite database:

```
python pop_db.py
python dummy_data.py
```

This only needs to be done the first time you run the app.

Next you'll need to set your PostHog Host and Project API key (available on the settings page) as Environment Variables:

```
export PH_HOST='https://<eu or us>.i.posthog.com'
export PH_PROJECT_KEY='<Project API key>'
```

Finally, run the app:

```
python app.py
```

If you open up a browser and head to http://127.0.0.1:5000/ you'll see the HogFlix app running.  Use Ctrl + C in your terminal to stop the app.

### Option 2 - run as a container with Docker

The container hasn't been pushed to a registry yet so you'll need to build and run it yourself.  Make sure you have [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/) installed.

In the root of the repository, first build the container:

```
docker build --no-cache --tag posthog-hogflix-demo .
```

And then run the container in detatched mode (e.g. the background) with the following command, substituting in the correct Project API key and PostHog Host:

```
docker run -d -p 5000:5000 -e PH_PROJECT_KEY=<Project API key> -e PH_HOST='https://<eu or us>.i.posthog.com' posthog-hogflix-demo
```

You can then access the app on localhost:5000 or whatever the first port number is after `-p`, if you changed it.

## Seed historic usage data

To be able to see valuable insights in your PostHog project you'll also need to add some historic event data.  The `seed_demo_data.py` script creates some pseudo-random data which looks like real usage of the HogFlix app.  You'll need to have the `500_names_and_emails.csv` in your `scripts` folder (see below on how to generate this)  and then you can run it as follows:

```
python scripts/seed_demo_data.py -k <Project API Key>  -p https://<eu or us>.i.posthog.com -d 30 -i 100
```
The input parameters are:
* -k the Project API key for your demo project
* -h the PostHog Host
* -d the number of previous days to generate data over (this is optional and will default to 30 if not present)
* -i the number of iterations of the generation script to run (this is optional and will default to 100 if not present)

After a few minutes you'll see some newly created events and people in your PostHog project.

## Create demo artifacts

After generating some historic data you'll need some PostHog artifacts to view as part of a demo.  The `create_posthog_artifacts.py` script adds in:

* Actions looking at pageview and custom events
* Cohorts looking at both behavior and user properties
* Insights using the above actions
* Feature Flag for the action mode feature which is integrated into the app

You'll need a Personal API key for this rather than a Project API key.  You can generate one from `/settings/user-api-keys` in the PostHog UI

When you've got the Personal API key you can run the script to generate the artifacts (you'll just need to run this once per project):

```
python scripts/create_posthog_artifacts.py -p "https://<eu or us>.posthog.com/api/projects/<project id>" -k "<Personal API key>"
```

The input parameters are:
* -k the Project API key for your demo project
* -h the API Endpoint for your PostHog Project 

## Recreate the seed data

The `500_names_and_emails.csv` file in the `scripts/` folder has dummy data for 500 users including some group (Family) information.  This reduces some of the randomness, assigns more than one user to some groups and allows you to generate data for the same users over time, more realisticly mirroring a real product.  You shouldn't need to but if for any reason you want to recreate this CSV first delete the older version in the `scripts/` folder and then run:

```
python scripts/generate_fake_names_and_emails.py     
```

Then copy the generated file back to the `scripts/` folder and you will be good to generate more demo data.