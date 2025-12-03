from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from src.pipelines.predict_pipeline import CustomData, PredictPipeline 

application = Flask(__name__)
app = application

# 1. Home Page Route: Renders the form/results page.
@app.route('/')
def index():
    # Render home.html for the initial view
    return render_template('home.html', results=None)

# 2. Prediction Route: Handles form submission and re-renders home.html with results
@app.route('/predict_datapoint', methods = ['GET','POST'])
def predict_datapoint():
    if request.method == 'GET':
        # If accessing directly, just show the form/home page without results
        return render_template('home.html', results=None)
    else:
        # Data extraction for POST request
        try:
            # Note: The input names must match the corrected HTML names (e.g., race_ethnicity)
            data = CustomData(
                gender=request.form.get('gender'),
                # Using the correct name 'race_ethnicity' from the form
                race_ethnicity=request.form.get('race_ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                # Correctly mapping form names to CustomData attributes
                reading_score=float(request.form.get('reading_score')), 
                writing_score=float(request.form.get('writing_score')) 
            )
        
            pred_df = data.get_data_as_data_frame()
            print("Input DataFrame for Prediction:\n", pred_df)

            predict_pipeline = PredictPipeline()
            results_array = predict_pipeline.predict(pred_df)
            
            # Format the result for display
            predicted_score = round(results_array[0], 2)
            display_result = f"Predicted Math Score: {predicted_score}"
            
            # Re-render home.html, passing the result variable
            return render_template("home.html", results=display_result)
            
        except Exception as e:
            # Handle prediction/pipeline errors gracefully
            error_message = f"An error occurred: {e}"
            print(error_message)
            # Re-render home.html, passing the error message
            return render_template("home.html", results=f"ERROR: {error_message}")


if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug = True)