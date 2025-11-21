import pandas as pd


recipes = pd.read_csv("recipe.csv")
ingredients = pd.read_csv("ingredients.csv")
steps = pd.read_csv("steps.csv")
interactions = pd.read_csv("interactions.csv")

report_lines = []
report_lines.append("===== DATA QUALITY VALIDATION REPORT =====\n")


def add_issue(issue):
    report_lines.append(issue)


valid_recipes = 0
invalid_recipes = 0

for index, row in recipes.iterrows():

    issues = []

    if pd.isna(row["recipe_id"]) or row["recipe_id"] == "":
        issues.append("Missing recipe_id")

    if pd.isna(row["name"]) or row["name"] == "":
        issues.append("Missing recipe name")

    if row["servings"] <= 0:
        issues.append("Invalid servings (must be > 0)")
    
    if row["total_views"] < 0:
        issues.append("Invalid total_views (must be >= 0)")

    if row["total_likes"] < 0:
        issues.append("Invalid total_likes (must be >= 0)")

    if row["total_cook_attempts"] < 0:
        issues.append("Invalid total_cook_attempts (must be >= 0)")

    # Cross-check if steps exist
    if len(steps[steps["recipe_id"] == row["recipe_id"]]) == 0:
        issues.append("Missing steps for recipe")

    # Cross-check if ingredients exist
    if len(ingredients[ingredients["recipe_id"] == row["recipe_id"]]) == 0:
        issues.append("Missing ingredients for recipe")

    if issues:
        invalid_recipes += 1
        add_issue(f"[RECIPE INVALID] recipe_id={row['recipe_id']} → {', '.join(issues)}")
    else:
        valid_recipes += 1



valid_ing = 0
invalid_ing = 0

for index, row in ingredients.iterrows():

    issues = []

    if pd.isna(row["item"]) or row["item"] == "":
        issues.append("Missing ingredient item")

    if pd.isna(row["quantity"]) or row["quantity"] == "":
        issues.append("Missing ingredient quantity")

    if issues:
        invalid_ing += 1
        add_issue(f"[INGREDIENT INVALID] recipe_id={row['recipe_id']} item={row['item']} → {', '.join(issues)}")
    else:
        valid_ing += 1

valid_steps = 0
invalid_steps = 0

for index, row in steps.iterrows():
    issues = []

    if row["step_number"] <= 0:
        issues.append("step_number must be positive")

    if pd.isna(row["instruction"]) or row["instruction"] == "":
        issues.append("Empty instruction")

    if issues:
        invalid_steps += 1
        add_issue(f"[STEP INVALID] recipe_id={row['recipe_id']} step={row['step_number']} → {', '.join(issues)}")
    else:
        valid_steps += 1

valid_interactions = 0
invalid_interactions = 0

allowed_types = ["view", "like", "cook_attempt", "rating"]

for index, row in interactions.iterrows():

    issues = []

    if row["interaction_type"] not in allowed_types:
        issues.append("Invalid interaction_type")

    if row["interaction_type"] == "rating":
        if row["rating"] < 1 or row["rating"] > 5:
            issues.append("rating out of range (1–5)")

    if pd.isna(row["timestamp"]):
        issues.append("Missing timestamp")

    if pd.isna(row["user_id"]) or row["user_id"] == "":
        issues.append("Missing user_id")

    if pd.isna(row["recipe_id"]) or row["recipe_id"] == "":
        issues.append("Missing recipe_id")

    if issues:
        invalid_interactions += 1
        add_issue(f"[INTERACTION INVALID] id={row['interaction_id']} → {', '.join(issues)}")
    else:
        valid_interactions += 1



report_lines.append("\n===== SUMMARY =====\n")
report_lines.append(f"Valid recipes: {valid_recipes}")
report_lines.append(f"Invalid recipes: {invalid_recipes}\n")

report_lines.append(f"Valid ingredients: {valid_ing}")
report_lines.append(f"Invalid ingredients: {invalid_ing}\n")

report_lines.append(f"Valid steps: {valid_steps}")
report_lines.append(f"Invalid steps: {invalid_steps}\n")

report_lines.append(f"Valid interactions: {valid_interactions}")
report_lines.append(f"Invalid interactions: {invalid_interactions}\n")


with open("data_quality_report.txt", "w") as f:
    f.write("\n".join(report_lines))

print("Data quality validation complete!")
print("Report saved as: data_quality_report.txt")
