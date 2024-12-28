import json

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from workflow_settings.models import Workflow

# Unit Test
# urls: settings/workflow/ and settings/workflow/<int:pk>/
class WorkflowViewTest(APITestCase):

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


        self.url_1 = reverse('workflow')
        self.client = APIClient()

    # Test settings/workflow/
    # post
    def test_create_workflow(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_3.key)

        data = {'is_public': 'True', 'title': 'Workflow_Test_3'}

        response = self.client.post(self.url_1, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workflow.objects.all().count(), 3)
        self.assertEqual(Workflow.objects.filter(creator=self.user_3).count(), 1)
        self.assertEqual(Workflow.objects.filter(creator=self.user_3)[0].title, 'Workflow_Test_3')

    def test_create_workflow_failed(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_1.key)

        data = {'is_public': 'True', 'title': 'Workflow_Test_1'}

        response = self.client.post(self.url_1, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Workflow.objects.all().count(), 2)

    # get
    def test_list_user_1(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_1.key)

        response = self.client.get(self.url_1)

        response_content: list = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_content), 2)

    def test_list_user_2(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_2.key)

        response = self.client.get(self.url_1)

        response_content: list = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_content), 1)

    def test_list_user_3(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_3.key)

        response = self.client.get(self.url_1)

        response_content: list = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_content), 1)

    # Test settings/workflow/<int:pk>/
    # get

    def test_list_user_1_creator_get_by_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_1.key)

        self.url_2 = reverse('workflow_user', args=[1])

        response = self.client.get(self.url_2)
        response_content: dict = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_user_1_contributer_get_by_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_1.key)

        self.url_2 = reverse('workflow_user', args=[2])

        response = self.client.get(self.url_2)
        response_content: dict = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_user_3_forbidden_get_by_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_3.key)

        self.url_2 = reverse('workflow_user', args=[1])

        response = self.client.get(self.url_2)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_user_3_get_by_id_public(self):
        Workflow.objects.create(creator=self.user_4, is_public=True, title="Workflow_Test_4")

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_3.key)

        self.url_2 = reverse('workflow_user', args=[3])

        response = self.client.get(self.url_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # delete
    def test_list_user_1_creator_delete_by_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_1.key)

        self.url_2 = reverse('workflow_user', args=[1])

        response = self.client.delete(self.url_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_user_1_contributer_delete_by_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_1.key)

        self.url_2 = reverse('workflow_user', args=[2])

        response = self.client.delete(self.url_2)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_user_3_forbidden_delete_by_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_3.key)

        self.url_2 = reverse('workflow_user', args=[1])

        response = self.client.delete(self.url_2)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_update_by_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_2.key)

        self.url_2 = reverse('workflow_user', args=[2])

        data = {'is_public': 'True'}

        response = self.client.patch(self.url_2, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_by_id_public(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_2.key)

        self.url_2 = reverse('workflow_user', args=[2])

        data = {'is_public': 'True'}

        response = self.client.patch(self.url_2, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_add_contributer(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_1.key)

        self.url_2 = reverse('workflow_contibuter', args=[1])

        data = {'username': 'test_user_2'}

        response = self.client.post(self.url_2, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Workflow.objects.get(pk=1).contributors.count(), 1)

    def test_add_contributer_connected(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_2.key)

        self.url_2 = reverse('workflow_contibuter', args=[2])

        data = {'username': 'test_user_1'}

        response = self.client.post(self.url_2, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Workflow.objects.get(pk=2).contributors.count(), 2)

    def test_add_contributer_not_exists(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_2.key)

        self.url_2 = reverse('workflow_contibuter', args=[2])

        data = {'username': 'test_user_6'}

        response = self.client.post(self.url_2, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Workflow.objects.get(pk=2).contributors.count(), 2)

    def test_add_contributer_not_creator(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_1.key)

        self.url_2 = reverse('workflow_contibuter', args=[2])

        data = {'username': 'test_user_6'}

        response = self.client.post(self.url_2, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Workflow.objects.get(pk=2).contributors.count(), 2)

    def test_remove_contributer(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_2.key)

        self.url_2 = reverse('workflow_contibuter', args=[2])

        data = {'username': 'test_user_1'}

        response = self.client.delete(self.url_2, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Workflow.objects.get(pk=2).contributors.count(), 1)

    def test_remove_contributer_not_exists(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_2.key)

        self.url_2 = reverse('workflow_contibuter', args=[2])

        data = {'username': 'test_user_6'}

        response = self.client.post(self.url_2, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Workflow.objects.get(pk=2).contributors.count(), 2)

    def test_remove_contributer_not_creator(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user_1.key)

        self.url_2 = reverse('workflow_contibuter', args=[2])

        data = {'username': 'test_user_6'}

        response = self.client.post(self.url_2, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Workflow.objects.get(pk=2).contributors.count(), 2)
