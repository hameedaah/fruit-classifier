import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import json


class FruitMaster:
  def __init__(self) -> None:
    self.model = load_model("model/fruit_classifier_model.h5")


    #import class names
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

  def get_details(self, fruit):
    for key, value in self.categorical_details.items():
      if fruit.lower() in value['fruits']:
        category = key
        description = value['description']
        smoothie_recipe = value['smoothie_recipe'].replace("{{fruit}}", fruit.lower())

        similar_fruits_list = value["fruits"][:]
        if fruit.lower() in similar_fruits_list:
            similar_fruits_list.remove(fruit.lower())

        # similar_fruits_list = value["fruits"]
        # similar_fruits_list.remove(fruit.lower())

    fruit_benefits = self.nutritional_benefits[fruit.lower()]

    return category, description, fruit_benefits, smoothie_recipe, similar_fruits_list
