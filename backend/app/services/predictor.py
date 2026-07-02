from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image

MODEL_PATH = (
    Path(__file__).resolve().parents[3] / "models" / "breast_cancer_model.keras"
)
model = tf.keras.models.load_model(MODEL_PATH)


def preprocess_image(image_path):

    image = Image.open(image_path)

    image = image.convert("RGB")

    image = image.resize((224, 224))

    image = np.array(image)

    image = image / 255.0

    image = np.expand_dims(image, axis=0)

    return image


def predict(image_path):

    image = preprocess_image(image_path)

    prediction = model.predict(image)[0][0]

    if prediction > 0.5:
        label = "Malignant"

        confidence = float(prediction)

    else:
        label = "Benign"

        confidence = float(1 - prediction)

    return {"prediction": label, "confidence": confidence}
