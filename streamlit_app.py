# import streamlit as st
# from utils import extract_recipe_details, extract_timestamps
# from youtube_scrapper import get_eng_recipe
# from gemini import get_gemini_response, create_prompt_for_recipe, create_prompt_for_timestamps

# # Initialize session state for selected timestamp
# if 'selected_timestamp' not in st.session_state:
#     st.session_state['selected_timestamp'] = None

# def main():
#     st.title("Recipe Helper")

#     # User inputs the recipe name
#     recipe_to_cook = st.text_input("Enter the name of the recipe", "shahi paneer")

#     if recipe_to_cook:
#         # Search for YouTube videos with English transcripts
#         eng_recipes = get_eng_recipe(recipe_to_cook)
#         if eng_recipes:
#             # Let the user select a video
#             video_titles = [recipe['title'] for recipe in eng_recipes]
#             index_of_recipe_chosen = st.selectbox("Select a video", options=range(len(video_titles)), format_func=lambda x: video_titles[x])
#             selected_video = eng_recipes[index_of_recipe_chosen]
#             base_youtube_video_url = f"https://www.youtube.com/embed/{selected_video['id']}"

#             # Extract recipe details
#             recipe_prompt = create_prompt_for_recipe(selected_video['transcript'], recipe_to_cook)
#             recipe_output = get_gemini_response(*recipe_prompt)
#             steps, ingredients, servings, utensils = extract_recipe_details(recipe_output)

#             # Display recipe details
#             st.subheader("Recipe Details")
#             st.write("Ingredients:", ingredients)
#             st.write("Servings:", servings)
#             st.write("Utensils:", utensils)

#             # Generate and extract timestamps
#             timestamp_prompt = create_prompt_for_timestamps(selected_video['transcript'], steps, recipe_to_cook)
#             timestamp_output = get_gemini_response(*timestamp_prompt)
#             timestamps = extract_timestamps(timestamp_output)
#             print(timestamps)
#             # Create buttons for each step to navigate the video
#             st.subheader("Navigate through the video")
#             for step, value in steps.items():
#                 if st.button(f"{step} : {steps[step]}"):
#                     # Update the session state with the selected timestamp
#                     st.session_state['selected_timestamp'] = timestamps[step]

#             # Embed the YouTube video using HTML iframe with the selected timestamp
#             if st.session_state['selected_timestamp'] is not None:
#                 youtube_video_url = f"{base_youtube_video_url}?start={int(st.session_state['selected_timestamp'])}&autoplay=1"
#                 st.components.v1.html(
#                     f'<iframe width="560" height="315" src="{youtube_video_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
#                     height=315,)
#             else:
#             # Embed the YouTube video without a specific start time
#                 st.components.v1.html(
#                 f'<iframe width="560" height="315" src="{base_youtube_video_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
#                 height=315,
#                 )

# # Run the main function
# if __name__ == "__main__":
#     main()

import streamlit as st
from utils import extract_recipe_details, extract_timestamps, load_json_file, append_to_json_file
from youtube_scrapper import get_eng_recipe, get_transcript
from gemini import get_gemini_response, create_prompt_for_recipe, create_prompt_for_timestamps

# Initialize session state for selected timestamp URL
if 'selected_timestamp_url' not in st.session_state:
    st.session_state['selected_timestamp_url'] = None

def main():
    st.title("Recipe Helper")

    # User inputs the recipe name
    recipe_to_cook = st.text_input("Enter the name of the recipe")

    if recipe_to_cook:
        # Search for YouTube videos with English transcripts
        eng_recipes = get_eng_recipe(recipe_to_cook)
        if eng_recipes:
            # Let the user select a video
            video_titles = [recipe['title'] for recipe in eng_recipes]
            index_of_recipe_chosen = st.selectbox("Select a video", options=range(len(video_titles)), format_func=lambda x: video_titles[x])
            recipe_chosen = eng_recipes[index_of_recipe_chosen]

            file_path = "cache.json"
            loaded_data = load_json_file(file_path)

            # Check if the recipe is already in the cache
            if loaded_data is not None:
                if len(loaded_data) > 0:
                    if recipe_chosen['id'] in loaded_data[0].keys():
                        dictionary = loaded_data[0][recipe_chosen['id']]
                        steps = dictionary['steps']
                        ingredients = dictionary['ingredients']
                        servings = dictionary['servings']
                        utensils = dictionary['utensils']
                        timestamps_urls = dictionary['timestamps_urls']
                        base_youtube_video_url = f"https://www.youtube.com/embed/{recipe_chosen['id']}"
            else:
                transcript = get_transcript(recipe_chosen['id'])  # transcript with time stamps
                transcript_list = [i['text'] for i in transcript] # has individual element from the transcript
                transcript_combined = "".join(f"{i} " for i in transcript_list) # has transcript in the form of a single combined para
                model_role, prompt = create_prompt_for_recipe(transcript, recipe_to_cook)
                gemini_output = get_gemini_response(model_role, prompt)
                steps, ingredients, servings, utensils = extract_recipe_details(gemini_output)
                if steps is None:
                    gemini_output = get_gemini_response(model_role, prompt, temperature=1)
                    steps, ingredients, servings, utensils = extract_recipe_details(gemini_output)
                model_role_time, time_stamp_prompt = create_prompt_for_timestamps(transcript, steps, recipe_to_cook)
                time_gemini_output = get_gemini_response(model_role_time, time_stamp_prompt)
                timestamps = extract_timestamps(time_gemini_output)
                if timestamps is None:
                    time_gemini_output = get_gemini_response(model_role_time, time_stamp_prompt, temperature=1)
                    timestamps = extract_timestamps(time_gemini_output)
                base_youtube_video_url = f"https://www.youtube.com/embed/{recipe_chosen['id']}"
                timestamps_urls = {
                    key: f"{base_youtube_video_url}?start={value}&autoplay=1"
                    for key, value in timestamps.items()
                }
                dict_key = recipe_chosen['id']
                store_data = {
                    dict_key: {
                        'steps': steps,
                        'ingredients': ingredients,
                        'servings': servings,
                        'utensils': utensils,
                        'timestamps_urls': timestamps_urls,
                        'transcript' : transcript
                    }
                }
                append_to_json_file("cache.json", store_data)

            # Display recipe details
                st.subheader("Recipe Details")
                st.write("Ingredients:", ingredients)
                st.write("Servings:", servings)
                st.write("Utensils:", utensils)

                # Create buttons for each step to navigate the video
                st.subheader("Navigate through the video")
                for step, url in timestamps_urls.items():
                    if st.button(f"{step} : {steps[step]}"):
                        # Update the session state with the selected timestamp URL
                        st.session_state['selected_timestamp_url'] = url

            # Embed the YouTube video using HTML iframe with the selected timestamp URL
            if st.session_state['selected_timestamp_url'] is not None:
                url_to_visit = st.session_state['selected_timestamp_url']
                st.components.v1.html(
                    f'<iframe width="560" height="315" src="{url_to_visit}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
                    height=315,
                )
            else:
                # Embed the YouTube video without a specific start time
                st.components.v1.html(
                    f'<iframe width="560" height="315" src="{base_youtube_video_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
                    height=315,
                )

# Run the main function
if __name__ == "__main__":
    main()
