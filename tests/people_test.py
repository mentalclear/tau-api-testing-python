import requests
from assertpy.assertpy import assert_that

from json import dumps
from config import BASE_URI
from utils.print_helpers import pretty_print
from uuid import uuid4


def test_read_all_has_kent():
    response_text, response = get_all_users()
    pretty_print(response_text)

    assert_that(response.status_code).is_equal_to(200)
    first_names = [people['fname'] for people in response_text]
    assert_that(first_names).contains('Bunny')


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

