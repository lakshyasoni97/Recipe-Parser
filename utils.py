from skimage import io
import matplotlib.pyplot as plt
from PIL import Image
import json
import re
import os


def display_image(image_url):
    '''this function displays the image possible from all the urls'''
    try:
        a = io.imread(image_url)
        plt.imshow(a)
        plt.axis('off')
        plt.show()
    except Exception as e:
        print(f"Could not load image {e}")
        

def extract_recipe_details(recipe_json):
    # Remove any non-JSON characters (e.g., backticks)
    recipe_json = recipe_json.strip("`").replace('```', '')

    # Remove the word "JSON" (case-insensitive) along with surrounding spaces or newline characters
    recipe_json = re.sub(r'\s*JSON\s*\n?', '', recipe_json, flags=re.IGNORECASE)

    # Remove multiple consecutive spaces
    recipe_json = re.sub(r'\s+', ' ', recipe_json)

    # Load the JSON string into a Python dictionary
    try:
        recipe_dict = json.loads(recipe_json)
    except json.JSONDecodeError:
        print("Error decoding JSON. Please check the input format.")
        return {}, {}, "", []

    # Extract the details
    steps = recipe_dict.get("Step-by-step instructions", {})
    ingredients = recipe_dict.get("Ingredients", {})
    servings = recipe_dict.get("Servings", "")
    utensils = recipe_dict.get("Utensils", [])

    # Ensure utensils is a list
    if isinstance(utensils, (set, dict)):
        utensils = list(utensils)

    return steps, ingredients, servings, utensils


def extract_timestamps(recipe_json):
    recipe_json = recipe_json.strip("`").replace('```', '')
    recipe_json = re.sub(r'\s*JSON\s*\n?', '', recipe_json, flags=re.IGNORECASE)
    recipe_json = re.sub(r'\s+', ' ', recipe_json)
    try:
        recipe_dict = json.loads(recipe_json)
    except json.JSONDecodeError:
        print("Error decoding JSON. Please check the input format.")
        return {}
    dic = recipe_dict.get("Step-by-step timestamps", {})
    for key, value in dic.items():
        try:
            dic[key] = int(value)
        except:
            dic[key] = value
    return dic
    
    

def append_to_json_file(file_path, data):
    # Check if the file exists and is not empty
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "r") as file:
            existing_data = json.load(file)
    else:
        existing_data = []
    # Append the new data to the existing data
    if len(existing_data) > 0 and list(data.keys())[0] not in existing_data[0].keys():
        existing_data.append(data)
    # Write the updated data back to the file
    with open(file_path, "w") as file:
        json.dump(existing_data, file, indent=4)
        


def load_json_file(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"File '{file_path}' is not a valid JSON file.")
        return None