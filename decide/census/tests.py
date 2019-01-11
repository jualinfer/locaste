import random
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Census
from voting.models import Voting
from base import mods
from base.tests import BaseTestCase


class CensusTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        # self.census = Census.create(voting_id=1, voter_id=1)
        # self.census.save()

    def tearDown(self):
        super().tearDown()
        self.census = None

    def test_check_vote_permissions(self):
        response = self.client.get('/census/{}/?voter_id={}'.format(1, 2), format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 'Invalid voter')

        response = self.client.get('/census/{}/?voter_id={}'.format(1, 1), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Valid voter')

    def test_list_voting(self):
        # response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        # self.assertEqual(response.status_code, 401)

        # self.login(user='noadmin')
        # response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        # self.assertEqual(response.status_code, 403)

        # self.login()
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'voters': [1]})

    def test_add_new_voters_conflict(self):
        data = {'voting_id': 1, 'voters': [1]}
        # response = self.client.post('/census/', data, format='json')
        # self.assertEqual(response.status_code, 401)

        # self.login(user='noadmin')
        # response = self.client.post('/census/', data, format='json')
        # self.assertEqual(response.status_code, 403)

        # self.login()
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 409)

    def test_add_new_voters(self):
        data = {'voting_id': 1, 'voters': [1, 2, 3, 4]}
        # response = self.client.post('/census/', data, format='json')
        # self.assertEqual(response.status_code, 401)

        # self.login(user='noadmin')
        # response = self.client.post('/census/', data, format='json')
        # self.assertEqual(response.status_code, 403)

        # self.login()
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(data.get('voters')), Census.objects.count() - 1)

    def test_destroy_voter(self):
        data = {'voters': [1]}
        response = self.client.delete('/census/{}/'.format(1), data, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(0, Census.objects.count())

    def test_create_census_with_voting_restrictions(self):
        # username, gender, birthdate, voting_name, voting_gender, voting_min_age, voting_max_age, expected_status_code

        self.login()

        test_data = [
            ['newuser1', 'Male', '2001-12-08T00:00', 'test_voting1', 'Male', 10, 18, 201],  # Positive Test
            ['newuser2', 'Male', '2001-12-08T00:00', 'test_voting2', 'Female', 10, 18, 400],  # Negative Test - Gender
            ['newuser3', 'Female', '2001-12-08T00:00', 'test_voting3', 'Other', 10, 18, 400],  # Negative Test - Gender
            ['newuser4', 'Other', '2001-12-08T00:00', 'test_voting3', 'Male', 10, 18, 400],  # Negative Test - Gender
            ['newuser5', 'Male', '2010-12-08T00:00', 'test_voting4', 'Male', 10, 18, 400],  # Negative Test - min age
            ['newuser6', 'Male', '1993-12-08T00:00', 'test_voting5', 'Male', 10, 18, 400],  # Negative Test - max age
        ]

        for data in test_data:
            self.census_test_voting_restrictions(*data)

    def census_test_voting_restrictions(self, username, gender, birthdate, voting_name, voting_gender,
                                        voting_min_age, voting_max_age, expected_status_code):
        user_data = {'username': username,
                     'password1': '1234abcd',
                     'password2': '1234abcd',
                     'gender': gender,
                     'birthdate': birthdate}
        response = self.client.post('/authentication/signup/', user_data, format='json')
        self.assertEqual(response.status_code, 201)

        voting_data = {
            'name': voting_name,
            'desc': 'Description example',
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse']
        }
        response = self.client.post('/voting/', voting_data, format='json')
        self.assertEqual(response.status_code, 201)

        user_id = User.objects.filter(username=username).values('id')[0]['id']
        voting_id = Voting.objects.filter(name=voting_name).values('id')[0]['id']

        voting = Voting.objects.get(id=voting_id)
        voting.gender = voting_gender
        voting.min_age = voting_min_age
        voting.max_age = voting_max_age
        voting.save()

        census_data = {
            'voting_id': voting_id,
            'voters': [user_id]
        }
        response = self.client.post('/census/', census_data, format='json')
        self.assertEqual(response.status_code, expected_status_code)
