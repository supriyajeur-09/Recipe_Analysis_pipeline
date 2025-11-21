from firebase_setup import init_firebase
from datetime import datetime
import random

db = init_firebase()


def generate_recipe_id(number):
    return f"recipe_{number}"

counter = 1  # start from Recipe_1



veg_pulao = {
    "name": "Veg Pulao",
    "description": "A fragrant vegetable pulao made with basmati rice and mixed veggies.",
    "servings": 2,
    "ingredients": [
        {"item": "Basmati rice", "quantity": "1 cup"},
        {"item": "Water", "quantity": "2 cups"},
        {"item": "Salt", "quantity": "¾ tsp"},
        {"item": "Oil or ghee", "quantity": "1.5 tbsp"},
        {"item": "Onion", "quantity": "1 small sliced"},
        {"item": "Green chilli", "quantity": "1 slit"},
        {"item": "Ginger-garlic paste", "quantity": "1 tsp"},
        {"item": "Carrot", "quantity": "½ cup diced"},
        {"item": "Green peas", "quantity": "¼ cup"},
        {"item": "French beans", "quantity": "¼ cup"},
        {"item": "Potato", "quantity": "½ small diced"},
        {"item": "Tomato", "quantity": "1 small chopped"},
        {"item": "Garam masala", "quantity": "½ tsp"},
        {"item": "Turmeric", "quantity": "¼ tsp"},
        {"item": "Fresh coriander", "quantity": "2 tbsp"},
        {"item": "Lemon", "quantity": "1 wedge"},
        {"item": "Whole spices", "quantity": "bay leaf, cloves, cinnamon, cardamom, cumin"}
    ],
    "steps": [
        "Rinse rice 2–3 times and soak for 15 minutes.",
        "Heat oil and add cumin + whole spices.",
        "Add onion and sauté until golden.",
        "Add ginger-garlic paste and chilli.",
        "Add vegetables and cook for 2 minutes.",
        "Add turmeric, garam masala, salt.",
        "Add rice and mix gently.",
        "Pour water and adjust salt.",
        "Pressure cook: 1 whistle + 5 mins low flame.",
        "Fluff & garnish with coriander."
    ],
    "author_id": "user_001",
    "tags": ["Indian", "Vegetarian", "Rice", "Quick Meal"],
    "created_on": datetime.now(),
    "updated_on": datetime.now(),
    "total_views": 0,
    "total_likes": 0,
    "total_cook_attempts": 0
}

veg_pulao_id = generate_recipe_id(counter)
db.collection("recipes").document(veg_pulao_id).set(veg_pulao)
print(f"Inserted Veg Pulao ✔ Document ID: {veg_pulao_id}")
counter += 1

recipe_names = [
    "Paneer Butter Masala", "Dal Tadka", "Masala Dosa", "Aloo Paratha",
    "Chicken Biryani", "Egg Curry", "Vegetable Khichdi", "Chole Bhature",
    "Pav Bhaji", "Sambar Rice", "Mango Lassi", "Poha", "Upma",
    "Fried Rice", "Jeera Rice", "Lemon Rice", "Curd Rice", "Veg Momos",
    "Chilli Paneer"
]

def create_fake_recipe(name):
    return {
        "name": name,
        "description": f"A delicious {name} recipe.",
        "servings": random.choice([1,2,3,4]),
        "ingredients": [
            {"item": "Salt", "quantity": "1 tsp"},
            {"item": "Oil", "quantity": "2 tbsp"},
            {"item": "Water", "quantity": "1 cup"}
        ],
        "steps": [
            "Prepare ingredients.",
            "Cook using standard process.",
            "Serve hot."
        ],
        "author_id": f"user_{random.randint(2,10)}",
        "tags": ["Indian", "Quick"],
        "created_on": datetime.now(),
        "updated_on": datetime.now(),
        "total_views": 0,
        "total_likes": 0,
        "total_cook_attempts": 0
    }

for name in recipe_names:
    doc_id = generate_recipe_id(counter)
    db.collection("recipes").document(doc_id).set(create_fake_recipe(name))
    print(f"Inserted: {name} ✔ Document ID: {doc_id}")
    counter += 1

print("Completed inserting all recipes!")

