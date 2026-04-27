import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

SYMPTOMS = [
    'fever', 'cough', 'headache', 'fatigue', 'shortness_of_breath',
    'chest_pain', 'nausea', 'sore_throat', 'runny_nose', 'muscle_pain',
    'loss_of_taste', 'rash', 'diarrhea', 'dizziness'
]

DISEASE_PROFILES = {
    'Flu':              [1,1,1,1,0,0,1,0,0,1,0,0,0,0],
    'COVID-19':         [1,1,1,1,1,0,0,0,0,1,1,0,0,0],
    'Common Cold':      [0,1,1,0,0,0,0,1,1,0,0,0,0,0],
    'Pneumonia':        [1,1,0,1,1,1,0,0,0,0,0,0,0,0],
    'Gastroenteritis':  [1,0,1,1,0,0,1,0,0,0,0,0,1,0],
    'Food Poisoning':   [0,0,1,1,0,0,1,0,0,0,0,0,1,1],
    'Dengue':           [1,0,1,1,0,0,0,0,0,1,0,1,0,1],
    'Typhoid':          [1,0,0,1,0,0,1,0,0,1,0,0,1,0],
    'Migraine':         [0,0,1,0,0,0,1,0,0,0,0,0,0,1],
    'Heart Disease':    [0,0,0,1,1,1,0,0,0,0,0,0,0,1],
}

def generate_samples(disease, profile, n=50):
    rows = []
    for _ in range(n):
        row = []
        for val in profile:
            if val == 1:
                row.append(1 if np.random.random() > 0.1 else 0)
            else:
                row.append(1 if np.random.random() < 0.1 else 0)
        row.append(disease)
        rows.append(row)
    return rows

all_rows = []
for disease, profile in DISEASE_PROFILES.items():
    all_rows.extend(generate_samples(disease, profile, n=50))

df = pd.DataFrame(all_rows, columns=SYMPTOMS + ['disease'])
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

X = df[SYMPTOMS]
y = df['disease']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model accuracy: {accuracy * 100:.2f}%')
print(f'Training samples: {len(X_train)}')
print(f'Test samples: {len(X_test)}')

model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
joblib.dump({'model': model, 'symptoms': SYMPTOMS}, model_path)
print(f'Model saved to {model_path}')