import unittest

from fastapi.testclient import TestClient

from main import app


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_chat_msgs(self):
        response = self.client.get("/chats/1", params={"limit": 30})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["messages"]), 30)
        response = self.client.get("/chats/9999", params={"limit": 30})
        self.assertEqual(response.status_code, 400)

    def test_create_chat(self):
        response = self.client.post("/chats", json={"title": "new title"})
        self.assertEqual(response.status_code, 200)

    def test_create_msg(self):
        response = self.client.post("/chats/1/messages", json={"text": "new msg"})
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/chats/9999/messages", json={"text": "new msg"})
        self.assertEqual(response.status_code, 400)

    def test_delete_chat(self):
        response = self.client.delete("/chats/2")
        self.assertEqual(response.status_code, 204)


if __name__ == "__main__":
    unittest.main()
