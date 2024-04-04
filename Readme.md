
# Recipe Helper


## Overview

The Recipe Helper is a Streamlit-based web application designed to assist users in finding and preparing recipes. By entering the name of a dish, users can search for relevant cooking videos, view detailed recipe information, and even get timestamps for crucial steps in the video. This application integrates with YouTube to fetch recipe videos and uses google gemini to extract recipe details and timestamps from video transcripts.

## Features

- **User Authentication**: Secure login system to ensure that only authorized users can access the application.
- **Recipe Search**: Users can search for recipes by entering the name of the dish.
- **Detailed Recipe Information**: For each selected video, the application displays ingredients, servings, utensils needed, and step-by-step instructions.
- **Timestamps**: Users can view the exact timestamps for each step in the recipe video, making it easier to follow along.

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/lakshyasoni97/Recipe-Parser.git
   cd Recipe-Parser
   ```


2. **Install Requirements**

   - Ensure you have Python installed on your system.
   - Install the required Python packages:
     ```bash
     pip install -r requirements.txt
     ```
3. **Run the Application**

   - To start the application, use the following command:
     ```bash
     streamlit run ui.py
     ```
4. **Access the Application**

   - Open your web browser and navigate to `http://localhost:8501`. You should see the login page of the Recipe Helper application.

## Usage

1. **Login**: Use your google gemini api key to log in.
2. **Search for a Recipe**: Enter the name of the dish you're interested in cooking in the text input field.
3. **Select a Video**: Choose a cooking video from the dropdown list to see more details.
4. **Fetch Recipe Details**: Click the "Fetch Recipe Details" button to view ingredients, utensils, servings, and step-by-step instructions.
5. **Follow Along**: If you have any questions about the recipe, you can ask your personal chef.


## Contribution

Contributions to the Recipe Helper are welcome! Please fork the repository and submit a pull request with your proposed changes.
