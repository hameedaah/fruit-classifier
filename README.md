# 🍎 FRUITTION - The Fruit Solution App

## 🎯 Project Objective

The primary goal of this project was to **build a Convolutional Neural Network (CNN)** capable of accurately **predicting the class of a fruit** from an input image.

This was done to assist **app users and fruit consumers** in identifying fruits—whether shopping in a **supermarket** or Browse through an app—and to provide **brief informative details** about each fruit class. The model serves both as a recognition tool and a lightweight educational assistant.

## ✨ Features

The Fruition app aims to provide a seamless experience for fruit identification and nutritional information:
* **Snap a Fruit:** Easily identify fruits by taking a picture.
* **Get Nutrition & Recipes:** Access nutritional facts and healthy recipes.
* **Make Better Choices:** Discover nutritious, lean, and balanced food options.

## 📦 Imported Libraries

The project leverages several key Python libraries for data handling, model building, and visualization:
* **Pandas / NumPy**: For efficient data manipulation.
* **Matplotlib / Seaborn**: For creating insightful visualizations.
* **TensorFlow / Keras**: The core framework for deep learning models and layers.
* **ImageDataGenerator**: Essential for image data preprocessing and augmentation.
* **Train-Test Split (from sklearn.model_selection)**: For dividing the dataset into training and validation sets.
* **Callbacks**: Utilized for early stopping and model checkpointing during training.

## 📊 Dataset

The dataset used for this project is sourced from `Fruit_dataset/train.csv` and contains image filenames paired with their corresponding labels. Human-readable class names were loaded from `classname.txt` to replace numeric labels, enhancing interpretability.

* **Total Images:** Approximately 40,000 images.
* **Number of Classes:** 100 distinct fruit classes.
* **Image Dimensions:** All input images are resized to 128x128 pixels.
* **Class Distribution:** Each class is proportionally represented due to stratified sampling.

## 🧪 Data Preprocessing and Augmentation

A robust data pipeline was implemented to prepare the images for CNN training:

1.  **Train-Validation Split:**
    * The full dataset was split into **80% training data** and **20% validation data**.
    * Stratified sampling was applied to maintain the class distribution in both sets.

2.  **Augmented and Normalized Splits:**
    * The training dataset was further divided into **40% augmented training data** and **60% normalized training data**, also using stratified sampling.

3.  **Image Augmentation with `ImageDataGenerator`:**
    * An `ImageDataGenerator` was configured to apply real-time augmentations to the augmented training images. These include:
        * **Rescaling:** Pixel values are scaled from [0, 255] to [0, 1].
        * **Rotation:** Images are randomly rotated (up to 67 degrees).
        * **Zoom:** Random zooming (between 75% and 125% of the original size).
        * **Brightness Adjustment:** Random brightness adjustments (between 75% and 125%).
        * **Horizontal and Vertical Flipping:** Images are randomly flipped horizontally and vertically.
    * These augmentations expand the dataset size, reduce overfitting, and improve model generalization.

4.  **Data Rescaling (Normalization):**
    * For the normalized training data and validation data, only pixel rescaling (1/255) was applied to stabilize training. No other augmentations were used at this stage.

5.  **Data Loading with `flow_from_dataframe`:**
    * The `flow_from_dataframe` method was used to efficiently stream image batches from disk, apply augmentations/rescaling on-the-fly, and optimize memory usage.
    * Labels are converted to a categorical format, and data is shuffled for each epoch.

6.  **Combined Generator:**
    * A custom generator `combined_generator` merges batches from both the augmented and rescaled datasets, concatenating images and labels. This ensures the model trains on diverse and clean samples, enhancing robustness and generalization.

## 🧠 Model Architecture

The Convolutional Neural Network (CNN) is built using the Keras Sequential API and comprises several layers designed for image classification:

```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Dense, Flatten, MaxPooling2D, Dropout

model = Sequential([
    # First Convolutional Block
    Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    MaxPooling2D(2, 2),
    Dropout(0.25),

    # Second Convolutional Block
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Dropout(0.25),

    # Third Convolutional Block
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Dropout(0.25),

    # Flattening for Dense layers
    Flatten(),

    # Dense Layers
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(100, activation='softmax') # 100 classes for fruit classification
])
```

## ⚙️ Training

