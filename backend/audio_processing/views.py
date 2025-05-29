# audio_processing/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import tempfile
import os
from .processing import transcribe_audio

@csrf_exempt
def transcribe_view(request):
    full_text = []
    if request.method == "POST" and request.FILES.get("audio"):
        audio_file = request.FILES["audio"]
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            for chunk in audio_file.chunks():
                temp_audio.write(chunk)
            temp_audio_path = temp_audio.name

        try:
            transcription = transcribe_audio(temp_audio_path)
            full_text.append([t[2] for t in transcription])
            os.remove(temp_audio_path)
            return JsonResponse({"transcription": full_text})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "POST a valid audio file."}, status=400)
