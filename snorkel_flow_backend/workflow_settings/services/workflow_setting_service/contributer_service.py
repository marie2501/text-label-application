from django.db.models import Q, QuerySet
from rest_framework import status
from rest_framework.authtoken.admin import User

from workflow_settings.models import Workflow


class ContributerServiceClass:

    def remove_contributer_by_id(self, workflow_id, contributer_username):
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            user = workflow[0].contributors.filter(username=contributer_username)
            if user.exists():
                workflow[0].contributors.remove(user[0])
                return status.HTTP_200_OK, {"message": "Contributer was successfully removed"}
        return status.HTTP_404_NOT_FOUND, {"message": "Contributer was successfully removed"}

    def add_contributer_by_id(self, workflow_id, contributer_username):
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            user = User.objects.filter(username=contributer_username)
            if user.exists():
                if not workflow[0].contributors.filter(username=user[0].username).exists():
                    workflow[0].contributors.add(user[0])
                    return status.HTTP_200_OK, {"message": "Contributer was successfully added"}
                return status.HTTP_400_BAD_REQUEST, {"message": "The User already is a contributer"}
        return status.HTTP_404_NOT_FOUND, {"message": "Contributer couldn't be added. Username doesn't exists"}

    def get_contributers(self, workflow_id):
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            workflow = workflow[0]
            workflow_contributer = workflow.contributors.order_by('username').values_list('username', flat=True)
            workflow_creator = workflow.creator.username

            all_contributer = self.__get_contributers(workflow_creator, workflow_contributer)

            return status.HTTP_200_OK, all_contributer
        return status.HTTP_404_NOT_FOUND, {"message": "Workflow doesn't exists"}

    def filter_contributer(self, workflow_id, request_user, username_start):
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            workflow = workflow[0]
            workflow_contributer = workflow.contributors.order_by('username').values_list('username', flat=True)

            all_users = self.__filter_contributer(workflow_contributer, request_user, username_start)

            return status.HTTP_200_OK, all_users
        return status.HTTP_404_NOT_FOUND, {"message": "Workflow doesn't exists"}

    def __filter_contributer(self, workflow_contributer, request_user, username_start):
        users_not_contributer : QuerySet[User] = User.objects.filter(Q(is_staff=False), ~Q(username=request_user),
                                                    ~Q(username__in=workflow_contributer))
        filter_possible_contributer = users_not_contributer.filter(username__startswith=username_start).order_by('username').values_list('username', flat=True)

        all_users = []
        for contributer in filter_possible_contributer:
            dic = {}
            dic['username'] = contributer
            all_users.append(dic)
        return all_users

    def __get_contributers(self, workflow_creator, workflow_contributer):
        contributer_list = []
        for contributer in workflow_contributer:
            dic = {}
            dic['username'] = contributer
            contributer_list.append(dic)
        contributer_list.append({'username': workflow_creator})
        return contributer_list
