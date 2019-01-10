from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    def test_identity(self):
        data = {
            'type': 'IDENTITY',
            'census': 23,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        expected_result = {
            'results': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 5 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
            ],
            'participation': 69.57,
        }

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_dhondt(self):
        data = {
            'type': 'DHONDT',
            'seats': 8,
            'census': 230000,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 100000 },
                { 'option': 'Option 2', 'number': 2, 'votes': 80000 },
                { 'option': 'Option 3', 'number': 3, 'votes': 30000 },
                { 'option': 'Option 4', 'number': 4, 'votes': 20000 },
            ]
        }

        expected_result = {
            'results': [
                { 'option': 'Option 1', 'number': 1, 'votes': 100000, 'postproc': 4 },
                { 'option': 'Option 2', 'number': 2, 'votes': 80000, 'postproc': 3 },
                { 'option': 'Option 3', 'number': 3, 'votes': 30000, 'postproc': 1 },
            ],
            'participation': 100.00,
        }

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
