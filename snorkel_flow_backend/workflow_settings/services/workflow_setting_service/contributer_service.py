"""
contributer_service.py

The module provides a service that enables the management of Contibuters.

Classes:
- ContributerServiceClass
"""

from django.db.models import Q, QuerySet
from rest_framework import status
from rest_framework.authtoken.admin import User

from workflow_settings.models import Workflow


class ContributerServiceClass:
    """
    Service class for adding, deleting and retrieving contributors in workflows.

    Methods:
        - remove_contributer_by_id(workflow_id, contributer_username):
            Removes a contributor from the specified workflow by username.

        - add_contributer_by_id(workflow_id, contributer_username):
            Adds a contributor to the specified workflow by username.

        - get_contributers(workflow_id):
            Retrieves all contributors for the specified workflow.

        - filter_contributer(workflow_id, request_user, username_start):
            Filters potential contributors based on username prefix.
    """

    def remove_contributer_by_id(self, workflow_id, contributer_username):
        """
        Removes a contributor from the specified workflow by username.

        Args:
            workflow_id (int): The ID of the workflow.
            contributer_username (str): The username of the contributor to be removed.

        Returns:
            - int: A HTTP status code.
            - dict: A dictionary containing a success message or error details.
        """
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            user = workflow[0].contributors.filter(username=contributer_username)
            if user.exists():
                workflow[0].contributors.remove(user[0])
                return status.HTTP_200_OK, {
                    "message": "Contributer was successfully removed"
                }
        return status.HTTP_404_NOT_FOUND, {
            "message": "Contributer was successfully removed"
        }

    def add_contributer_by_id(self, workflow_id, contributer_username):
        """
        Adds a contributor to the specified workflow by username.

        Args:
            workflow_id (int): The ID of the workflow.
            contributer_username (str): The username of the contributor to be added.

        Returns:
            - int: A HTTP status code.
            - dict: A dictionary containing a success message or error details.
        """
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            user = User.objects.filter(username=contributer_username)
            if user.exists():
                if (
                    not workflow[0]
                    .contributors.filter(username=user[0].username)
                    .exists()
                ):
                    workflow[0].contributors.add(user[0])
                    return status.HTTP_200_OK, {
                        "message": "Contributer was successfully added"
                    }
                return status.HTTP_400_BAD_REQUEST, {
                    "message": "The User already is a contributer"
                }
        return status.HTTP_404_NOT_FOUND, {
            "message": "Contributer couldn't be added. Username doesn't exists"
        }

    def get_contributers(self, workflow_id):
        """
        Retrieves all contributors from the specified workflow.

        Args:
            workflow_id (int): The ID of the workflow.

        Returns:
            - int: A HTTP status code.
            - dict:
                success: A dictionary containing a list of contributers.
                error: A dictionary containing a error message.
        """
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            workflow = workflow[0]
            workflow_contributer = workflow.contributors.order_by(
                "username"
            ).values_list("username", flat=True)
            workflow_creator = workflow.creator.username

            all_contributer = self.__get_contributers(
                workflow_creator, workflow_contributer
            )

            return status.HTTP_200_OK, all_contributer
        return status.HTTP_404_NOT_FOUND, {"message": "Workflow doesn't exists"}

    def filter_contributer(self, workflow_id, request_user, username_start):
        """
        Retrieves all users (and are not contributer) which match
        the prefix of the string username_start.

        Args:
            workflow_id (int): The ID of the workflow.
            request_user (User): User who made the request.
            username_start (string): Prefix of the username you are looking for.

        Returns:
            - int: A HTTP status code.
            - dict:
                success: A dictionary containing a list of possible usernames.
                error: A dictionary containing a error message.
        """
        workflow = Workflow.objects.filter(pk=workflow_id)
        if workflow.exists():
            workflow = workflow[0]
            workflow_contributer = workflow.contributors.order_by(
                "username"
            ).values_list("username", flat=True)

            all_users = self.__filter_contributer(
                workflow_contributer, request_user, username_start
            )

            return status.HTTP_200_OK, all_users
        return status.HTTP_404_NOT_FOUND, {"message": "Workflow doesn't exists"}

    def __filter_contributer(self, workflow_contributer, request_user, username_start):
        """
        Private function:
        Filters potential contributors based on username prefix.

        Args:
            workflow_id (int): The ID of the workflow.
            request_user (User): User who made the request.
            username_start (str): The username prefix to filter potential contributors.

        Returns:
            list: list of filtered users in a dict.
        """
        users_not_contributer: QuerySet[User] = User.objects.filter(
            Q(is_staff=False),
            ~Q(username=request_user),
            ~Q(username__in=workflow_contributer),
        )
        filter_possible_contributer = (
            users_not_contributer.filter(username__startswith=username_start)
            .order_by("username")
            .values_list("username", flat=True)
        )

        all_users = []
        for contributer in filter_possible_contributer:
            dic = {}
            dic["username"] = contributer
            all_users.append(dic)

        if len(all_users) == 0:
            dic = {}
            dic["username"] = "No results were found!"
            all_users.append(dic)
        return all_users

    def __get_contributers(self, workflow_creator, workflow_contributer):
        """
        Private function:
        Retrieves all contributors from the specified workflow.

        Args:
            workflow_creator (str): The username of the workflow creator.
            workflow_contributer (list): List of contributors.

        Returns:
            list: list of contributors and the workflow creator in a dict.
        """
        contributer_list = []
        for contributer in workflow_contributer:
            dic = {}
            dic["username"] = contributer
            contributer_list.append(dic)
        contributer_list.append({"username": workflow_creator})
        return contributer_list
