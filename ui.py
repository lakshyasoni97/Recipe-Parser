import streamlit as st
from utils import extract_recipe_details, extract_timestamps
from youtube_scrapper import get_eng_recipe
from gemini import get_gemini_response, create_prompt_for_recipe, create_prompt_for_timestamps, create_prompt_for_question_answering
from config import USER_CREDENTIALS

def check_login(username, password):
    """Check if the username and password are correct."""
    return username == USER_CREDENTIALS["username"] and password == USER_CREDENTIALS["password"]

def login_form():
    """Display the login form and handle authentication."""
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    gemini_api_key = st.sidebar.text_input("Gemini API Key")
    if st.sidebar.button("Login"):
        if check_login(username, password):
            st.session_state["authenticated"] = True
            st.session_state["gemini_api_key"] = gemini_api_key 
            st.rerun()
        else:
            st.sidebar.error("Invalid username or password.")

def main_app(gemini_api_key):
    st.title("Recipe Helper")
    
    # Initialize session state variables if they don't exist
    if 'eng_recipes' not in st.session_state:
        st.session_state['eng_recipes'] = None
    if 'recipe_details_fetched' not in st.session_state:
        st.session_state['recipe_details_fetched'] = False
    if 'last_selected_recipe_index' not in st.session_state:
        st.session_state['last_selected_recipe_index'] = None
    if 'selected_video' not in st.session_state:
        st.session_state['selected_video'] = None

    recipe_to_cook = st.text_input("Enter the name of the recipe")
    if recipe_to_cook:
        if st.session_state.eng_recipes is None or st.session_state.recipe_to_cook != recipe_to_cook:
            with st.spinner('Searching for recipes...'):
                try:
                    st.session_state.eng_recipes = get_eng_recipe(f"{recipe_to_cook} recipe")
                    st.session_state.recipe_to_cook = recipe_to_cook
                    st.session_state.recipe_details_fetched = False
                    st.session_state.last_selected_recipe_index = None
                except Exception as e:
                    st.error("Failed to fetch recipes. Please check your internet connection and try again.")
                    st.error(f"Error details: {e}")

    if st.session_state.eng_recipes:
        video_titles = [recipe['title'] for recipe in st.session_state.eng_recipes]
        index_of_recipe_chosen = st.selectbox("Select a video", options=range(len(video_titles)), format_func=lambda x: video_titles[x])

        if index_of_recipe_chosen != st.session_state.last_selected_recipe_index:
            st.session_state.recipe_details_fetched = False
            st.session_state.last_selected_recipe_index = index_of_recipe_chosen
            st.session_state.selected_video = st.session_state.eng_recipes[index_of_recipe_chosen]

        if st.session_state.selected_video and st.button('Fetch Recipe Details'):
            with st.spinner('Fetching recipe details...'):
                try:
                    embed_youtube_video(f"https://www.youtube.com/embed/{st.session_state.selected_video['id']}")
                    steps, ingredients, servings, utensils = fetch_recipe_details(st.session_state.selected_video, recipe_to_cook, gemini_api_key)
                    st.session_state.steps = steps
                    st.session_state.ingredients = ingredients
                    st.session_state.servings = servings
                    st.session_state.utensils = utensils
                    display_recipe_details(st.session_state.ingredients, st.session_state.servings, st.session_state.utensils )
                    timestamps = fetch_recipe_steps_timestamps(st.session_state.selected_video, st.session_state.steps, recipe_to_cook, gemini_api_key)
                    st.session_state.timestamps = timestamps
                    display_steps_timestamps(st.session_state.steps, st.session_state.timestamps)
                    st.session_state.recipe_details_fetched = True
                except Exception as e:
                    st.error("An error occurred while processing the recipe details. Please try again.")
                    st.error(f"Error details: {e}")

    # Question-Answering Section
    if st.session_state.get('recipe_details_fetched', False):
        st.subheader("Ask a Chef")
        user_question = st.text_input("Enter your question about the recipe", key='user_question')
        if st.button("Ask", key='ask_chef'):
            with st.spinner("Thinking..."):
                try:
                    qa_role, qa_prompt = create_prompt_for_question_answering(
                        st.session_state.selected_video['transcript'], 
                        recipe_to_cook, 
                        user_question)
                    answer = get_gemini_response(qa_role, qa_prompt, gemini_api_key)
                    st.session_state['chef_answer'] = answer
                except Exception as e:
                    st.error("Failed to process your question. Please try again.")
                    st.error(f"Error details: {e}")
        if 'chef_answer' in st.session_state:
            st.write(st.session_state['chef_answer'])
            embed_youtube_video(f"https://www.youtube.com/embed/{st.session_state.selected_video['id']}")
            display_recipe_details(st.session_state.ingredients, st.session_state.servings, st.session_state.utensils )
            display_steps_timestamps(st.session_state.steps, st.session_state.timestamps)
            
            

def main():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if st.session_state['authenticated']:
        main_app(st.session_state['gemini_api_key'])
    else:
        login_form()

def fetch_recipe_details(selected_video, recipe_to_cook, gemini_api_key):
    recipe_prompt = create_prompt_for_recipe(selected_video['transcript'], recipe_to_cook)
    recipe_output = get_gemini_response(*recipe_prompt, gemini_api_key)
    return extract_recipe_details(recipe_output)

def fetch_recipe_steps_timestamps(selected_video, steps, recipe_to_cook, gemini_api_key):
    timestamp_prompt = create_prompt_for_timestamps(selected_video['transcript'], steps, recipe_to_cook)
    timestamp_output = get_gemini_response(*timestamp_prompt, gemini_api_key)
    return extract_timestamps(timestamp_output)

def display_recipe_details(ingredients, servings, utensils):
    st.subheader("Recipe Details")
    st.write("Ingredients:", ingredients)
    st.write("Servings:", servings)
    st.write("Utensils:", utensils)

def display_steps_timestamps(steps, timestamps):
    st.subheader("Steps and Timestamps")
    for step, value in steps.items():
        st.markdown(f"**{step}**: {value} - Timestamp: {timestamps[step]}")

def embed_youtube_video(base_youtube_video_url):
    st.components.v1.html(
        f'<iframe width="560" height="315" src="{base_youtube_video_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
        height=315,
    )

if __name__ == "__main__":
    main()
