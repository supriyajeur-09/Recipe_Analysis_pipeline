
# 🍽️ Firebase Recipe Analytics Pipeline  


Author- Supriya Gurushant jeur
Email - supriyajeur95@gmail.com
Batch - Data Engineering

# Data Modeling
### 1. Recipes

Stores recipe metadata:

- recipe_id  

- name  

- description  

- servings  

- ingredients[]  

- steps[]  

- tags  

- author_id  

- created_on  

- updated_on  

- total_views  

- total_likes  

- total_cook_attempts

### 2. Users

Stores user details:

- user_id  

- name  

- email  

- favourite_recipes[]  

- created_on  

- last_login

### 3. Interactions

Stores user engagement:

- interaction_id  

- recipe_id  

- user_id  

- interaction_type (view / like / rating / cook_attempt)  

- timestamp  

- notes  

- rating (optional)

This data model is clean, scalable, analytics-ready, and fully aligned with the requirements of your Firebase-based Recipe Analytics Pipeline.
This Task uses a three-entity data model designed for recipe analytics on Firebase Firestore. The model supports recipe creation, ingredient & step structuring, and user-driven interactions such as views, likes, ratings, and cook attempts.

# ERD

![alt text](er_diagram.png)

---
###  Firebase Source Data Setup

Scripts created:
- firebase_setup.py  
- seed_recipes.py  
- create_users.py  
- generate_interactions.py  

Data added:
- 1 real Veg Pulao recipe  
- 20 synthetic recipes  
- 20 users  
- 300+ interactions  

Firestore collections:
- recipes  
- users  
- interactions  

---

# Instructions for running the pipeline

### Setup Environment

- Install Dependencies

`pip install firebase-admin pandas`

- Add Firebase Credentials

Place your Firebase Admin SDK file as:

`serviceAccountKey.json`

Used by `firebase_setup.py` to initialize Firestore.\
📄


- Start Firestore Emulator

This project uses **local Firestore** (no billing).

- Start Emulato

`firebase emulators:start`

- Point Python to Emulator

On a new terminal:

`set FIRESTORE_EMULATOR_HOST=localhost:8080`

This ensures every script reads/writes to emulator, not real Firestore.


- Seed Firestore with Data (Users + Recipes + Interactions)**

- 3.1 Insert Users

`python create_users.py`

This generates synthetic users
📄

create_users

- Insert Recipes

`python seed_recipes.py`

This loads:

-   1 real Veg Pulao recipe

-   19 synthetic recipes

Each recipe contains ingredients, steps, metadata.\
📄

seed_recipes

-  Generate 300 Interactions

`python generate_interactions.py`

Creates random:

-   views

-   likes

-   ratings

-   cook_attempts


#   ETL Pipeline

Script: export_firestore_to_csv.py

This project follows a standard Extract → Transform → Load workflow.

### Extract Phase

The first step in the ETL process was extracting data from Firestore. Since I was working locally and did not use any billing-enabled resources, I used the Firebase Firestore Emulator.

1.  I started the emulator using

2.  firebase emulators:start

3.  In a new terminal, I pointed my Python application to the emulator by setting

4.  set FIRESTORE_EMULATOR_HOST=localhost:8080

5.  I created a seed_recipes.py file which inserts the main recipe (Veg Pulao) and around 20 synthetic recipes into the recipes collection.

6.  When I ran the script, all recipe documents were inserted with the recipe name as the document ID (for example: veg_pulao, paneer_butter_masala, etc.).

This completed the data extraction part, and all the recipe data was ready inside Firestore Emulator for processing.

### Transform Phase

Next, I built my Apache Beam pipeline to transform the extracted recipe data.

This was the core part of Module 3.

Here are the transformations I performed:

-   First, I fetched all recipe documents from Firestore using the Firebase Admin SDK.

-   Beam converted the fetched list of recipes into a PCollection.

-   I cleaned and structured the data so that all fields were consistent.

-   I applied various transformations like:

-   Filtering recipes (for example, veg recipes or quick recipes)

-    Mapping data to specific fields (like extracting only names, tags, or likes)

-   Counting the number of recipes

- Aggregating data (for example, total veg recipes, total tags, etc.)

These transformations helped me understand how Apache Beam processes data in a distributed and scalable way, even when running locally.

### Load Phase

The final step of the ETL process was loading the transformed data.

Depending on my pipeline logic, the output was handled in different ways:

-   Most transformed results were printed directly in the terminal.

This helped me verify the output immediately.

-   I also had the option to write the results back to Firestore Emulator (like storing statistics).

-   Beam also allows writing to files such as JSON or CSV, but for today's module, I mainly focused on console output.

This completed the Load phase of my ETL process.


#  Data Quality Validation

Script: data_quality_validator.py

Validation Rules:

### Recipes
- recipe_id required  
- name required  
- servings > 0  
- views/likes/attempts >= 0  
- must contain ingredients  
- must contain steps  

### Ingredients
- item non-empty  
- quantity non-empty  

### Steps
- step_number > 0  
- instruction non-empty  

### Interactions
- valid interaction_type  
- rating (1–5)  
- timestamp required  
- user_id required  
- recipe_id required  

Output:

# data_quality_report.txt

===== DATA QUALITY VALIDATION REPORT =====

===== SUMMARY =====

Valid recipes: 20

Invalid recipes: 0

Valid ingredients: 74

Invalid ingredients: 0

Valid steps: 67

Invalid steps: 0

Valid interactions: 300

Invalid interactions: 0


#  Analytics & Insights

