from firebase_setup import init_firebase
from datetime import datetime
import random

db = init_firebase()

# Sample names for generating users
names = [
    "Aarav", "Vihaan", "Reyansh", "Mohammed", "Advait",
    "Sai", "Arjun", "Ayan", "Ishaan", "Kabir",
    "Anaya", "Siya", "Aadhya", "Myra", "Anika",
    "Diya", "Sara", "Amaira", "Ira", "Veda"
]

def create_user(user_id, name):
    return {
        "user_id": user_id,
        "name": name,
        "email": f"{name.lower()}@example.com",
        "created_on": datetime.now(),
        "last_login": datetime.now(),
        "favourite_recipes": []
    }

# Generate 20 synthetic users
for i, name in enumerate(names):
    user_id = f"user_{i+1:03}"
    user_doc = create_user(user_id, name)
    db.collection("users").document(user_id).set(user_doc)

print("20 Users inserted successfully into Firestore ✔")
