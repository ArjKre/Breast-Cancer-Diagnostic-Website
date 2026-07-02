import tensorflow as tf
from config import BATCH_SIZE, IMAGE_SIZE, MODEL_PATH
from tensorflow.keras import layers
from tensorflow.keras.utils import image_dataset_from_directory

AUTOTUNE = tf.data.AUTOTUNE

model = tf.keras.models.load_model(MODEL_PATH)

val_ds = image_dataset_from_directory(
    "./dataset",
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
)

val_ds = val_ds.map(lambda x, y: (layers.Rescaling(1.0 / 255)(x), y))
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

loss, accuracy = model.evaluate(val_ds)
print(f"Validation Accuracy: {accuracy:.4f}")
