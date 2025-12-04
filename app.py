from flask import Flask, render_template, request, jsonify
# Assuming the utility script for prediction is named 'util.py' and contains the ValuePredictor class/function
# from util import ValuePredictor 
# Note: Since the core ML logic file (util.py) was not provided, 
# I will use a simple placeholder function for the prediction logic.

app = Flask(__name__)

# --- Placeholder Prediction Function ---
def get_prediction(data):
    """
    Simulates a machine learning prediction based on input data.
    In a real app, this would load a trained model (e.g., pickle file) and run the prediction.
    The current version is a simple rule-based simulation for demonstration.
    """
    try:
        # Extract numerical features
        reading_score = float(data.get('reading_score'))
        writing_score = float(data.get('writing_score'))
        
        # Simple linear model simulation: Math_Score = 0.5 * Reading + 0.5 * Writing + Base_Bias
        base_bias = 5.0
        
        # Apply categorical feature bias (simulation)
        if data.get('gender') == 'female':
            base_bias += 2.0
        if data.get('lunch') == 'free/reduced':
            base_bias -= 5.0
        if data.get('test_preparation_course') == 'completed':
            base_bias += 8.0
            
        # Calculate score (clamped between 0 and 100)
        predicted_score = (0.5 * reading_score) + (0.5 * writing_score) + base_bias
        
        # Ensure score is within bounds
        final_score = round(max(0, min(100, predicted_score)), 2)
        
        return f"Predicted Score: {final_score}"

    except Exception as e:
        return f"ERROR: Invalid input data. Please check all fields. Detail: {e}"


# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Home route: Handles the prediction form display and prediction results.
    """
    # If the user lands on the homepage, render the template with no results initially
    return render_template('home.html', results=None)

@app.route('/predict', methods=['POST'])
def predict_datapoint():
    """
    Handles the prediction request from the form submission.
    """
    if request.method == 'POST':
        # Get all form data
        data = request.form

        # Collect data for prediction in a dictionary
        input_data = {
            'gender': data.get('gender'),
            'race_ethnicity': data.get('race_ethnicity'),
            'parental_level_of_education': data.get('parental_level_of_education'),
            'lunch': data.get('lunch'),
            'test_preparation_course': data.get('test_preparation_course'),
            'reading_score': data.get('reading_score'),
            'writing_score': data.get('writing_score')
        }
        
        # Get the prediction result using the placeholder function
        prediction_result = get_prediction(input_data)
        
        # Re-render the home page with the prediction result and all form data
        # so the user can see their input again.
        return render_template('home.html', results=prediction_result, request=request)

@app.route('/dashboard')
def show_dashboard():
    """
    Route for the interactive scatter plot dashboard.
    """
    return render_template('dashboard.html')

@app.route('/analysis')
def show_analysis():
    """
    Route for the feature impact analyzer page.
    """
    return render_template('analysis.html')

@app.route('/data_health')
def show_data_health():
    """
    Route for the data health monitor page.
    """
    return render_template('data_health.html')

@app.route('/model_registry')
def show_model_registry():
    """
    NEW Route for the Model Registry and Version Control page.
    """
    return render_template('model_registry.html')


if __name__ == '__main__':
    # When running locally, use a specified port
    app.run(debug=True, port=8080)