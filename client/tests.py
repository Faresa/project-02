from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Client, Address, ClientRelationship

class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_login_redirect(self):
        response = self.client.get(reverse('client_list'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('client_list'))

    def test_authenticated_user_access(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('client_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Logged in as testuser')

    def test_logout(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        response = self.client.get(reverse('client_list'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('client_list'))

class ClientListViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_client_list_pagination(self):
        for i in range(25):
            Client.objects.create(first_name=f'Client{i}', last_name='Doe', id_number=f'920220472008{i}')

        response = self.client.get(reverse('client_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['object_list']) == 20)

    def test_client_search(self):
        Client.objects.create(first_name='John', last_name='Doe', id_number='9202204720081')
        response = self.client.get(reverse('client_list') + '?q=John')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 1)
        self.assertContains(response, 'John Doe')

class ClientCreationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_create_client(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'id_number': '9202204720081',  # Valid SA ID number for testing
            'street': '123 Main St',
            'city': 'Springfield',
            'province': 'Anytown',
            'code': '1234',
            'country': 'South Africa',
            'address_type': 'Physical'
        }
        response = self.client.post(reverse('create_client'), data)
        self.assertEqual(response.status_code, 200)  # Redirects to client list upon success

        # Verify client and address creation
        self.assertTrue(Client.objects.filter(first_name='John', last_name='Doe', id_number='9202204720081').exists())
        self.assertTrue(Address.objects.filter(street='123 Main St', city='Springfield', code='1234').exists())

    def test_invalid_id_number(self):
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'id_number': '1234567890123',  # Invalid SA ID number
            'street': '456 Oak St',
            'city': 'Gotham',
            'province': 'Metropolis',
            'code': '5678',
            'country': 'South Africa',
            'address_type': 'Physical'
        }
        response = self.client.post(reverse('create_client'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'client_form', 'id_number', 'Invalid South African ID number format.')

class ClientRelationshipTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.client1 = Client.objects.create(first_name='John', last_name='Doe', id_number='9202204720081')
        self.client2 = Client.objects.create(first_name='Jane', last_name='Smith', id_number='9001014720081')

    def test_create_relationship(self):
        data = {
            'client_from': self.client1.id,
            'client_to': self.client2.id,
            'relationship_type': 'Husband'
        }
        response = self.client.post(reverse('add_client_relationship', args=[self.client1.id]), data)
        self.assertEqual(response.status_code, 302)  # Redirects to client list upon success

        # Verify relationship creation
        self.assertTrue(ClientRelationship.objects.filter(client_from=self.client1, client_to=self.client2, relationship_type='Husband').exists())
        self.assertTrue(ClientRelationship.objects.filter(client_from=self.client2, client_to=self.client1, relationship_type='Wife').exists())

    def test_invalid_relationship(self):
        data = {
            'client_from': self.client1.id,
            'client_to': self.client1.id,  # Self relationship attempt
            'relationship_type': 'Father'
        }
        response = self.client.post(reverse('add_client_relationship', args=[self.client1.id]), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, 'Client cannot have a relationship with themselves.')

        data = {
            'client_from': self.client1.id,
            'client_to': self.client2.id,
            'relationship_type': 'Husband'
        }
        response = self.client.post(reverse('add_client_relationship', args=[self.client1.id]), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, 'Client already has a relationship with the specified client.')

