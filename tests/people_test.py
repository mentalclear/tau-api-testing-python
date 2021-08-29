import requests
from assertpy.assertpy import assert_that
from json import dumps, loads
from config import BASE_URI
from utils.print_helpers import pretty_print
from uuid import uuid4
import pytest
import random
from utils.file_reader import read_file
from jsonpath_ng import parse


def test_read_all_has_kent():
    response_text, response = get_all_users()
    pretty_print(response_text)

    assert_that(response.status_code).is_equal_to(200)
    first_names = [people['fname'] for people in response_text]
    # assert_that(first_names).contains('Kent')
    
    # Same option with assertpy extracting the first name from the response
    assert_that(response_text).extracting('fname').contains('Kent')

def test_new_person_can_be_added():
    unique_last_name = create_new_unique_user()

    people = requests.get(BASE_URI).json()
    is_new_user_created = filter(lambda person: person['lname'] == unique_last_name, people)
    assert_that(is_new_user_created).is_true()


def test_person_can_be_deleted():
    new_user_last_name = create_new_unique_user()
    all_users, _ = get_all_users()
    new_user = search_user_by_last_name(all_users, new_user_last_name)[0]

    print(new_user)
    person_to_be_deleted = new_user['person_id']

    url = f'{BASE_URI}/{person_to_be_deleted}'
    response= requests.delete(url)

    assert_that(response.status_code).is_equal_to(200)

def create_new_unique_user():
    unique_last_name = f'User {str(uuid4())}'
    payload = dumps({
        'fname': 'New',
        'lname': unique_last_name
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.post(url=BASE_URI, data=payload, headers=headers)
    assert_that(response.status_code).is_equal_to(204)
    return unique_last_name

def get_all_users():
    response = requests.get(BASE_URI)
    response_text = response.json()
    return response_text, response

def search_user_by_last_name(response_text, last_name):
    return [person for person in response_text if person['lname'] == last_name]


@pytest.fixture
def create_data():
    payload = read_file('create_person.json')

    random_no = random.randint(0, 1000)
    last_name = f'Olabini{random_no}'

    payload['lname'] = last_name
    yield payload


def test_person_can_be_added_with_a_json_template(create_data):
    create_person_with_unique_last_name(create_data)

    response = requests.get(BASE_URI)
    peoples = loads(response.text)

    # Get all last names for any object in the root array
    # Here $ = root, [*] represents any element in the array
    # Read full syntax: https://pypi.org/project/jsonpath-ng/
    jsonpath_expr = parse("$.[*].lname")
    result = [match.value for match in jsonpath_expr.find(peoples)]

    expected_last_name = create_data['lname']
    assert_that(result).contains(expected_last_name)


def create_person_with_unique_last_name(body=None):
    if body is None:
        # Ensure a user with a unique last name is created everytime the test runs
        # Note: json.dumps() is used to convert python dict to json string
        unique_last_name = f'User {str(uuid4())}'
        payload = dumps({
            'fname': 'New',
            'lname': unique_last_name
        })
    else:
        unique_last_name = body['lname']
        payload = dumps(body)

    # Setting default headers to show that the client accepts json
    # And will send json in the headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # We use requests.post method with keyword params to make the request more readable
    response = requests.post(url=BASE_URI, data=payload, headers=headers)
    assert_that(response.status_code, description='Person not created').is_equal_to(requests.codes.no_content)
    return unique_last_name

def search_created_user_in(peoples, last_name):
    return [person for person in peoples if person['lname'] == last_name]