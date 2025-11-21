from firebase_setup import init_firebase
from datetime import datetime
import random

db = init_firebase()

interaction_types = ["view", "like", "cook_attempt", "rating"]

users = [f"user_{i:03}" for i in range(1, 20)]
recipes = ["veg_pulao_01"] + [f"recipe_{i}" for i in range(1, 20)]

def add_interaction(recipe_id, user_id):
    interaction_type = random.choice(interaction_types)

    data = {
        "recipe_id": recipe_id,
        "user_id": user_id,
        "interaction_type": interaction_type,
        "timestamp": datetime.now()
    }

    if interaction_type == "rating":
        data["rating"] = random.randint(1, 5)

    if interaction_type == "cook_attempt":
        data["notes"] = random.choice([
            "Turned out great!", 
            "A little salty", 
            "Very tasty", 
            "Will try again!"
        ])

    db.collection("interactions").add(data)


# Generate 300 interactions
for _ in range(300):
    add_interaction(
        recipe_id=random.choice(recipes),
        user_id=random.choice(users)
    )

print("Inserted 300 user interactions ✔")

