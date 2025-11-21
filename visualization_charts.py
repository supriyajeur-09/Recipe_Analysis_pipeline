import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_PATH = r"C:\Users\SUPRIYA\OneDrive\Documents\vscode\projectReceipe"

# Load CSVs
recipes = pd.read_csv(BASE_PATH + r"\recipe.csv")
ingredients = pd.read_csv(BASE_PATH + r"\ingredients.csv")
steps = pd.read_csv(BASE_PATH + r"\steps.csv")
interactions = pd.read_csv(BASE_PATH + r"\interactions.csv")

# Merge names into interactions
interactions = interactions.merge(
    recipes[["recipe_id", "name"]],
    on="recipe_id",
    how="left"
)

views = interactions[interactions["interaction_type"] == "view"]
top_viewed = views["name"].value_counts().head(10)

plt.figure(figsize=(10, 5))
top_viewed.plot(kind='barh', color='royalblue')
plt.title("Top 10 Most Viewed Recipes")
plt.xlabel("Views")
plt.ylabel("Recipe")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("chart_top_viewed.png")
plt.show()


likes = interactions[interactions["interaction_type"] == "like"]
top_liked = likes["name"].value_counts().head(10)

plt.figure(figsize=(10, 5))
top_liked.plot(kind='barh', color='orange')
plt.title("Top 10 Most Liked Recipes")
plt.xlabel("Likes")
plt.ylabel("Recipe")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("chart_top_liked.png")
plt.show()


ratings = interactions[interactions["interaction_type"] == "rating"]
rating_avg = ratings.groupby("name")["rating"].mean().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 5))
rating_avg.plot(kind="bar", color="green")
plt.title("Top 10 Average Rated Recipes")
plt.ylabel("Average Rating")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("chart_avg_ratings.png")
plt.show()


common_ingredients = ingredients["item"].value_counts().head(10)

plt.figure(figsize=(10, 5))
common_ingredients.plot(kind="barh", color="purple")
plt.title("Most Common Ingredients")
plt.xlabel("Count")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("chart_common_ingredients.png")
plt.show()


engagement_by_recipe = interactions.groupby("recipe_id").size().reset_index(name="engagement")

merged = ingredients.merge(engagement_by_recipe, on="recipe_id", how="left")
ingredient_engagement = merged.groupby("item")["engagement"].mean().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 5))
ingredient_engagement.plot(kind="bar", color="teal")
plt.title("Top Ingredients by Engagement")
plt.ylabel("Engagement Score")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("chart_ingredient_engagement.png")
plt.show()


# ========= CHART 6: Recipes with Most Steps =========
prep_time_proxy = steps.merge(recipes[["recipe_id", "name"]], on="recipe_id")
prep_time_proxy = prep_time_proxy.groupby("name").size().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 5))
prep_time_proxy.plot(kind="bar", color="brown")
plt.title("Recipes with Most Steps")
plt.ylabel("Number of Steps")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("chart_most_steps.png")
plt.show()


# ========= CHART 7: Steps vs Likes Correlation =========
likes_count = likes.groupby("recipe_id").size().reset_index(name="likes")
prep = steps.groupby("recipe_id").size().reset_index(name="num_steps")

corr_df = pd.merge(prep, likes_count, on="recipe_id", how="left").fillna(0)

plt.figure(figsize=(6, 6))
sns.scatterplot(data=corr_df, x="num_steps", y="likes", color="red")
plt.title("Correlation: Steps vs Likes")
plt.xlabel("Number of Steps")
plt.ylabel("Likes")
plt.tight_layout()
plt.savefig("chart_correlation_steps_likes.png")
plt.show()


# ========= CHART 8: Highest Engagement Recipes =========
all_engagement = interactions.groupby("name").size().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 5))
all_engagement.plot(kind="barh", color="darkblue")
plt.title("Top Recipes by Engagement")
plt.xlabel("Engagement")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("chart_overall_engagement.png")
plt.show()


# ========= CHART 9: Top Users by Activity =========
user_engagement = interactions.groupby("user_id").size().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 5))
user_engagement.plot(kind="bar", color="magenta")
plt.title("Top 10 Active Users")
plt.ylabel("Actions")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("chart_top_users.png")
plt.show()


# ========= CHART 10: Difficulty Pie Chart =========
difficulty = steps.merge(recipes[["recipe_id", "name"]], on="recipe_id")
difficulty = difficulty.groupby(["recipe_id", "name"]).size().reset_index(name="step_count")

difficulty["difficulty"] = pd.cut(
    difficulty["step_count"],
    bins=[0, 3, 7, 50],
    labels=["Easy", "Medium", "Hard"]
)

difficulty_count = difficulty["difficulty"].value_counts()

plt.figure(figsize=(6, 6))
difficulty_count.plot(kind="pie", autopct="%1.1f%%", colors=["lightgreen", "gold", "red"])
plt.title("Recipe Difficulty Distribution")
plt.ylabel("")
plt.tight_layout()
plt.savefig("chart_difficulty_pie.png")
plt.show()

