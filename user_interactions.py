from firebase_setup import init_firebase
from datetime import datetime

db = init_firebase()

def add_interaction(recipe_id, user_id, interaction_type, notes=None):
    data = {
        "recipe_id": recipe_id,
        "user_id": user_id,
        "interaction_type": interaction_type,
        "timestamp": datetime.now()
    }
    if notes:
        data["notes"] = notes

    db.collection("interactions").add(data)
    print(f"Added interaction: {interaction_type}")

# Simulating data
add_interaction("veg_pulao_01", "user_001", "view")
add_interaction("veg_pulao_01", "user_001", "like")
add_interaction("veg_pulao_01", "user_002", "cook_attempt", notes="Came out very tasty!")
