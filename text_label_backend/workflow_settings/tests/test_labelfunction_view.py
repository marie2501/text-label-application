import json
import os
import yaml

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from workflow_settings.models import Workflow, Labelfunction

class LabelfunctionViewTest(APITestCase):

    def setUp(self):
        # Setup 4 Users
        self.user_1 = User.objects.create(username='test_user_1', email='test_user1@user.com')
        self.token_user_1 = Token.objects.create(user=self.user_1)
        self.user_2 = User.objects.create(username='test_user_2', email='test_user2@user.com')
        self.token_user_2 = Token.objects.create(user=self.user_2)
        self.user_3 = User.objects.create(username='test_user_3', email='test_user3@user.com')
        self.token_user_3 = Token.objects.create(user=self.user_3)
        self.user_4 = User.objects.create(username='test_user_4', email='test_user4@user.com')
        self.token_user_4 = Token.objects.create(user=self.user_4)

        self.workflow_user1 =  Workflow.objects.create(creator=self.user_1, is_public=False, title="Workflow_Test_1")
        self.workflow_user2 = Workflow.objects.create(creator=self.user_2, is_public=False, title="Workflow_Test_2")
        self.workflow_user2.contributors.add(self.user_1)
        self.workflow_user2.contributors.add(self.user_3)

        self.client = APIClient()

    # Datenbanktests
    # 'title', 'type', 'code'
    def test_add_labelfunction(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_1.key)

        data = {'name': 'Test_Python_Code', 'type': 'python_code', 'code': 'def add():\n   x = 16\n   y = 13\n   print(x+y)'}

        self.url_1 = reverse('labelfunction', args=[1])

        response = self.client.post(self.url_1, data=data, format='json')

        code = Labelfunction.objects.get(workflow_id=1).code

        exec(code)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Labelfunction.objects.filter(workflow_id=1).count(), 1)


    def test_add_labelfunction_missing_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_1.key)

        data = {'name': 'Test_Python_Code', 'code': 'def add():\n   x = 16\n   y = 13\n   print(x+y)'}

        self.url_1 = reverse('labelfunction', args=[1])

        response = self.client.post(self.url_1, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Labelfunction.objects.filter(workflow_id=1).count(), 0)


    def test_get_all_by_workflow_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_2.key)
        Labelfunction.objects.create(name='Test_Python_Code', creator=self.user_2, type='python_code',
                                     code='def add():\n   x = 16\n   y = 13\n   print(x+y)', workflow_id=2)
        Labelfunction.objects.create(name='Test_Python_Code_1', creator=self.user_2, type='python_code',
                                     code='def add():\n   x = 16\n   y = 13\n   print(x+y)', workflow_id=2)
        Labelfunction.objects.create(name='Test_Python_Code_2', creator=self.user_1, type='python_code',
                                     code='def add():\n   x = 16\n   y = 13\n   print(x+y)', workflow_id=2)

        self.url_1 = reverse('labelfunction', args=[2])

        response = self.client.get(self.url_1, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_by_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_2.key)
        Labelfunction.objects.create(name='Test_Python_Code', creator=self.user_2, type='python_code',
                                     code='def add():\n   x = 16\n   y = 13\n   print(x+y)', workflow_id=2)
        Labelfunction.objects.create(name='Test_Python_Code_1', creator=self.user_2, type='python_code',
                                     code='def add():\n   x = 16\n   y = 13\n   print(x+y)', workflow_id=2)
        Labelfunction.objects.create(name='Test_Python_Code_2', creator=self.user_1, type='python_code',
                                     code='def add():\n   x = 16\n   y = 13\n   print(x+y)', workflow_id=2)

        self.url_1 = reverse('labelfunction', args=[1])

        response = self.client.delete(self.url_1, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Labelfunction.objects.filter(workflow_id=2).count(), 2)

    def test_delete_by_id_wrong_creator(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_2.key)
        Labelfunction.objects.create(name='Test_Python_Code', creator=self.user_2, type='python_code',
                                     code='def add():\n   x = 16\n   y = 13\n   print(x+y)', workflow_id=2)
        Labelfunction.objects.create(name='Test_Python_Code_1', creator=self.user_2, type='python_code',
                                     code='def add():\n   x = 16\n   y = 13\n   print(x+y)', workflow_id=2)
        Labelfunction.objects.create(name='Test_Python_Code_2', creator=self.user_1, type='python_code',
                                     code='def add():\n   x = 16\n   y = 13\n   print(x+y)', workflow_id=2)

        self.url_1 = reverse('labelfunction', args=[3])

        response = self.client.delete(self.url_1, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Labelfunction.objects.filter(workflow_id=2).count(), 3)

    def test_update_by_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_2.key)
        Labelfunction.objects.create(name='Test_Python_Code', creator=self.user_2, type='python_code',
                                     code='def add():\n   x = 16\n   y = 13\n   print(x+y)', workflow_id=2)
        Labelfunction.objects.create(name='Test_Python_Code_1', creator=self.user_2, type='python_code',
                                     code='def add():\n   x = 16\n   y = 13\n   print(x+y)', workflow_id=2)
        Labelfunction.objects.create(name='Test_Python_Code_2', creator=self.user_1, type='python_code',
                                     code='def add():\n   x = 16\n   y = 13\n   print(x+y)', workflow_id=2)

        self.url_1 = reverse('labelfunction', args=[1])

        data = {'name': 'Update_Test'}

        response = self.client.patch(self.url_1, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Labelfunction.objects.get(pk=1).name, 'Update_Test')

    def test_update_by_id_wrong_creator(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_2.key)
        Labelfunction.objects.create(name='Test_Python_Code', creator=self.user_2, type='python_code',
                                     code='def add():\n   x = 16\n   y = 13\n   print(x+y)', workflow_id=2)
        Labelfunction.objects.create(name='Test_Python_Code_1', creator=self.user_2, type='python_code',
                                     code='def add():\n   x = 16\n   y = 13\n   print(x+y)', workflow_id=2)
        Labelfunction.objects.create(name='Test_Python_Code_2', creator=self.user_1, type='python_code',
                                     code='def add():\n   x = 16\n   y = 13\n   print(x+y)', workflow_id=2)

        self.url_1 = reverse('labelfunction', args=[3])

        data = {'name': 'Update_Test'}

        response = self.client.patch(self.url_1, data=data, format='json')


        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Labelfunction.objects.get(pk=3).name, 'Test_Python_Code_2')

    # FileTest
    # def test_get_run_by_id(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_2.key)
    #     Labelfunction.objects.create(title='Test_Python_Code', creator=self.user_2, type='python_code',
    #                                  code='def add():\n   x = 16\n   y = 13\n   print(x+y)', workflow_id=2)
    #     Labelfunction.objects.create(title='Test_Python_Code_1', creator=self.user_2, type='python_code',
    #                                  code='def add():\n   x = 16\n   y = 13\n   print(x+y)', workflow_id=2)
    #     Labelfunction.objects.create(title='Test_Python_Code_2', creator=self.user_1, type='python_code',
    #                                  code='def add():\n   x = 16\n   y = 13\n   print(x+y)', workflow_id=2)
    #
    #     self.url_1 = reverse('labelfunction', args=[2])
    #
    #     response = self.client.get(self.url_1, format='json')
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
