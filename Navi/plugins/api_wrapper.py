import requests
from .database import new_db_connection


def grab_headers():
    database = r"navi.db"
    conn = new_db_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * from keys;")
        rows = cur.fetchall()
        for row in rows:
            access_key = row[0]
            secret_key = row[1]
    return {'Content-type': 'application/json', 'user-agent': 'navi-5.0.0', 'X-ApiKeys': 'accessKey=' + access_key + ';secretKey=' + secret_key}


def request_data(method, url_mod, **kwargs):

    # set the Base URL
    url = "https://cloud.tenable.com"

    # check for params and set to None if not found
    try:
        params = kwargs['params']
    except KeyError:
        params = None

    # check for a payload and set to None if not found
    try:
        payload = kwargs['payload']
    except KeyError:
        payload = None

    try:
        r = requests.request(method, url + url_mod, headers=grab_headers(), params=params, json=payload, verify=True)
        if r.status_code == 200:
            return r.json()
        if r.status_code == 202:
            print("Success!")
        elif r.status_code == 404:
            print('Check your query...', r)
        elif r.status_code == 429:
            print("Too many requests at a time...")
        elif r.status_code == 400:
            pass
        else:
            print("Something went wrong...Don't be trying to hack me now", r)
    except ConnectionError:
        print("Check your connection...You got a connection error")