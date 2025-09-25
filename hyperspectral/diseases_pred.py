import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

IMAGE_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 10
DATASET_PATH = 'dataset'
MODEL_PATH = 'disease_model.h5'

def build_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(*IMAGE_SIZE, 3)),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(len(os.listdir(DATASET_DIR)), activation='softmax')
    ])
    model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def train_model():
    datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

    train_data = datagen.flow_from_directory(
        DATASET_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )

    val_data = datagen.flow_from_directory(
        DATASET_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation'
    )

    model = build_model()

    es = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

    model.fit(train_data, validation_data=val_data, epochs=EPOCHS, callbacks=[es])

    model.save(MODEL_PATH)
    print("✅ Model trained and saved to", MODEL_PATH)

    return model, train_data.class_indices

def predict_image(image_path, model, class_indices):
    img = load_img(image_path, target_size=IMAGE_SIZE)
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    predicted_class = list(class_indices.keys())[np.argmax(prediction)]

    print(f"📷 Image: {image_path} -> 🧪 Predicted Disease: {predicted_class}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train and predict diseases from images")
    parser.add_argument('--train', action='store_true', help="Train the model on dataset")
    parser.add_argument('--predict', type=str, help="Path to image for prediction")

    args = parser.parse_args()

    if args.train:
        model, class_indices = train_model()
    else:
        if not os.path.exists(MODEL_PATH):
            print("⚠️ Model not found. Please train the model first using --train")
            exit()

        model = load_model(MODEL_PATH)
        class_indices = {name: idx for idx, name in enumerate(sorted(os.listdir(DATASET_DIR)))}

    if args.predict:
        predict_image(args.predict, model, class_indices)