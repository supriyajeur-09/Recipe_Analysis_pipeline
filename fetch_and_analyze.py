from firebase_setup import init_firebase

db = init_firebase()

# Fetch recipe
recipe = db.collection("recipes").document("veg_pulao_01").get()
print("Recipe:", recipe.to_dict())

# Fetch interactions
interactions = db.collection("interactions").where("recipe_id", "==", "veg_pulao_01").stream()

print("\n--- Interactions ---")
for i in interactions:
    print(i.to_dict())
