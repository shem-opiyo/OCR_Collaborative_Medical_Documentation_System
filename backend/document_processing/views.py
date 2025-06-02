from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, generics
from django.views.decorators.csrf import csrf_exempt
from .serializers import UploadedImageSerializer
from .models import UploadedImage
# from .processing import process_image_ocr  # You'll define this
import os
from django.conf import settings
from django.http import JsonResponse
import cv2
from . import utility
import numpy as np
from PIL import Image
import torch
import pytesseract
import matplotlib.pyplot as plt
import requests
from .doc_processor import classify_sentence, extract_entities
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from google.cloud import vision
import io

# # Load once when the server starts
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# MODEL_PATH = os.path.join(BASE_DIR, "self_trained_models", "distil-clinicalbert-0.66")

tokenizer = AutoTokenizer.from_pretrained("self_trained_models/nlpie-distil-clinicalbert-0.66")
model = AutoModelForSequenceClassification.from_pretrained("self_trained_models/nlpie-distil-clinicalbert-0.66")

#upload image
class UploadedImageCreateView(generics.CreateAPIView):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer
    parser_classes = [MultiPartParser, FormParser]

class UploadedImageListView(generics.ListAPIView):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer

#preprocess image
@csrf_exempt
def preprocess_image(request):
    try:
        # Assume latest uploaded file is to be processed
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads/images')
        processed_dir = os.path.join(settings.MEDIA_ROOT, 'uploads/image/processed')
        image_files = sorted(
            [f for f in os.listdir(upload_dir) if f.endswith(('.jpg', '.jpeg', '.png'))],
            key=lambda x: os.path.getmtime(os.path.join(upload_dir, x)),
            reverse=True
        )

        if not image_files:
            return JsonResponse({'error': 'No image found in upload directory.'}, status=404)

        latest_image_path = os.path.join(upload_dir, image_files[3])
        print(f"Processing image: {latest_image_path}")

        # Step 1: Load image
        img = cv2.imread(latest_image_path)
        if img is None:
            return JsonResponse({'error': 'Unable to load image.'}, status=400)
        
        img_original = img.copy()   #create a copy of the image

        # Step 2: Detect edges
        edged = utility.detect_edge(img)

        # Step 3: Align image
        aligned_image = utility.align_image(edged, img, img_original)

        # Step 4: Enhance contrast
        enhanced_image = utility.enhance_contrast(aligned_image)

        # Optional: Save processed image
        processed_path = os.path.join(processed_dir, 'processed_image.jpg')
        cv2.imwrite(processed_path, enhanced_image)

        return JsonResponse({
            'message': 'Image processed successfully',
            'processed_image_path': os.path.join(settings.MEDIA_URL, 'uploads/image/processed/processed_image.jpg')
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt
def thresholding(image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(
        img_gray, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )
    return thresh

# Helper function to classify the lines of text
def classify_text(text):
    """
    Classifies a single line of text using the classify_sentence function.
    """
    if not text.strip():
        return "no_text_provided"
    try:
        return classify_sentence(text)
    except Exception as e:
        return f"classification_error: {str(e)}"

#handle named entity recognition
def extract_entities_from_sentence(text):
    """
    Helper function to extract named entities from a sentence using preloaded NER models.
    """
    if not text or not text.strip():
        return {"error": "No valid text provided for entity extraction."}

    try:
        extracted_entities = extract_entities(text)
        return extracted_entities
    except Exception as e:
        return {"error": f"Entity extraction failed: {str(e)}"}

#handle text extraction
@csrf_exempt
def process_image_view(request):
    # Path to input image 
    img_path = os.path.join(settings.MEDIA_ROOT, 'uploads/images/processed/processed_image.jpg') 
    if not os.path.exists(img_path):
        return JsonResponse({'error': 'Image not found.'}, status=404)

    # Load & (if necessary) resize
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, _ = img.shape
    if w > 1000:
        new_w = 1000
        ar = w / h
        new_h = int(new_w / ar)
        img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    print("Image successfully loaded and ready for processing")

    # Thresholding and dilation to detect the lines
    thresh = thresholding(img)
    kernel_lines = np.ones((3, 85), np.uint8)
    dilated = cv2.dilate(thresh, kernel_lines, iterations=1)
    contours, _ = cv2.findContours(
        dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    lines = sorted(contours, key=lambda c: cv2.boundingRect(c)[1])

    #confirm line's detection
    print("line processing complete")

    # dilation to detect Words
    kernel_words = np.ones((3, 15), np.uint8)
    dilated2 = cv2.dilate(thresh, kernel_words, iterations=1)
    words_list = []
    for line in lines:
        x, y, w, h = cv2.boundingRect(line)
        roi = dilated2[y:y+h, x:x+w]
        cnts, _ = cv2.findContours(
            roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
        for word in sorted(cnts, key=lambda c: cv2.boundingRect(c)[0]):
            if cv2.contourArea(word) < 400:
                continue
            x2, y2, w2, h2 = cv2.boundingRect(word)
            words_list.append([x + x2, y + y2, x + x2 + w2, y + y2 + h2])

    #confirm word processing
    print("word processing complete")

    # Load YOLOv5
    print("Loading Yolo...")
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    print("Successfully loaded Yolo")

    class_names = model.names

    # Prepare text output file
    txt_path = os.path.join(settings.MEDIA_ROOT, 'ocr_output2.txt')
    with open(txt_path, 'a', encoding='utf-8') as txt_file:
        results_data = []      

        for idx, (x1, y1, x2, y2) in enumerate(words_list):
            roi = img[y1:y2, x1:x2]
            preds = model(roi, size=320).xyxy[0]

            if len(preds):
                best = preds[preds[:, 4].argmax()]
                label = class_names[int(best[5].item())]
            else:
                label = 'typed'

            if label == 'typed':
                pil_roi = Image.fromarray(roi).convert('L')
                cfg = r'--oem 3 --psm 7'
                print("Tesseract loading...")
                # pytesseract.pytesseract.tesseract_cmd = r"C:\Users\HP\Saved Games\android\python\Lib\site-packages\tesseract"
                text = pytesseract.image_to_string(
                    pil_roi, lang='eng', config=cfg
                ).strip()
                # print("THis is nice")
                line = f"Word #{idx} ({x1},{y1},{x2},{y2}) → {repr(text)}\n"

                #classify the image into classes
                predicted_class = classify_sentence(text)
                
                # extract entities from text
                entities = extract_entities_from_sentence(text)

                results_data.append({
                    'index': idx,
                    'bbox': [x1, y1, x2, y2],
                    'label': 'typed',
                    'text': text,
                    "predicted_class": predicted_class,
                    "entities": entities
                })
            else:
                # Convert ROI to bytes for Google Cloud Vision
                client = vision.ImageAnnotatorClient()
                success, encoded_image = cv2.imencode('.png', roi)
                content = encoded_image.tobytes()

                image = vision.Image(content=content)
                response = client.text_detection(image=image)
                annotations = response.text_annotations

                if annotations:
                     text = annotations[0].description.strip()
                else:
                            text = ""

                line = f"Word #{idx} ({x1},{y1},{x2},{y2}) → <{label} detected: {repr(text)}>\n"

                #classify the image into classes
                predicted_class = classify_sentence(text)
                entities = extract_entities_from_sentence(text)
                results_data.append({
                    'index': idx,
                    'bbox': [x1, y1, x2, y2],
                    'label': label,
                    'text': None,
                    "predicted_class": predicted_class,
                    "entities": entities
                })

            # write each line immediately
            txt_file.write(line)

    #process the results_data
    return JsonResponse({'results': results_data})