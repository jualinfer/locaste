from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods


class PostProcTestCase(APITestCase):
    maxDiff = None


    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    def test_percentage(self):
        data = {
            'type' : 'PERCENTAGE',
            'census': 100000,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 30000 },
                { 'option': 'Option 2', 'number': 2, 'votes': 20000 },
                { 'option': 'Option 3', 'number': 3, 'votes': 7500 },
                { 'option': 'Option 4', 'number': 4, 'votes': 15000 },
                { 'option': 'Option 5', 'number': 5, 'votes': 25000 },
                { 'option': 'Option 6', 'number': 6, 'votes': 2500 },
            ]
        }
        expected_result = {
            'results': [
                { 'option': 'Option 1', 'number': 1, 'votes': 30000, 'percentage': 30.00 },
                { 'option': 'Option 5', 'number': 5, 'votes': 25000, 'percentage': 25.00 },
                { 'option': 'Option 2', 'number': 2, 'votes': 20000, 'percentage': 20.00 },
                { 'option': 'Option 4', 'number': 4, 'votes': 15000, 'percentage': 15.00 },
                { 'option': 'Option 3', 'number': 3, 'votes': 7500, 'percentage': 7.50 },
                { 'option': 'Option 6', 'number': 6, 'votes': 2500, 'percentage': 2.50 },
            ],
            'participation': 100.00,
        }

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)





    def test_identity(self):
        data = {
            'type': None,
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

    def test_majorrest(self):
        data = {
            'type': 'MAJORREST',
            'seats': 21,
            'census': 1000000,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 391000 },
                { 'option': 'Option 2', 'number': 2, 'votes': 311000 },
                { 'option': 'Option 3', 'number': 3, 'votes': 184000 },
                { 'option': 'Option 4', 'number': 4, 'votes': 73000 },
                { 'option': 'Option 5', 'number': 5, 'votes': 27000 },
                { 'option': 'Option 6', 'number': 6, 'votes': 12000 },
                { 'option': 'Option 7', 'number': 7, 'votes': 2000 },
            ]
        }

        expected_result = {
            'results_hare': [
                { 'option': 'Option 1', 'number': 1, 'votes': 391000, 'postproc': 8 },
                { 'option': 'Option 2', 'number': 2, 'votes': 311000, 'postproc': 6 },
                { 'option': 'Option 3', 'number': 3, 'votes': 184000, 'postproc': 4 },
                { 'option': 'Option 4', 'number': 4, 'votes': 73000, 'postproc': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 27000, 'postproc': 1 },
                { 'option': 'Option 6', 'number': 6, 'votes': 12000, 'postproc': 0 },
                { 'option': 'Option 7', 'number': 7, 'votes': 2000, 'postproc': 0 },
            ],
            'results_droop': [
                { 'option': 'Option 1', 'number': 1, 'votes': 391000, 'postproc': 8 },
                { 'option': 'Option 2', 'number': 2, 'votes': 311000, 'postproc': 7 },
                { 'option': 'Option 3', 'number': 3, 'votes': 184000, 'postproc': 4 },
                { 'option': 'Option 4', 'number': 4, 'votes': 73000, 'postproc': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 27000, 'postproc': 0 },
                { 'option': 'Option 6', 'number': 6, 'votes': 12000, 'postproc': 0 },
                { 'option': 'Option 7', 'number': 7, 'votes': 2000, 'postproc': 0 },
            ],
            'results_imperiali': [
                { 'option': 'Option 1', 'number': 1, 'votes': 391000, 'postproc': 9 },
                { 'option': 'Option 2', 'number': 2, 'votes': 311000, 'postproc': 7 },
                { 'option': 'Option 3', 'number': 3, 'votes': 184000, 'postproc': 4 },
                { 'option': 'Option 4', 'number': 4, 'votes': 73000, 'postproc': 1 },
                { 'option': 'Option 5', 'number': 5, 'votes': 27000, 'postproc': 0 },
                { 'option': 'Option 6', 'number': 6, 'votes': 12000, 'postproc': 0 },
                { 'option': 'Option 7', 'number': 7, 'votes': 2000, 'postproc': 0 },
            ],
            'participation': 100.00,
        }

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_saintelague(self):
        data = {
            'type': 'SAINTELAGUE',
            'seats': 7,
            'census': 840000,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 340000 },
                { 'option': 'Option 2', 'number': 2, 'votes': 280000 },
                { 'option': 'Option 3', 'number': 3, 'votes': 160000 },
                { 'option': 'Option 4', 'number': 4, 'votes': 60000 },
            ]
        }

        expected_result = {
            'results': [
            { 'option': 'Option 1', 'number': 1, 'votes': 340000, 'postproc': 3 },
            { 'option': 'Option 2', 'number': 2, 'votes': 280000, 'postproc': 2 },
            { 'option': 'Option 3', 'number': 3, 'votes': 160000, 'postproc': 1 },
            { 'option': 'Option 4', 'number': 4, 'votes': 60000, 'postproc': 1 },
            ],
             'participation': 100.00,
        }
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_saintelaguemod(self):
        data = {
            'type': 'SAINTELAGUEMOD',
            'seats': 8,
            'census': 350000,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 160000 },
                { 'option': 'Option 2', 'number': 2, 'votes': 90000 },
                { 'option': 'Option 3', 'number': 3, 'votes': 80000 },
                { 'option': 'Option 4', 'number': 4, 'votes': 20000 },
            ]
        }

        expected_result = {
            'results': [
            { 'option': 'Option 1', 'number': 1, 'votes': 160000, 'postproc': 4 },
            { 'option': 'Option 2', 'number': 2, 'votes': 90000, 'postproc': 2 },
            { 'option': 'Option 3', 'number': 3, 'votes': 80000, 'postproc': 2 },
            ],
            'participation': 100.00,
        }
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)



    def test_borda(self):
        data = {
            'type': 'BORDA',
            'census': 10,
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': [5, 2, 3] },
                { 'option': 'Option 2', 'number': 2, 'votes': [5, 0, 5] },
                { 'option': 'Option 3', 'number': 3, 'votes': [3, 1, 6] },
            ]
        }

        expected_result = {
            'results': [
                { 'option': 'Option 1', 'number': 1, 'votes': [5, 2, 3], 'postproc': 22 },
                { 'option': 'Option 2', 'number': 2, 'votes': [5, 0, 5], 'postproc': 20 },
                { 'option': 'Option 3', 'number': 3, 'votes': [3, 1, 6], 'postproc': 17 },
            ],
        }

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
