import pandas as pd

BASE_PATH = r"C:\Users\SUPRIYA\OneDrive\Documents\vscode\projectReceipe"

recipes = pd.read_csv(BASE_PATH + r"\recipe.csv")
ingredients = pd.read_csv(BASE_PATH + r"\ingredients.csv")
steps = pd.read_csv(BASE_PATH + r"\steps.csv")
interactions = pd.read_csv(BASE_PATH + r"\interactions.csv")


# Merge recipe names into interactions
interactions = interactions.merge(
    recipes[["recipe_id", "name"]],
    on="recipe_id",
    how="left"
)

print("=== ANALYTICS REPORT ===\n")

views = interactions[interactions["interaction_type"] == "view"]
top_viewed = views["name"].value_counts().head(10)

print("1️⃣  TOP 10 MOST VIEWED RECIPES:")
print(top_viewed, "\n")

likes = interactions[interactions["interaction_type"] == "like"]
top_liked = likes["name"].value_counts().head(10)

print("2️⃣  TOP 10 MOST LIKED RECIPES:")
print(top_liked, "\n")

ratings = interactions[interactions["interaction_type"] == "rating"]

if "rating" in ratings.columns:
    rating_avg = ratings.groupby("name")["rating"].mean().sort_values(ascending=False)
else:
    rating_avg = pd.Series(dtype=float)

print("3️⃣  AVERAGE RATINGS PER RECIPE:")
print(rating_avg.head(10), "\n")

common_ingredients = ingredients["item"].value_counts().head(10)

print("4️⃣  MOST COMMON INGREDIENTS:")
print(common_ingredients, "\n")

engagement_by_recipe = interactions.groupby("recipe_id").size().reset_index(name="engagement")

merged = ingredients.merge(engagement_by_recipe, on="recipe_id", how="left")
merged = merged.merge(recipes[["recipe_id", "name"]], on="recipe_id", how="left")

ingredient_engagement = merged.groupby("item")["engagement"].mean().fillna(0).sort_values(ascending=False)

print("5️⃣  INGREDIENTS MOST ASSOCIATED WITH HIGH ENGAGEMENT:")
print(ingredient_engagement.head(10), "\n")

prep_time_proxy = steps.merge(recipes[["recipe_id", "name"]], on="recipe_id")
prep_time_proxy = prep_time_proxy.groupby("name").size().sort_values(ascending=False)

print("6️⃣  RECIPES WITH MOST STEPS (LONGEST PREP TIME):")
print(prep_time_proxy.head(10), "\n")

likes_count = likes.groupby("recipe_id").size().reset_index(name="likes")
prep = steps.groupby("recipe_id").size().reset_index(name="num_steps")

corr_df = pd.merge(prep, likes_count, on="recipe_id", how="left").fillna(0)

if corr_df["likes"].nunique() > 1:
    correlation = corr_df["num_steps"].corr(corr_df["likes"])
else:
    correlation = 0.0

print("7️⃣  CORRELATION BETWEEN PREP TIME (STEPS) AND LIKES:")
print(f"Correlation: {correlation}\n")

all_engagement = interactions.groupby("name").size().sort_values(ascending=False)

print("8️⃣  RECIPES WITH HIGHEST OVERALL ENGAGEMENT:")
print(all_engagement.head(10), "\n")

user_engagement = interactions.groupby("user_id").size().sort_values(ascending=False)

print("9️⃣  TOP USERS BY TOTAL ACTIVITY:")
print(user_engagement.head(10), "\n")


difficulty = steps.merge(recipes[["recipe_id", "name"]], on="recipe_id")
difficulty = difficulty.groupby(["recipe_id", "name"]).size().reset_index(name="step_count")

difficulty["difficulty"] = pd.cut(
    difficulty["step_count"],
    bins=[0, 3, 7, 50],
    labels=["Easy", "Medium", "Hard"]
)

print("🔟  DIFFICULTY CLASSIFICATION BASED ON STEP COUNT:")
print(difficulty[["name", "step_count", "difficulty"]].head(1), "\n")

print("=== END OF ANALYTICS REPORT ===")

