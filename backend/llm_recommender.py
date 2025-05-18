from dotenv import load_dotenv
import os
import openai

load_dotenv()  # 🔥 loads variables from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")
def filter_relevant_recipes(patient, recipes):
    # Match on flavor_profile and symptoms
    patient_flavors = patient.taste_preferences.lower().split(", ")
    patient_symptoms = patient.symptoms.lower().split(", ")

    relevant = []
    for recipe in recipes:
        match_score = 0
        if recipe.flavor_profile.lower() in patient_flavors:
            match_score += 1
        for symptom in patient_symptoms:
            if symptom in recipe.suitable_for.lower():
                match_score += 1
        if match_score > 0:
            relevant.append((match_score, recipe))

    # Sort and return top 5
    relevant.sort(reverse=True, key=lambda x: x[0])
    return [r for _, r in relevant[:5]]


def generate_recommendation(patient, feedbacks, clinical_results, recipes):
    try:
        print("🔍 Matching recipes...")
        top_recipes = filter_relevant_recipes(patient, recipes)

        # Group feedbacks by recipe name
        feedback_map = {}
        for fb in feedbacks:
            recipe_key = fb.recipe_name.strip().lower()
            feedback_map.setdefault(recipe_key, []).append(fb.feedback_text.strip())

        # Build formatted recipe list with inline feedback
        recipe_list = ""
        for r in top_recipes:
            key = r.name.strip().lower()
            feedback_summary = "\n    - " + "\n    - ".join(feedback_map.get(key, [])) if key in feedback_map else " No prior feedback."
            recipe_list += f"\n- {r.name}: {r.description} (Flavor: {r.flavor_profile}, Suitable for: {r.suitable_for})\n  Previous Feedback:{feedback_summary}\n"

        # Overall feedback summary
        feedback_summary_all = "\n".join(f"- {f.recipe_name}: {f.feedback_text}" for f in feedbacks) or "No general feedback available."
        clinical_summary = clinical_results.result_summary if clinical_results else "No clinical results available."

        user_prompt = f"""
You are a dietary assistant for cancer patients with taste disorders.

Patient Profile:
- Name: {patient.name}
- Taste Preferences: {patient.taste_preferences}
- Texture Likes: {patient.texture_likes}
- Dietary Restrictions: {patient.dietary_restriction}
- Symptoms: {patient.symptoms}
- Known Taste Deficits: {patient.known_deficits}
- Sensory Scores (Sweet, Salty, Bitter, Umami, Sour): 
  {patient.sensory_sweet}, {patient.sensory_salty}, {patient.sensory_bitter}, {patient.sensory_umami}, {patient.sensory_sour}

Recent Meal Feedback (All):
{feedback_summary_all}

Clinical Summary:
{clinical_summary}

Top Matching Recipes (with previous feedback if any):
{recipe_list}

➡️ Based on this data, suggest 1–5 recipes from the list or modify them to suit this patient's preferences, restrictions, and past experiences.
"""

        print("🔍 Sending to OpenAI...")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4
            messages=[
                {"role": "system", "content": "You are a helpful clinical dietary assistant."},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )

        print("✅ OpenAI responded.")
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        print("❌ LLM ERROR:", str(e))
        raise