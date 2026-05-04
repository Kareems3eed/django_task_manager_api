from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task


class TaskAPITest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="123456"
        )

        self.client.force_authenticate(user=self.user)

        self.task = Task.objects.create(
            user=self.user,
            title="Test Task",
            description="Test Description"
        )

    def test_get_tasks(self):
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(len(response.data["data"]), 1)

    def test_create_task(self):
        data = {
            "title": "New Task",
            "description": "Something",
            "status": "todo",
            "priority": "medium"
        }

        response = self.client.post("/api/tasks/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(Task.objects.count(), 2)

    def test_create_task_invalid_title(self):
        data = {
            "title": "a",
            "description": "bad"
        }

        response = self.client.post("/api/tasks/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])

    def test_user_cannot_see_others_tasks(self):
        other_user = get_user_model().objects.create_user(
            username="other",
            password="123456"
        )

        Task.objects.create(user=other_user, title="Other Task")

        response = self.client.get("/api/tasks/")
        self.assertEqual(len(response.data["data"]), 1)

    def test_update_task(self):
        response = self.client.patch(
            f"/api/tasks/{self.task.id}/",
            {"title": "Updated"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated")

    def test_delete_task(self):
        response = self.client.delete(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)