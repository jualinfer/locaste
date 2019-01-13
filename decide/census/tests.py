import random
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Census
from voting.models import Voting
from authentication.models import UserProfile

from base import mods
from base.tests import BaseTestCase


class CensusTestCase(BaseTestCase):

    def create_voters(self):
        res = []
        for i in range(10):
            u = User(username='testvoter{}'.format(i))
            u.set_password('1234abcd')
            u.save()
            u.userprofile.gender = 'Male'
            u.userprofile.birthdate = '2019-01-13 11:39:48.792042+01:00'
            u.save()

            user_id = User.objects.filter(username='testvoter{}'.format(i)).values('id')[0]['id']
            res.append(user_id)
        return res

    def setUp(self):
        super().setUp()

        self.login()

        self.u = User(username='newUserGeneral')
        self.u.set_password('1234abcd')
        self.u.save()
        self.u.userprofile.gender = 'Male'
        self.u.userprofile.birthdate = '2019-01-13 11:39:48.792042+01:00'
        self.u.save()

        voting_data = {
            'name': 'test_voting_General',
            'desc': 'Description example',
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse']
        }
        response = self.client.post('/voting/', voting_data, format='json')
        self.assertEqual(response.status_code, 201)

        user_id = User.objects.filter(username='newUserGeneral').values('id')[0]['id']
        voting_id = Voting.objects.filter(name='test_voting_General').values('id')[0]['id']
        self.voting = Voting.objects.get(id=voting_id)

        self.census = Census.create(voting_id=voting_id, voter_id=user_id)
        self.census.save()

    def tearDown(self):
        super().tearDown()
        self.census.delete()
        self.voting.delete()
        self.u.delete()
        # self.user_profile.delete()

    def test_check_vote_permissions(self):
        user_id = User.objects.filter(username='newUserGeneral').values('id')[0]['id']
        voting_id = Voting.objects.filter(name='test_voting_General').values('id')[0]['id']

        response = self.client.get('/census/{}/?voter_id={}'.format(1, 2), format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 'Invalid voter')

        response = self.client.get('/census/{}/?voter_id={}'.format(voting_id, user_id), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Valid voter')

    def test_list_voting(self):
        voting_id = Voting.objects.filter(name='test_voting_General').values('id')[0]['id']
        user_id = User.objects.filter(username='newUserGeneral').values('id')[0]['id']

        response = self.client.get('/census/?voting_id={}'.format(voting_id), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'voters': [user_id]})

        self.logout()
        response = self.client.get('/census/?voting_id={}'.format(voting_id), format='json')
        self.assertEqual(response.status_code, 401)

    def test_add_new_voters_conflict(self):
        user_id = User.objects.filter(username='newUserGeneral').values('id')[0]['id']
        voting_id = Voting.objects.filter(name='test_voting_General').values('id')[0]['id']

        data = {'voting_id': voting_id, 'voters': [user_id]}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 409)

        self.login(user='noadmin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 403)

        self.logout()
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_add_new_voters(self):
        voters = self.create_voters()
        voting_id = Voting.objects.filter(name='test_voting_General').values('id')[0]['id']
        data = {'voting_id': voting_id, 'voters': voters}

        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(data.get('voters')), Census.objects.count() - 1)

        self.login(user='noadmin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 403)

        self.logout()
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_destroy_voter(self):
        user_id = User.objects.filter(username='newUserGeneral').values('id')[0]['id']
        voting_id = Voting.objects.filter(name='test_voting_General').values('id')[0]['id']

        data = {'voters': [user_id]}
        response = self.client.delete('/census/{}/'.format(voting_id), data, format='json')
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