The following insights were generated using Python-based analytics on the processed recipe dataset.\
This section highlights recipe popularity, ingredient trends, user behavior, and difficulty classification.

* * * * *

### Top 10 Most Viewed Recipes**

Most frequently viewed recipes in the dataset.

| Recipe | Views |
| --- | --- |
| Masala Dosa | 7 |
| Vegetable Khichdi | 6 |
| Pav Bhaji | 5 |
| Dal Tadka | 4 |
| Veg Pulao | 4 |
| Paneer Butter Masala | 4 |
| Chicken Biryani | 4 |
| Fried Rice | 3 |
| Chole Bhature | 2 |
| Lemon Rice | 2 |

### Top 10 Most Liked Recipes**

Recipes receiving the highest number of likes.

| Recipe | Likes |
| --- | --- |
| Mango Lassi | 11 |
| Veg Momos | 7 |
| Egg Curry | 6 |
| Pav Bhaji | 6 |
| Sambar Rice | 5 |
| Dal Tadka | 5 |
| Upma | 5 |
| Aloo Paratha | 5 |
| Vegetable Khichdi | 4 |
| Paneer Butter Masala | 4 |


### Average Ratings per Recipe**

Mean rating per recipe.

| Recipe | Avg Rating |
| --- | --- |
| Curd Rice | 4.0 |
| Paneer Butter Masala | 4.0 |
| Egg Curry | 4.0 |
| Veg Pulao | 3.63 |
| Aloo Paratha | 3.5 |
| Fried Rice | 3.5 |
| Vegetable Khichdi | 3.5 |
| Jeera Rice | 3.33 |
| Chole Bhature | 3.2 |
| Masala Dosa | 3.0 |

### Most Common Ingredients**

Most frequently used ingredients across all recipes.

| Ingredient | Count |
| --- | --- |
| Salt | 20 |
| Water | 20 |
| Oil | 19 |
| Potato | 1 |
| Whole spices | 1 |
| Lemon | 1 |
| Fresh coriander | 1 |
| Turmeric | 1 |
| Garam masala | 1 |
| Tomato | 1 |

### Ingredients Most Associated With High Engagement**

Ingredients found in recipes with the highest combined likes + views.

| Ingredient | Engagement |
| --- | --- |
| Basmati rice | 19.0 |
| Lemon | 19.0 |
| Turmeric | 19.0 |
| Tomato | 19.0 |
| Potato | 19.0 |
| Onion | 19.0 |
| Oil or ghee | 19.0 |
| Carrot | 19.0 |
| Whole spices | 19.0 |
| Green peas | 19.0 |

### Recipes With Most Steps (Longest Prep Time)**

| Recipe | Steps |
| --- | --- |
| Veg Pulao | 10 |
| Aloo Paratha | 3 |
| Chicken Biryani | 3 |
| Veg Momos | 3 |
| Upma | 3 |
| Sambar Rice | 3 |
| Poha | 3 |
| Pav Bhaji | 3 |
| Paneer Butter Masala | 3 |
| Masala Dosa | 3 |

### Correlation Between Prep Time and Likes**

Correlation coefficient (steps vs. likes):

# Correlation: -0.1143**

### Recipes With Highest Overall Engagement**

(views + likes + ratings interactions)

| Recipe | Engagement |
| --- | --- |
| Mango Lassi | 26 |
| Masala Dosa | 21 |
| Veg Pulao | 19 |
| Dal Tadka | 17 |
| Chicken Biryani | 16 |
| Aloo Paratha | 16 |
| Egg Curry | 15 |
| Paneer Butter Masala | 15 |
| Pav Bhaji | 15 |
| Sambar Rice | 15 |

### Top Users by Total Activity**

Users with the highest number of interactions.

| User ID | Actions |
| --- | --- |
| user_016 | 28 |
| user_013 | 23 |
| user_018 | 19 |
| user_011 | 19 |
| user_012 | 18 |
| user_005 | 17 |
| user_015 | 17 |
| user_002 | 17 |
| user_004 | 16 |
| user_009 | 16 |

### Difficulty Classification Based on Step Count

Difficulty levels were assigned using step-based rules:

-   **1--3 steps → Easy**

-   **4--6 steps → Medium**

-   **7+ steps → Hard**

| Recipe | Steps | Difficulty |
| --- | --- | --- |
| Veg Pulao | 10 | Hard |

#  Known constraints or limitations

1. Emulator Only (No Cloud Mode)
All scripts use the Firestore Emulator.
To run in production, remove:
set FIRESTORE_EMULATOR_HOST=localhost:8080

2. Synthetic Data
Recipes, users, and interactions are artificially generated.
Analytics may not reflect real-world patterns.

3. No Real Authentication
Users are fake and not linked to Firebase Auth.

4. Timestamps Depend on Local System
All timestamps use datetime.now() from Python scripts.

5. Analytics Uses CSV, Not Firestore
Pipeline runs on exported CSV instead of directly on Firestore documents.

6. Simple Difficulty Heuristic
Difficulty = steps count:
1–3: Easy
4–7: Medium
8+: Hard

#  conclusion 
This project successfully demonstrates a full ETL workflow using the Firestore Emulator, Python scripts, and Apache Beam. Recipe and interaction data were extracted, cleaned, normalized into CSV tables, validated, and analyzed to generate useful insights. The system works end-to-end without any cloud billing and provides a solid foundation for future scaling, dashboarding, or real Firebase deployment.

# 🎉 Project Status
Recipe Analytics Pipeline Done Sucessfully!


