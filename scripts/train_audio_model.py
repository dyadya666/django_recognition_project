import numpy as np
import os
import tensorflow as tf
from keras import layers, models


X = np.load("X.npy")
y = np.load("y.npy")

CLASS_NAMES = np.load("class_names.npy")

X = X[..., np.newaxis]  # додаємо канал
y = tf.keras.utils.to_categorical(y, num_classes=len(CLASS_NAMES))

model = models.Sequential([
    layers.Input(shape=(128, 128, 1)),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(len(CLASS_NAMES), activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(X, y, epochs=10, batch_size=8, validation_split=0.2)

os.makedirs("models", exist_ok=True)
model.save("models/audio_classifier.keras")

print("Model trained and saved to models/audio_classifier.keras")
