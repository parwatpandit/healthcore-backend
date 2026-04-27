import os
import joblib
import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

def load_model():
    if not os.path.exists(MODEL_PATH):
        return None, None
    data = joblib.load(MODEL_PATH)
    return data['model'], data['symptoms']


class DiseasePredictionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        model, symptoms = load_model()

        if model is None:
            return Response(
                {'error': 'ML model not found. Please train the model first.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        provided_symptoms = request.data.get('symptoms', [])

        if not provided_symptoms:
            return Response(
                {'error': 'Please provide at least one symptom.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Build feature vector
        feature_vector = [1 if s in provided_symptoms else 0 for s in symptoms]
        input_array = np.array(feature_vector).reshape(1, -1)

        # Predict
        prediction = model.predict(input_array)[0]
        probabilities = model.predict_proba(input_array)[0]
        classes = model.classes_

        # Top 3 predictions with probabilities
        top_indices = np.argsort(probabilities)[::-1][:3]
        top_predictions = [
            {
                'disease': classes[i],
                'confidence': round(float(probabilities[i]) * 100, 2)
            }
            for i in top_indices
            if probabilities[i] > 0
        ]

        return Response({
            'primary_prediction': prediction,
            'top_predictions': top_predictions,
            'symptoms_analysed': provided_symptoms,
            'total_symptoms_checked': len(symptoms),
        })


class SymptomsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        _, symptoms = load_model()
        if symptoms is None:
            return Response(
                {'error': 'Model not found'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response({'symptoms': symptoms})