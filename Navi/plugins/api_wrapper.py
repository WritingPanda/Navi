import requests
from .database import new_db_connection
from .utils import get_keys_from_config


def grab_headers():
    keys = get_keys_from_config()
    return {
        'Content-type': 'application/json', 
        'user-agent': 'navi-5.0.0', 
        'X-ApiKeys': 'accessKey={};secretKey={}'.format(keys['access_key'], keys['secret_key'])
    }

# TODO: Refactor code to include a session object to make requests
def request_delete(method, url_mod):

    # set the Base URL
    url = "https://cloud.tenable.com"

    try:
        r = requests.request(method, url + url_mod, headers=grab_headers(), verify=True)
        if r.status_code == 200:
            print("Success!\n")
        elif r.status_code == 404:
            print('\nCheck your query...', r)
        elif r.status_code == 429:
            print("\nToo many requests at a time...\n")
        else:
            print("Something went wrong...Don't be trying to hack me now", r)
    except ConnectionError:
        print("Check your connection...You got a connection error")


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
            # This response is for some successful posts.
            print("\nSuccess!\n")
        elif r.status_code == 404:
            print('\nCheck your query...', r)
        elif r.status_code == 429:
            print("\nToo many requests at a time...\n")
        elif r.status_code == 400:
            print("\nThe object you tried to create already exists\n")
            print("If you are Updating tags via groups it is not supported right now, "
                  "delete your group using the delete command\n")
        else:
            print("Something went wrong...Don't be trying to hack me now", r)
    except ConnectionError:
        print("Check your connection...You got a connection error")
