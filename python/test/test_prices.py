import multiprocessing

import pytest
import requests
from datetime import datetime
import time

from prices import app

TEST_PORT = 3006


def server(port):
    app.run(port=port)


def wait_for_server_to_start(server_url):
    started = False
    while not started:
        try:
            requests.get(server_url)
            started = True
        except Exception as e:
            time.sleep(0.2)


@pytest.fixture(autouse=True, scope="session")
def lift_pass_pricing_app():
    """ starts the lift pass pricing flask app running on localhost """
    p = multiprocessing.Process(target=server, args=(TEST_PORT,))
    p.start()
    server_url = f"http://127.0.0.1:{TEST_PORT}"
    wait_for_server_to_start(server_url)
    yield server_url
    p.terminate() 


def test_something(lift_pass_pricing_app):
    response = requests.get(lift_pass_pricing_app + "/prices", params={'type': '1jour'})
    assert response.json() == {'cost': 35}

def test_something_using_multiline_strings(lift_pass_pricing_app):
    response = requests.get(lift_pass_pricing_app + "/prices", params={'type': '1jour'})
    
    expected = """{"cost":35}
"""

    assert response.text == expected

    # new feature: 1. request quantity
    #              2. request multiple types of tickets

def test_request_2_adult_passes(lift_pass_pricing_app):
    response = requests.get(lift_pass_pricing_app + "/prices", params={'type': '1jour', 'quantity': 2})
    assert response.json() == {'cost': 35 * 2}


def test_request_3_adult_passes(lift_pass_pricing_app):
    response = requests.get(lift_pass_pricing_app + "/prices", params={'type': '1jour', 'quantity': 3})
    assert response.json() == {'cost': 35 * 3}

