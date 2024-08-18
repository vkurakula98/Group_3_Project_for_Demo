from pymongo import MongoClient
from faker import Faker
import random

# Initialize Faker for generating fake data
fake = Faker()

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['sample_events']  # Corrected database name
events_collection = db['events']
subscribers_collection = db['subscribers']


# Helper function to generate a random duration
def get_random_duration():
    hours = random.choice([1, 2, 3, 4])
    return f"{hours} hours"


# Generate 20 sample events
event_ids = []
for _ in range(20):
    event_id = fake.unique.uuid4()[:8].upper()  # Generate a unique short ID
    event_ids.append(event_id)
    event_data = {
        "eventId": event_id,
        "eventName": fake.sentence(nb_words=4),
        "eventDescription": fake.paragraph(nb_sentences=2),
        "location": random.choice(["On Campus", "Virtual"]),
        "venue": fake.address() if random.choice([True, False]) else None,
        "platform": fake.company() if random.choice([True, False]) else None,
        "eventDate": fake.date_this_year().strftime('%Y-%m-%d'),  # Corrected date format
        "duration": get_random_duration(),
        "organizer": {
            "organizerName": fake.company(),
            "organizerEmail": fake.company_email(),
            "contactNumber": fake.phone_number()
        },
        "tags": fake.words(nb=3),
        "attendees": []
    }
    events_collection.insert_one(event_data)

# Generate 20 sample subscribers
for _ in range(20):
    subscriber_id = fake.unique.uuid4()[:8].upper()  # Generate a unique short ID
    subscribed_events = random.sample(event_ids, k=random.randint(1, 3))
    registered_events = [
        {
            "eventId": event_id,
            "eventName": events_collection.find_one({"eventId": event_id})["eventName"],
            "registrationDate": fake.date_this_year().strftime('%Y-%m-%d')  # Corrected date format
        }
        for event_id in subscribed_events
    ]

    subscriber_data = {
        "subscriberId": subscriber_id,
        "name": fake.name(),
        "email": fake.email(),
        "phoneNumber": fake.phone_number(),
        "registeredEvents": registered_events,
        "subscriptionDate": fake.date_this_year().strftime('%Y-%m-%d')  # Corrected date format
    }

    subscribers_collection.insert_one(subscriber_data)

    # Update the corresponding event's attendees list
    for event in registered_events:
        events_collection.update_one(
            {"eventId": event["eventId"]},
            {"$push": {
                "attendees": {
                    "subscriberId": subscriber_id,
                    "name": subscriber_data["name"],
                    "email": subscriber_data["email"],
                    "registrationDate": event["registrationDate"]
                }
            }}
        )
#To be reviewed by Vijay

# Verify inserted data
print("Inserted Events:")
for event in events_collection.find():
    print(event)

print("\nInserted Subscribers:")
for subscriber in subscribers_collection.find():
    print(subscriber)
