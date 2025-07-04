import google.generativeai as genai
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
    
    genai.configure(api_key=gemini_api_key)
    
    self.model = load_model("model/fruit_classifier_model.h5")
    self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')


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
    y = float(output[index])
    predicted_name = self.decode_output(index)
    return predicted_name, y

  def get_details_from_gemini(self, fruit_name: str):

    prompt = f"""
      Tell a well-structured and informative story about the fruit: {fruit_name}.<br><br>
      Begin by introducing its category, such as whether it’s a berry, citrus, tropical, or something else.<br><br>
      Then, describe its nutritional profile by highlighting key vitamins, minerals, calorie content, carbohydrates, fiber, and any standout components that make it notable from a health perspective.<br><br>
      Follow this with a summary of the primary health benefits that regular consumption of this fruit may offer, including effects on digestion, immunity, skin, or chronic disease prevention.<br><br>
      Afterward, explain how the fruit is commonly used in meals—whether it's eaten fresh, juiced, baked, blended, or cooked—and name some typical culinary contexts or recipes where it plays a central role.<br><br>
      Compare it to a few other fruits with similar taste, texture, or nutritional qualities to give a sense of how it fits into the broader fruit family.<br><br>
      Finally, provide a simple and tasty smoothie recipe using {fruit_name} as the main ingredient, listing the ingredients and brief preparation steps.<br><br>
      Keep the explanation factual, engaging, and easy to understand, while staying under 2000 characters in total length.


    """

    try:
        response = self.gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        # Consider a more detailed error return in a real app, e.g., logging the full exception.
        return "Could not retrieve detailed information at this time."

  def get_details(self, fruit):
    # This method seems to pull from local JSON files, not Gemini.
    # Ensure this is intentional and how your application flows.
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