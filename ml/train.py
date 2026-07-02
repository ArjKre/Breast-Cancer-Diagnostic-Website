import tensorflow as tf
from config import BATCH_SIZE, IMAGE_SIZE
from tensorflow.keras import layers
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.utils import image_dataset_from_directory

AUTOTUNE = tf.data.AUTOTUNE


train_ds = image_dataset_from_directory(
    "./dataset",
    validation_split=0.2,
    subset="training",
    seed=42,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    color_mode="rgb",
)

val_ds = image_dataset_from_directory(
    "./dataset",
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    color_mode="rgb",
)

normalization_layer = layers.Rescaling(1.0 / 255)

train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)

val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

data_augmentation = tf.keras.Sequential(
    [
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
    ]
)

base_model = EfficientNetB0(
    weights="imagenet", include_top=False, input_shape=(224, 224, 3)
)

base_model.trainable = True

inputs = tf.keras.Input(shape=(224, 224, 3))

x = data_augmentation(inputs)

x = base_model(x, training=base_model.trainable)

x = layers.GlobalAveragePooling2D()(x)

x = layers.Dropout(0.3)(x)

outputs = layers.Dense(1, activation="sigmoid")(x)

model = tf.keras.Model(inputs, outputs)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss="binary_crossentropy",
    metrics=["accuracy"],
)

model.summary()

callbacks = [
    tf.keras.callbacks.ModelCheckpoint(
        "../models/best_model.keras", save_best_only=True, monitor="val_accuracy", mode="max"
    ),
    tf.keras.callbacks.EarlyStopping(
        monitor="val_accuracy", patience=15, restore_best_weights=True, mode="max"
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss", factor=0.3, patience=5, min_lr=1e-8, verbose=1
    ),
]

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=80,
    callbacks=callbacks,
)

print("\nFinal Metrics:")
print(f"loss = {history.history['loss'][-1]:.4f}")
print(f"accuracy = {history.history['accuracy'][-1]:.4f}")
print(f"val_loss = {history.history['val_loss'][-1]:.4f}")
print(f"val_accuracy = {history.history['val_accuracy'][-1]:.4f}")

loss, accuracy = model.evaluate(val_ds)
print(f"TEST VALIDATION Accuracy: {accuracy:.4f}")
