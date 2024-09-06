import streamlit as st
import google.generativeai as genai

# Configure the API key
GOOGLE_API_KEY = "AIzaSyBHwULJ6COMJ32xLGbOwy797Q2CiFkz35c"
genai.configure(api_key=GOOGLE_API_KEY)

# Define Ingredient class
class Ingredient:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"{self.name}"

# Define Recipe class
class Recipe:
    def __init__(self, name, ingredients, cuisine, flavor):
        self.name = name
        self.ingredients = ingredients  
        self.cuisine = cuisine
        self.flavor = flavor

    def generate_recipe_prompt(self):
        ingredient_names = ", ".join([ingredient.name for ingredient in self.ingredients])
        return f"Provide me with a {self.cuisine} recipe that is {self.flavor} flavored using the following ingredients: {ingredient_names} and divide the recipe into Title,Ingredients,Directions to cook"

    def __str__(self):
        ingredients_list = ", ".join([str(ingredient) for ingredient in self.ingredients])
        return f"Recipe Name: {self.name}\nCuisine: {self.cuisine}\nFlavor: {self.flavor}\nIngredients: {ingredients_list}"

def parse_recipe_string(recipe_string):
    
    sections = recipe_string.split("\n\n")
    
    
    title = sections[0].split("\n")[0].strip('# ').strip()

    description = sections[0].split("\n", 1)[1].strip() if len(sections[0].split("\n")) > 1 else ""

    ingredients_section = sections[1] if len(sections) > 1 else ""
    ingredients = [line.strip() for line in ingredients_section.split('\n')[1:] if line.strip()]

    directions_section = sections[2] if len(sections) > 2 else ""
    directions = [line.strip() for line in directions_section.split('\n')[1:] if line.strip()]

    tips_section = sections[3] if len(sections) > 3 else ""
    tips = [line.strip() for line in tips_section.split('\n')[1:] if line.strip()]

    return title, description, ingredients, directions, tips

def main():
    st.title("Custom Recipe Generator")

    st.header("Enter Recipe Details")

    recipe_name = st.text_input("Recipe Name")

    cuisine = st.selectbox("Cuisine", ["Italian", "Chinese", "Indian", "Mexican", "French", "American"])

    flavor = st.selectbox("Flavor", ["Spicy", "Sweet", "Savory", "Sour", "Bitter", "Umami"])

    if 'ingredients' not in st.session_state:
        st.session_state.ingredients = []

    ingredient_name = st.text_input("Ingredient Name")

    if st.button("Add Ingredient"):
        if ingredient_name:
            ingredient = Ingredient(ingredient_name)
            st.session_state.ingredients.append(ingredient)
            st.success(f"Added {ingredient_name} to the recipe")

    if st.button("Generate Recipe"):
        if not st.session_state.ingredients:
            st.error("Please enter at least one ingredient.")
        else:
            recipe = Recipe(recipe_name, st.session_state.ingredients, cuisine, flavor)
            st.write(recipe)

            model = genai.GenerativeModel('gemini-1.5-flash')
            input_prompt = recipe.generate_recipe_prompt()
            response = model.generate_content(input_prompt)
            
            modified_text = response.text.replace('**', '').replace('*', '')
            
            st.subheader("Generated Recipe:")
            st.write(modified_text.encode('utf-8').decode('utf-8'))

            title, description, ingredients, directions, tips = parse_recipe_string(modified_text)
            
           

if __name__ == "__main__":
    main()