The model was compiled with the Adam optimizer and categorical cross-entropy loss, suitable for multi-class classification. Early stopping and model checkpointing callbacks were used to prevent overfitting and save the best model.

## 📈 Evaluation and Results

After training, the model's performance was evaluated on the test dataset.

* **Test Loss:** 2.5955
* **Test Accuracy:** 0.3458 (34.58%)

While the initial accuracy is moderate, further hyperparameter tuning, more extensive data augmentation, or exploring advanced CNN architectures could significantly improve performance.

A visualization of sample images from the dataset is available in the notebook to help understand the input data. (To view, please run the `cnn-fruit-classifier.ipynb` notebook.)

## 🚀 How to Run

## 🚀 How to Run

This project includes both a **Jupyter Notebook for model development and training** and a **web application** that demonstrates the fruit classification in action.

### 1. Running the Web Application

The web application is built with **FastAPI (Python backend)**, **HTML, CSS, and JavaScript (frontend)**, and uses **JSON files** for categorical and nutritional details.

#### Prerequisites

* Python 3.8+
* `pip` (Python package installer)

#### Setup Instructions

1.  **Project Structure:** Ensure your project directory is structured as follows, with the necessary files in their respective locations:

    ```
    .
    ├── app.py
    ├── src/
    │   ├── services.py
    ├── static/
    │   ├── style.css
    │   └── script.js
    ├── templates/
    │   └── index.html
    ├── model/
    │   └── fruit_classifier_model.h5
    └── others/
        ├── Categorical_Details.json
        ├── classnames.txt
        └── Nutritional_Benefits.json
    ```

    * **Note:** The `model/fruit_classifier_model.h5` file (the trained CNN model) is crucial for the application's functionality. Please ensure this model file is present in the `model/` directory. If it's not available, you would first need to train the model using the Jupyter Notebook to generate it.

2.  **Install Python Dependencies:**
    Install the required Python libraries using `pip`:
    ```bash
    pip install fastapi uvicorn tensorflow pillow python-multipart Jinja2
    ```
    * `tensorflow`: For loading and running the deep learning model.
    * `fastapi`: The web framework for the backend API.
    * `uvicorn`: An ASGI server to run the FastAPI application.
    * `pillow`: For image processing.
    * `python-multipart`: For handling form data, especially file uploads.
    * `Jinja2`: For rendering HTML templates.

3.  **Run the Backend Server:**
    Navigate to the root directory of your project (where `app.py` is located) in your terminal and run the FastAPI application using Uvicorn:
    ```bash
    uvicorn app:app --reload
    ```
    The `--reload` flag enables auto-reloading upon code changes, which is useful for development.

4.  **Access the Application:**
    Once the server is running, open your web browser and go to `http://127.0.0.1:8000` (or the address indicated in your terminal). You should see the Fruit Classifier application interface.

### 2. Running the Jupyter Notebook

The Jupyter Notebook (`cnn-fruit-classifier.ipynb`) contains all the code for data loading, preprocessing, model building, training, and evaluation.

1.  **Clone the Repository (or download the notebook and associated data):**
    ```bash
    git clone <repository_url>
    ```
    (Replace `<repository_url>` with the actual URL if this project is hosted.)

2.  **Install Python Dependencies:**
    Ensure you have all the required libraries installed. You can install them via pip:
    ```bash
    pip install pandas numpy matplotlib seaborn tensorflow keras scikit-learn
    ```

3.  **Download the Dataset:**
    The notebook expects the `Fruit_dataset` directory, typically located at `../input/fruit-classification-dataset/`. Ensure your dataset is structured accordingly relative to the notebook's location.

4.  **Run the Jupyter Notebook:**
    Open `cnn-fruit-classifier.ipynb` in a Jupyter environment (e.g., Jupyter Lab, Jupyter Notebook, VS Code with Jupyter extensions) and run all cells sequentially to reproduce the model training and evaluation.

## 💼 About Fruition

Fruition is a forward-thinking tech company dedicated to revolutionizing how consumers interact with fresh produce. Our mission is to leverage cutting-edge machine learning and deep learning technologies to create innovative solutions that empower individuals to make healthier and more informed food choices. We believe that technology can simplify daily decisions, bringing clarity and convenience to the complex world of nutrition and healthy living. With Fruition, the future of fruit identification and dietary guidance is just a snap away.
