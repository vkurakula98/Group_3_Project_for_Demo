from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Use or create a database
db = client['event_management']

# Create collections
events_collection = db['events']
subscribers_collection = db['subscribers']

# Insert data into the Events collection
event_data = {
    "eventId": "E001",
    "eventName": "Introduction to Machine Learning",
    "eventDescription": "A beginner's guide to understanding machine learning concepts.",
    "location": "On Campus",
    "venue": "Room A203, Engineering Building",
    "eventDate": "2024-09-15",
    "startTime": "10:00 AM",
    "endTime": "12:00 PM",
    "duration": "2 hours",
    "organizer": {
        "organizerName": "Concordia AI Club",
        "organizerEmail": "ai-club@concordia.ca",
        "contactNumber": "+1-514-123-4567"
    },
    "tags": ["Machine Learning", "AI", "Beginner"],
    "attendees": [
        {
            "subscriberId": "S001",
            "name": "Alice Johnson",
            "email": "alice.johnson@example.com",
            "registrationDate": "2024-08-20"
        },
        {
            "subscriberId": "S002",
            "name": "Bob Smith",
            "email": "bob.smith@example.com",
            "registrationDate": "2024-08-22"
        }
    ]
}

events_collection.insert_one(event_data)

# Insert data into the Subscribers collection
subscriber_data = {
    "subscriberId": "S001",
    "name": "Alice Johnson",
    "email": "alice.johnson@example.com",
    "phoneNumber": "+1-514-555-7890",
    "registeredEvents": [
        {
            "eventId": "E001",
            "eventName": "Introduction to Machine Learning",
            "registrationDate": "2024-08-20"
        }
    ],
    "subscriptionDate": "2024-08-15"
}

subscribers_collection.insert_one(subscriber_data)
#Review to be done outside the team

# Query data from Events collection
print("Events:")
for event in events_collection.find():
    print(event)

# Query data from Subscribers collection
print("\nSubscribers:")
for subscriber in subscribers_collection.find():
    print(subscriber)
