#!/usr/bin/env python3
"""Generate a synthetic student_performance.csv with clear influence
from AttendanceRate, StudyHoursPerWeek, PreviousGrade, Gender, and ParentalSupport.
"""
import csv
import random
import math
from pathlib import Path

OUT = Path(__file__).resolve().parents[0].parent / 'student_performance.csv'

def clip(x, lo, hi):
    return max(lo, min(hi, x))

def generate_row(i):
    # Base previous grade (0-100) with wide variability
    previous = clip(random.gauss(70, 18), 0, 100)

    # Attendance correlated with previous but with noise
    attendance = clip(random.gauss(previous * 0.9 + random.uniform(-10,10), 8), 20, 100)

    # Study hours influenced by previous (lower previous may study more or less) and attendance
    # Produce a wide range 0-40
    base = (100 - previous) / 3  # students with lower previous often study more
    attendance_influence = (attendance - 60) / 10
    study = clip(random.gauss(6 + base + attendance_influence, 5), 0, 40)

    # Gender and parental support categories
    gender = random.choices(['male','female'], weights=[0.48, 0.52])[0]
    parental = random.choices(['low','medium','high'], weights=[0.2,0.5,0.3])[0]

    # Numeric adjustments
    parental_bonus = {'low': -5.0, 'medium': 0.0, 'high': 5.0}[parental]
    gender_bonus = 1.5 if gender == 'female' else 0.0

    # Final grade formula with clear contributions from features
    # Weights chosen to make each feature meaningful.
    final = (
        0.4 * previous +                # prior knowledge
        0.25 * attendance +              # attendance matters
        1.6 * study +                    # study hours significant
        parental_bonus +                 # parental support shift
        gender_bonus +                   # small gender effect
        random.gauss(0, 6)               # noise
    )

    final = clip(final, 0, 100)

    # Round numeric fields to sensible precision
    return {
        'AttendanceRate': round(attendance,1),
        'StudyHoursPerWeek': round(study,1),
        'PreviousGrade': round(previous,1),
        'Gender': gender,
        'ParentalSupport': parental,
        'FinalGrade': round(final,1)
    }

def main(n=600):
    random.seed(42)
    rows = []
    for i in range(n):
        rows.append(generate_row(i))

    # Ensure we produce some extreme low and high cases explicitly
    rows.append({'AttendanceRate': 30.0, 'StudyHoursPerWeek': 0.0, 'PreviousGrade': 20.0, 'Gender':'male', 'ParentalSupport':'low', 'FinalGrade': 10.0})
    rows.append({'AttendanceRate': 98.0, 'StudyHoursPerWeek': 35.0, 'PreviousGrade': 95.0, 'Gender':'female', 'ParentalSupport':'high', 'FinalGrade': 99.0})

    with OUT.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['AttendanceRate','StudyHoursPerWeek','PreviousGrade','Gender','ParentalSupport','FinalGrade'])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(f"Wrote {len(rows)} rows to {OUT}")

if __name__ == '__main__':
    main()
