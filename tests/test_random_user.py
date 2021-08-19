import requests
from assertpy.assertpy import assert_that
from json import dumps

# Using ?seed=test to generate the same user each time
# which returns "first": "Areta","last": "Araújo"

BASE_URI = 'https://randomuser.me/api/?seed=test'

def test_read_all_has_areta():
    response = requests.get(BASE_URI)
    response_text = response.json()
    print(response_text)

    assert_that(response.status_code).is_equal_to(200)
    first_name = [results['first'] for results in response_text]
    assert_that(first_name).contains('Areta')