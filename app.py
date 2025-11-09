# ----------------------------------------
# House Price Prediction App
# ----------------------------------------

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
import traceback

app = Flask(__name__)
CORS(app)

# 1. Load the Trained Model
MODEL_PATH = 'random_forest_model.pkl'

try:
    with open(MODEL_PATH, 'rb') as file:
        model_data = pickle.load(file)

    model = model_data['model']
    MODEL_FEATURES = model_data['features']
    print("Model and feature list loaded successfully!")

except FileNotFoundError:
    print("Model file not found. Please check the MODEL_PATH.")
    model = None
    MODEL_FEATURES = []

except Exception as e:
    print(f"Error loading model: {str(e)}")
    traceback.print_exc()
    model = None
    MODEL_FEATURES = []


# 2. Home Route
@app.route('/')
def home():
    return jsonify({"message": "House Price Prediction API is running!"})


# 3. Prediction Endpoint
@app.route('/predict', methods=['POST'])
def predict():
    """Receives data from the frontend and returns a prediction."""
    if model is None:
        return jsonify({'error': 'Prediction model not loaded.'}), 500

    try:
        # Get data from frontend
        data = request.get_json(force=True)
        if not data:
            return jsonify({'error': 'No input data received.'}), 400

        # Convert JSON to DataFrame
        df = pd.DataFrame([data])

        # Debug print (optional)
        print(f"Received Input: {df.to_dict(orient='records')[0]}")

        # Predict using model pipeline
        prediction = model.predict(df)
        output = round(float(prediction[0]), 2)

        print(f"Predicted Price: ${output:,.2f}")

        return jsonify({
            'prediction': f"${output:,.2f}",
            'raw_value': output
        })

    except Exception as e:
        return jsonify({
            'error': f'An error occurred during prediction: {str(e)}',
            'trace': traceback.format_exc()
        }), 500


# 4. Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
