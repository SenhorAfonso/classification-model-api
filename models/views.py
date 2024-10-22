import pickle
from django.http import JsonResponse
from .model.load_model import load_model
import json
import torch
import os
from django.views.decorators.csrf import csrf_exempt


def _load_vectorizer():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    vectorizer_path = os.path.join(base_dir, 'model\\vectorizer.pkl')

    with open(vectorizer_path, 'rb') as f:
        return pickle.load(f)


def _get_model_inputs_from_payload(email_body):
    vectorizer = _load_vectorizer()

    email_vector = vectorizer.transform([email_body]).toarray()
    model_inputs = torch.tensor(email_vector, dtype=torch.float32)

    print(model_inputs)
    return model_inputs


def predict_from_payload(email_body):
    model_inputs = _get_model_inputs_from_payload(email_body)

    model = load_model()
    with torch.no_grad():
        outputs = model(model_inputs)
        _, predicted = torch.max(outputs, 1)

    return {"predicted": predicted.item()}


def _get_model_inputs_from_request(request):
    body = json.loads(request.body)
    vectorizer = _load_vectorizer()

    request_email = body['email']
    email_vector = vectorizer.transform([request_email]).toarray()
    model_inputs = torch.tensor(email_vector, dtype=torch.float32)

    print(model_inputs)
    return model_inputs


@csrf_exempt
def predict_from_request(request):
    model_inputs = _get_model_inputs_from_request(request)

    model = load_model()
    with torch.no_grad():
        outputs = model(model_inputs)
        _, predicted = torch.max(outputs, 1)

    return JsonResponse({ "predicted": predicted.item()})
