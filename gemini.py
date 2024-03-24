import google.generativeai as genai
import json
import re



def get_gemini_response(input, prompt, gemini_api_key, temperature = 0.9):
    # gemini_api_key = ''
    genai.configure(api_key=gemini_api_key)
    generation_config = {
        "temperature": temperature,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                    generation_config=generation_config)

    response = model.generate_content([input, prompt])
    return response.text


def create_prompt_for_recipe(transcript, recipe_to_cook):
    
    response_object = {
    "Step-by-step instructions": {
        "Step 1": "Step 1 goes here",
        "Step 2": "Step 2 goes here"
        # Add more steps as needed
    },
    "Ingredients": {
        "Ingredient 1": "Quantity of ingredient 1",
        "Ingredient 2": "Quantity of ingredient 2"
        # Add more ingredients as needed
    },
    "Servings": "number of people in integer for which the recipe is for",
    "Utensils": ["utensil 1", "utensil 2", "add more utensils to the list as needed"]
    # Add more utensils to the list as needed
    }

    model_role = "You are a large language model trained to extract step-by-step cooking instructions from a transcript of a YouTube cooking video. Your task is to identify and list all the steps involved in cooking the dish described in the transcript. Each step should be clear, concise, and in the order they appear in the video. If there are any specific measurements, cooking times, or temperatures mentioned, include those details in the corresponding steps."

    prompt =  f"""Transcript: {transcript}
    Based on the transcript above of the {recipe_to_cook} recipe, extract the step-by-step cooking instructions for the dish. List each step clearly and concisely, including any specific measurements, cooking times, or temperatures mentioned. Ensure the steps are in the order they appear in the video. Also list down ingredients, servings and utensils used.
    Give the output only in JSON format as shown below:
    {json.dumps(response_object)}
    """
    
    return model_role, prompt


def create_prompt_for_timestamps(transcript, steps, recipe_to_cook):
    response_object_step_time = {
    "Step-by-step timestamps": {
        "Step 1": 10.2,
        "Step 2": 15.3,
        "Step 3": 'and so on....'
        # Add more steps as needed
    }
    }
    model_role_time = "You are a large language model trained to extract precise timestamps in seconds for each step in a cooking process from a transcript of a YouTube cooking video. Your task is to analyze the transcript and identify the exact moment each step begins. Pay attention to cues in the language that indicate the start of a new step, such as changes in activity or the introduction of new ingredients. Provide the start time of each step in seconds in a clear and concise format."

    prompt =  f"""Transcript: {transcript}  
    Steps from the transcript: {steps}
    Based on the transcript above of the {recipe_to_cook} recipe and the steps extracted, determine the starting time of each step in seconds in the video. The start time should be in directly in seconds. Focus on identifying the exact moment when each step begins, considering any verbal cues or changes in activity.
    Provide the output in JSON format as shown below:
    {json.dumps(response_object_step_time, indent=4)}
    """
    return model_role_time, prompt

def create_prompt_for_question_answering(transcript, recipe_to_cook, question):
    model_role = "As a chef with expertise in various recipes, your task is to provide detailed answers to questions based on a specific recipe's transcript. Use your culinary knowledge and the given transcript to offer insightful and accurate responses."

    prompt = f"""Transcript of the {recipe_to_cook} Recipe: \n\n{transcript}\n\nGiven the detailed transcript above for the {recipe_to_cook} recipe, your expertise is needed to answer this culinary question:\n\nQuestion: {question}\n\nAs a chef, your Answer:"""

    return model_role, prompt