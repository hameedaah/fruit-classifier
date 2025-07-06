import google.generativeai as genai
from google.generativeai import types
from google.generativeai import types # Keep this, it might be useful for other configs
import os

import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import json
from dotenv import load_dotenv 

# Load environment variables from a .env file (for local development)
load_dotenv()

class FruitMaster:
  def __init__(self) -> None:

      # Get the API key from environment variables
      gemini_api_key = os.getenv("GOOGLE_API_KEY")
      if not gemini_api_key:
          raise ValueError("GOOGLE_API_KEY environment variable not set.")
      
      self.model = load_model("model/fruit_classifier_model.h5")
      self.gemini_model = genai.GenerativeModel('gemini-1.5-flash') # This is your Gemini model instance

      # Import class names
      with open("others/classnames.txt", 'r') as file:
          self.class_names = [line.strip() for line in file]

      with open("others/Categorical_Details.json", 'r') as file:
          self.categorical_details = json.load(file)

      with open("others/Nutritional_Benefits.json", 'r') as file:
          self.nutritional_benefits = json.load(file)


  def decode_output(self, output_ind):
      return self.class_names[output_ind]


  def predict(self, image):
      # Resize to (128, 128) as expected by the model
      resize = tf.image.resize(image, (128, 128))

      # Convert to numpy, normalize and expand dimensions
      input_array = np.expand_dims(resize.numpy() / 255.0, axis=0)  # shape: (1, 128, 128, 3)

      # Predict
      output = self.model.predict(input_array)[0]

    # Extract prediction
      index = int(np.argmax(output))
      self.y = float(output[index])
      self.predicted_name = self.decode_output(index)
      return self.predicted_name, self.y

  def get_details_from_gemini(self, fruit_name: str = None, question: str = None):
      
      if not fruit_name:
        fruit_name = self.predicted_name
      
      instruction = f""" 
        You are a nutritionist health care professional. You will be given reply to question about the fruit {fruit_name if fruit_name else "specified in the question"}. You will be provide answering only when the question aligns with the:
        1. Nutritional benefits of the fruit
        2. Health benefits of the fruit
        3. General information about the fruit
        4. Similar fruits to the fruit
        5. Fruit classification and identification
        6. Fruit storage and preservation methods
        7. Fruit recipes and culinary uses
        If the question does not align with the above topics, you will respond with "I am unable to provide information on that topic."
        Always keep your responses concise and to the point, avoiding unnecessary details or tangents. Also, use less technical terms while given reply.
        """
      
      if question:
          user_query = question
      elif fruit_name:
          user_query = f"Tell me about {fruit_name}"
      else:
          return "No fruit name or question provided for Gemini API."

      # THIS IS THE KEY PART FOR GEMINI-1.5-FLASH
      # System instruction as the first user message, followed by the actual query
      contents_list = [
          {"role": "user", "parts": [instruction]},
          {"role": "user", "parts": [user_query]} # Actual query
      ]

      try:
          response = self.gemini_model.generate_content(
              contents=contents_list
          )
          return response.text
      
      except Exception as e:
          print(f"Error calling Gemini API: {e}")
          return "Could not retrieve detailed information at this time."

  def get_details(self, fruit):
      category = "Unknown"
      description = "No description available."
      smoothie_recipe = "No smoothie recipe available."
      similar_fruits_list = []
      fruit_benefits = {}

      for key, value in self.categorical_details.items():
          if fruit.lower() in value['fruits']:
              category = key
              description = value['description']
              smoothie_recipe = value['smoothie_recipe'].replace("{{fruit}}", fruit.lower())

              similar_fruits_list = value["fruits"][:]
              if fruit.lower() in similar_fruits_list:
                  similar_fruits_list.remove(fruit.lower())
              break # Exit loop once fruit is found

      if fruit.lower() in self.nutritional_benefits:
          fruit_benefits = self.nutritional_benefits[fruit.lower()]
      else:
          print(f"Warning: Nutritional benefits not found for {fruit.lower()} in local data.")


      return category, description, fruit_benefits, smoothie_recipe, similar_fruits_list