import streamlit as st
from utils import extract_recipe_details, extract_timestamps
from youtube_scrapper import get_eng_recipe
from gemini import get_gemini_response, create_prompt_for_recipe, create_prompt_for_timestamps

# Initialize session state for selected timestamp
if 'selected_timestamp' not in st.session_state:
    st.session_state['selected_timestamp'] = None

def main():
    st.title("Recipe Helper")

    # User inputs the recipe name
    recipe_to_cook = st.text_input("Enter the name of the recipe", "shahi paneer")

    if recipe_to_cook:
        # Search for YouTube videos with English transcripts
        eng_recipes = get_eng_recipe(recipe_to_cook)
        if eng_recipes:
            # Let the user select a video
            video_titles = [recipe['title'] for recipe in eng_recipes]
            index_of_recipe_chosen = st.selectbox("Select a video", options=range(len(video_titles)), format_func=lambda x: video_titles[x])
            selected_video = eng_recipes[index_of_recipe_chosen]
            base_youtube_video_url = f"https://www.youtube.com/embed/{selected_video['id']}"

            # Extract recipe details
            recipe_prompt = create_prompt_for_recipe(selected_video['transcript'], recipe_to_cook)
            recipe_output = get_gemini_response(*recipe_prompt)
            steps, ingredients, servings, utensils = extract_recipe_details(recipe_output)

            # Display recipe details
            st.subheader("Recipe Details")
            st.write("Ingredients:", ingredients)
            st.write("Servings:", servings)
            st.write("Utensils:", utensils)

            # Generate and extract timestamps
            timestamp_prompt = create_prompt_for_timestamps(selected_video['transcript'], steps, recipe_to_cook)
            timestamp_output = get_gemini_response(*timestamp_prompt)
            timestamps = extract_timestamps(timestamp_output)
            print(timestamps)
            # Create buttons for each step to navigate the video
            st.subheader("Navigate through the video")
            for step, value in steps.items():
                if st.button(f"{step} : {steps[step]}"):
                    # Update the session state with the selected timestamp
                    st.session_state['selected_timestamp'] = timestamps[step]

            # Embed the YouTube video using HTML iframe with the selected timestamp
            if st.session_state['selected_timestamp'] is not None:
                youtube_video_url = f"{base_youtube_video_url}?start={int(st.session_state['selected_timestamp'])}&autoplay=1"
                st.components.v1.html(
                    f'<iframe width="560" height="315" src="{youtube_video_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
                    height=315,)
            else:
            # Embed the YouTube video without a specific start time
                st.components.v1.html(
                f'<iframe width="560" height="315" src="{base_youtube_video_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
                height=315,
                )

# Run the main function
if __name__ == "__main__":
    main()

