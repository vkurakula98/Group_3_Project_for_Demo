from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['event_management']

# Function to subscribe a user to an event
def subscribe_to_event(event_id, subscriber_id):
    event = db.events.find_one({"_id": event_id})
    if event:
        db.events.update_one(
            {"_id": event_id},
            {"$addToSet": {"subscribers": subscriber_id}}
        )
        print(f"Subscriber {subscriber_id} subscribed to event {event_id}.")
    else:
        print(f"Event with ID {event_id} does not exist.")

# Function to publish an event to all subscribers
def publish_event(event_id):
    event = db.events.find_one({"_id": event_id})
    if event:
        subscribers = event.get("subscribers", [])
        summary = event.get("summary", "No summary available.")
        for subscriber_id in subscribers:
            print(f"Subscriber {subscriber_id} received event summary: {summary}")
    else:
        print(f"Event with ID {event_id} does not exist.")

import unittest
from pymongo import MongoClient
from unittest.mock import patch

client = MongoClient('mongodb://localhost:27017/')
db = client['event_management']

class TestEventManagement(unittest.TestCase):

    def setUp(self):
        # Setting up test data in MongoDB
        db.events.insert_one({
            "_id": "event123",
            "name": "Test Event",
            "summary": "This is a test event.",
            "subscribers": []
        })
        db.subscribers.insert_one({
            "_id": "subscriber1",
            "name": "John Doe",
            "email": "john@example.com"
        })

    def tearDown(self):
        # Cleaning up test data from MongoDB
        db.events.delete_many({})
        db.subscribers.delete_many({})

    def test_subscribe_to_event(self):
        # Test if subscriber is added to event's subscriber list
        subscribe_to_event("event123", "subscriber1")
        event = db.events.find_one({"_id": "event123"})
        self.assertIn("subscriber1", event['subscribers'])

    @patch('builtins.print')
    def test_publish_event(self, mock_print):
        # Test if event summary is published to all subscribers
        subscribe_to_event("event123", "subscriber1")
        publish_event("event123")
        mock_print.assert_called_with('Subscriber subscriber1 received event summary: This is a test event.')
#Review to be done outside the team

if __name__ == '__main__':
    unittest.main()
