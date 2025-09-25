import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import argparse
import joblib

# ========== CONFIG ==========
DATA_FILE = 'soil_data.csv'
MODEL_FILE = 'soil_model.pkl'

CROP_REQUIREMENTS = {
    'wheat': {'nitrogen': 60, 'phosphorus': 40, 'potassium': 50, 'ph_range': (6.0, 7.0), 'soil_types': ['Loamy', 'Clay']},
    'rice':  {'nitrogen': 100, 'phosphorus': 50, 'potassium': 60, 'ph_range': (5.5, 7.0), 'soil_types': ['Clay', 'Silty']},
    'maize': {'nitrogen': 90, 'phosphorus': 45, 'potassium': 50, 'ph_range': (5.8, 7.0), 'soil_types': ['Loamy', 'Sandy']},
    # Add more crops as needed
}

# ========== TRAINING ==========
def train_model():
    df = pd.read_csv(DATA_FILE)

    features = ['latitude', 'longitude', 'nitrogen', 'phosphorus', 'potassium', 'ph']
    X = df[features]
    y = df['soil_type']

    model = RandomForestClassifier()
    model.fit(X, y)

    joblib.dump(model, MODEL_FILE)
    print(f"✅ Model trained and saved to {MODEL_FILE}")
    return model

# ========== PREDICTION ==========
def predict_soil_type(model, input_data):
    features = ['latitude', 'longitude', 'nitrogen', 'phosphorus', 'potassium', 'ph']
    X = pd.DataFrame([input_data], columns=features)
    soil_type = model.predict(X)[0]
    return soil_type

# ========== CROP SUITABILITY CHECK ==========
def check_crop_suitability(crop, minerals, soil_type):
    crop = crop.lower()
    if crop not in CROP_REQUIREMENTS:
        return False, f"⚠️ Crop '{crop}' not found in database."

    reqs = CROP_REQUIREMENTS[crop]
    reasons = []

    if soil_type not in reqs['soil_types']:
        reasons.append(f"Incompatible soil type: {soil_type} ❌")

    for mineral in ['nitrogen', 'phosphorus', 'potassium']:
        if minerals[mineral] < reqs[mineral]:
            reasons.append(f"Low {mineral.title()}: Needs ≥ {reqs[mineral]}, found {minerals[mineral]} ❌")

    ph = minerals['ph']
    ph_min, ph_max = reqs['ph_range']
    if not (ph_min <= ph <= ph_max):
        reasons.append(f"pH out of range: Required {ph_min}-{ph_max}, found {ph} ❌")

    if not reasons:
        return True, "✅ Crop is suitable for this soil and mineral condition."
    else:
        return False, "❌ Unsuitable:\n" + "\n".join(reasons)

# ========== MAIN ==========
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict soil type and check crop suitability.")
    parser.add_argument('--train', action='store_true', help="Train the soil model")
    parser.add_argument('--latitude', type=float, help="Latitude of the area")
    parser.add_argument('--longitude', type=float, help="Longitude of the area")
    parser.add_argument('--nitrogen', type=int, help="Nitrogen content")
    parser.add_argument('--phosphorus', type=int, help="Phosphorus content")
    parser.add_argument('--potassium', type=int, help="Potassium content")
    parser.add_argument('--ph', type=float, help="pH value of soil")
    parser.add_argument('--crop', type=str, help="Crop to check for suitability")

    args = parser.parse_args()

    if args.train:
        train_model()
    else:
        # Check required fields
        required_fields = [args.latitude, args.longitude, args.nitrogen, args.phosphorus, args.potassium, args.ph, args.crop]
        if any(val is None for val in required_fields):
            print("⚠️ Please provide all required inputs: --latitude --longitude --nitrogen --phosphorus --potassium --ph --crop")
            exit()

        if not joblib.os.path.exists(MODEL_FILE):
            print("⚠️ Model not found. Train it first with --train")
            exit()

        model = joblib.load(MODEL_FILE)
        input_data = {
            'latitude': args.latitude,
            'longitude': args.longitude,
            'nitrogen': args.nitrogen,
            'phosphorus': args.phosphorus,
            'potassium': args.potassium,
            'ph': args.ph
        }

        soil_type = predict_soil_type(model, input_data)
        print(f"🧪 Predicted Soil Type: {soil_type}")

        is_suitable, message = check_crop_suitability(args.crop, input_data, soil_type)
        print(message)