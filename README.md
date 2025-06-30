# 🍎 FRUITION – An Image-Based Fruit Prediction App

&nbsp;
<a name="overview"></a>
## 📖 Overview

**Fruition** is a deep learning-powered fruit classification app that uses Convolutional Neural Networks (CNNs) to recognize fruit types from images. It features a **Streamlit web interface** that allows users to either upload a fruit image or take a picture using their device’s camera, and receive the predicted class along with fruit facts, benefits, and even a smoothie recipe suggestion.

We are a forward-thinking tech company dedicated to revolutionizing how consumers interact with fresh produce. Our mission is to leverage cutting-edge machine learning and deep learning technologies to create innovative solutions that empower individuals to make healthier and more informed food choices. We believe that technology can simplify daily decisions, bringing clarity and convenience to the complex world of nutrition and healthy living. With Fruition, the future of fruit identification and dietary guidance is just a snap away.

&nbsp;
## 📚 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Use Cases](#use-cases)
- [Dataset](#dataset)
- [Imported Libraries](#imported-libraries)
- [Model Workflow](#model-workflow)
- [Installation & Setup](#installation-setup)
- [Streamlit App](#streamlit-app)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Contributors](#contributors)
- [License](#license)

&nbsp;
<a name="project-structure"></a>
## 🏗️ Project Structure

```text
fruit-classifier/
├── model/
├── notebook/
├── others/
├── src/
├── static/
├── templates/
├── test_images/
├── app.py
├── install_dependencies.py
├── requirements.txt
├── README.md
└── LICENSE

````
&nbsp;
<a name="use-cases"></a>
## 🎯 Use Cases

* 🛒 **Grocery Aid**: Instantly identify unfamiliar fruits while shopping and access health benefits, helping consumers make informed choices and try new produce with confidence.

* 🧑‍🏫 **Classroom Learning**: Engage students with visual fruit recognition to teach nutrition, biology, and healthy habits in an interactive and memorable way.

* 🏥 **Nutrition Support**: Support dietitians and healthcare providers by helping patients identify fruits that align with diabetic, weight-loss, or heart-healthy meal plans.

* 🧳 **Travel Companion**: Discover exotic or local fruits while traveling by snapping a photo and learning their names, taste profiles, and uses in regional cuisine.

* 🛍️ **Retail Utility**: Enable farmers, vendors, and stores to label and manage fruit inventory using image recognition instead of barcodes or manual lookup.

&nbsp;
<a name="dataset"></a>
## 📂 Dataset

> ⚠️ The dataset used for this project is **not included in this repository** due to its size.

You can download it here:
- 📥 **[Fruit Image Classification Dataset on Kaggle](https://www.kaggle.com/datasets/icebearogo/fruit-classification-dataset)**

### Contents

- 100 fruit classes
- 40,000 labeled images
- Accompanying CSV files and `classname.txt` for class mapping

The notebook expects the `Fruit_dataset` directory, located at `../input/fruit-classification-dataset/`. Ensure your dataset is structured accordingly relative to the notebook's location.

&nbsp;
<a name="imported-libraries"></a>
## 📦 Imported Libraries

The project leverages several key Python libraries for data handling, model building, and visualization:
* **Pandas / NumPy**: For efficient data manipulation.
* **Matplotlib / Seaborn**: For creating insightful visualizations.
* **TensorFlow / Keras**: The core framework for deep learning models and layers.
* **ImageDataGenerator**: Essential for image data preprocessing and augmentation.
* **Train-Test Split (from sklearn.model_selection)**: For dividing the dataset into training and validation sets.
* **Callbacks**: Utilized for early stopping and model checkpointing during training.

&nbsp;
<a name="model-workflow"></a>
## 🔍 Model Workflow

### ✅ Data Preparation
- Load `train.csv` and`val.csv`.
- Strip unnecessary prefixes from image paths.
- Map numeric labels to fruit names using `classname.txt`.

### 🧪 Train/Val Splitting
- `80/20` split between training and validation.
- Stratified sampling ensures balanced class representation.
- Training data further split into:
  - 60% for standard training
  - 40% for on-the-fly **data augmentation**

### 🔁 Augmentation Strategy
- Used `ImageDataGenerator` for:
  - Rotation, zoom, brightness, horizontal & vertical flips
  - Normalization via `rescale=1./255`
- Combined clean and augmented samples into one generator.

### 🧠 Model Architecture

* **Model**: Convolutional Neural Network (Keras Sequential API)
* **Input Size**: 128×128×3 (RGB image)
* **Architecture**:  
  Conv2D → MaxPooling → Conv2D → MaxPooling → Conv2D → MaxPooling →  
  Flatten → Dense(128) → Dropout(0.5) → Dense(100, softmax)
* **Optimizer**: Adam
* **Loss Function**: Categorical Crossentropy
* **Callbacks**: EarlyStopping, ModelCheckpoint (.h5 and .keras)


### 📈 Training Results

* Trained for 50 epochs using 500 steps per epoch
* Final validation accuracy: **\~34.5% on 100 classes**
* Training & validation curves plotted for visual inspection

### 📊 Test Evaluation

```python
loss, accuracy = model.evaluate(test_flow)
print("Test Accuracy:", accuracy)
```
&nbsp;
<a name="installation-setup"></a>
## ⚙️ Installation & Setup

### 🔧 Clone the Repository and Set Up the Environment

```bash
git clone https://github.com/hameedaah/fruit-classifier.git
cd fruit-classifier
python -m venv venv
source venv/bin/activate         # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🚀 How to Run

This project includes both a **Jupyter Notebook for model development and training** and a **web application** that demonstrates the fruit classification in action.

### ⚡Run the FastAPI Web App 

The web application is built with **FastAPI (Python backend)**, **HTML, CSS, and JavaScript (frontend)**, and uses **JSON files** for categorical and nutritional details.

#### 🔑 Prerequisites

* Python 3.8+
* Required packages:

  ```bash
  pip install fastapi uvicorn tensorflow pillow python-multipart jinja2
  ```

#### ⚠️ Important

Ensure the model file `model/fruit_classifier_model.h5` exists. If not, train the model using the notebook first. This is crucial for the application's functionality


#### ▶️ Launch FastAPI Server
Navigate to the root directory of your project (where `app.py` is located) in your terminal and run the FastAPI application using Uvicorn:
```bash
uvicorn app:app --reload
```
The `--reload` flag enables auto-reloading upon code changes, which is useful for development.


#### ▶️ Access the Application
Once the server is running, open your web browser and go to [http://127.0.0.1:8000](http://127.0.0.1:8000) (or the address indicated in your terminal). You should see the Fruit Classifier application interface.



### 📓 3. Run the Jupyter Notebook

The Jupyter Notebook (`cnn-fruit-classifier.ipynb`) contains all the code for data loading, preprocessing, model building, training, and evaluation.
 Ensure you have all the required libraries installed. You can install them via pip:
```bash
jupyter notebook notebooks/cnn-fruit-classifier.ipynb
```


Install necessary packages if needed:

```bash
pip install pandas numpy matplotlib seaborn tensorflow keras scikit-learn
```
    * `tensorflow`: For loading and running the deep learning model.
    * `fastapi`: The web framework for the backend API.
    * `uvicorn`: An ASGI server to run the FastAPI application.
    * `pillow`: For image processing.
    * `python-multipart`: For handling form data, especially file uploads.
    * `Jinja2`: For rendering HTML templates.

&nbsp;
<a name="streamlit-app"></a>
## 💡 Streamlit App - Interface and Prediction Flow

### 📦 Features

* Upload or snap a picture of any fruit for instant recognition
* Get the predicted **fruit name** with a brief **description**
* View key **benefits**, a **smoothie recipe**, and **similar fruits**
* Access **nutritional facts** and make smarter food choices


### App Homepage

![App-Overview](https://github.com/user-attachments/assets/f4bd323e-e5da-4aa5-856b-f4635590ada7)

### Image Capture or Upload

![Image Capture](https://github.com/user-attachments/assets/9ab0974d-64bd-4444-ae1e-b648787d751e)


### Prediction Result

![Predicted-Result](https://github.com/user-attachments/assets/c8489c34-c581-4f61-8b10-8b0d19107fa4)

&nbsp;
<a name="limitations"></a>
## ⚠️ Limitations

* 🍓 **Limited Fruit Variety**: The model can only recognize fruits included in its training dataset (101+ classes).

* 🍏 **Single Fruit Detection**: It identifies one fruit per image and may not handle mixed or overlapping fruit scenes.

* 💡 **Lighting Sensitivity**: Accurate recognition requires well-lit images; poor lighting may affect performance.

* 📏 **No Portion Estimation**: The app does not estimate fruit size or quantity, so nutrition facts are not adjusted by portion.

&nbsp;
<a name="future-improvements"></a>
## 🔧 Future Improvements

* 🍍 **Expand Fruit Database**: Train the model on more fruit classes, including rare, regional, or hybrid varieties to broaden its recognition scope.

* 🥗 **Support Multi-Fruit Detection**: Enable the app to recognize and label multiple fruits within a single image.

* 💡 **Improve Low-Light Performance**: Enhance model robustness with training on varied lighting conditions and preprocessing for brightness correction.

* 📏 **Add Portion Size Estimation**: Integrate image-based size analysis to estimate fruit quantity and adjust nutritional outputs accordingly.

&nbsp;
<a name="contributors"></a>
## 👨‍💻 Contributors

* TeSA Artificial Intelligence Specialization (Cohort 3)

&nbsp;
<a name="license"></a>
## 📝 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.
