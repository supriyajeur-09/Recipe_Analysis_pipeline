from firebase_setup import init_firebase
import pandas as pd

db = init_firebase()

#Extract
def fetch_collection(name):
    docs = db.collection(name).stream()
    return [ {**doc.to_dict(), "id": doc.id} for doc in docs ]

recipes_data = fetch_collection("recipes")
interactions_data = fetch_collection("interactions")

print("Fetched recipes:", len(recipes_data))
print("Fetched interactions:", len(interactions_data))

#Transform

recipe_rows = []
ingredients_rows = []
steps_rows = []
interactions_rows = []

for recipe in recipes_data:
    recipe_id = recipe["id"]

    # --- MAIN RECIPE TABLE ---
    recipe_rows.append({
        "recipe_id": recipe_id,
        "name": recipe["name"],
        "description": recipe["description"],
        "servings": recipe["servings"],
        "author_id": recipe["author_id"],
        "created_on": recipe["created_on"],
        "updated_on": recipe["updated_on"],
        "total_views": recipe.get("total_views", 0),
        "total_likes": recipe.get("total_likes", 0),
        "total_cook_attempts": recipe.get("total_cook_attempts", 0)
    })

    # --- INGREDIENTS TABLE ---
    for ing in recipe["ingredients"]:
        ingredients_rows.append({
            "recipe_id": recipe_id,
            "item": ing["item"],
            "quantity": ing["quantity"]
        })

    # --- STEPS TABLE ---
    for step_num, step_text in enumerate(recipe["steps"], start=1):
        steps_rows.append({
            "recipe_id": recipe_id,
            "step_number": step_num,
            "instruction": step_text
        })


# --- INTERACTIONS TABLE ---
for inter in interactions_data:
    interactions_rows.append({
        "interaction_id": inter["id"],
        "recipe_id": inter["recipe_id"],
        "user_id": inter["user_id"],
        "interaction_type": inter["interaction_type"],
        "timestamp": inter["timestamp"],
        "rating": inter.get("rating", None),
        "notes": inter.get("notes", None)
    })

#Load

pd.DataFrame(recipe_rows).to_csv("recipe.csv", index=False)
pd.DataFrame(ingredients_rows).to_csv("ingredients.csv", index=False)
pd.DataFrame(steps_rows).to_csv("steps.csv", index=False)
pd.DataFrame(interactions_rows).to_csv("interactions.csv", index=False)

print("CSV export completed successfully!")
print("Generated: recipe.csv, ingredients.csv, steps.csv, interactions.csv")
