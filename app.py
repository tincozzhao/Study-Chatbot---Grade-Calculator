from flask import Flask, jsonify
import requests
from flask_cors import CORS
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn import linear_model

app = Flask(__name__)
CORS(app)

@app.route("/grade_predictor")
def grade_predictor():

    from flask import request
    df = pd.read_csv("student_performance.csv")

    X = df[['AttendanceRate', 'StudyHoursPerWeek', 'PreviousGrade']]
    Y = df[['FinalGrade']]

    # le = LabelEncoder()
    # gender_Encoded = le.fit_transform(df['Gender'])
    # X['Gender'] = gender_Encoded
    # ParentalSupport_Encoded = le.fit_transform(df['ParentalSupport'])
    # X['ParentalSupport'] = ParentalSupport_Encoded

    model = linear_model.LinearRegression()
    model.fit(X, Y)

    # Get user input from query params
    try:
        attendance = float(request.args.get('attendance', 0))
        study = float(request.args.get('study', 0))
        previous = float(request.args.get('previous', 0))
        gender = request.args.get('gender', 'none')
        parental = request.args.get('parental', 'no')
    except Exception as e:
        return jsonify({'error': 'Invalid input', 'details': str(e)}), 400

    # Encode gender and parental support using same label encoder
    # gender_map = {v: le.transform([v])[0] if v in df['Gender'].unique() else 0 for v in ['male','female']}
    # parental_map = {v: le.transform([v])[0] if v in df['ParentalSupport'].unique() else 0 for v in ['low', 'medium', 'high']}
    # gender_encoded = gender_map.get(gender, 0)
    # parental_encoded = parental_map.get(parental, 0)

    # Predict
    pred = model.predict([[attendance, study, previous ]])
    try:
        pred_val = float(pred[0][0])
    except Exception:
        pred_val = float(pred[0])
    # Letter grade
    def letter_grade(v):
        if v>=90: return 'A'
        if v>=80: return 'B'
        if v>=70: return 'C'
        if v>=60: return 'D'
        return 'F'
    return jsonify({
        'predicted': round(pred_val,1),
        'letter': letter_grade(pred_val)
    })

print("Server started.")
app.run(host = '0.0.0.0', port=80)
