from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import tempfile, json
import os
from .processing import correct_grammar, classify_sentence, extract_entities

# Create your views here.

@csrf_exempt
def correct_grammar_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            text_to_correct = data.get('text')

            if text_to_correct is not None:
                corrected_text = correct_grammar(text_to_correct)
                return JsonResponse({"corrected_text": corrected_text})
            else:
                return JsonResponse({"error": "Please provide 'text' in the POST request body."}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format in the request body."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "POST request with 'text' data is required."}, status=400)

@csrf_exempt
def classify_text_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            text_to_classify = data.get('text')

            if text_to_classify is not None:
                predicted_class = classify_sentence(text_to_classify)
                return JsonResponse({"predicted_class": predicted_class})
            else:
                return JsonResponse({"error": "Please provide 'text' to classify in the POST request body."}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format in the request body."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "POST request with 'text' data is required for classification."}, status=400)

@csrf_exempt
def extract_entities_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            sentence_to_extract = data.get('text')

            if sentence_to_extract is not None:
                extracted_entities_dict = extract_entities(sentence_to_extract)
                return JsonResponse(extracted_entities_dict)
            else:
                return JsonResponse({"error": "Please provide 'sentence' for entity extraction in the POST request body."}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format in the request body."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "POST request with 'sentence' data is required for entity extraction."}, status=400)