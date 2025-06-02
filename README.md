
# Collaborative Medical Documentation System  
*Optical Character Recognition Pipeline*

---

## Process Overview  

###  OCR Processing Pipeline
**Step 1 - Document Capture**  
   - Upload an image of the document (via picture or image uploads)

**Step 2 - Image Preprocessing**  
   - Use  auto-capture guidance (e.g., edge detection) to ensure document alignment.
   - conduct image preprocessing (Deskewing, Contrast enhancement, binarization)
   - Perform region detection to identify important document elements and regions, such as lines, words, and text blocks. This allows the system to segment the detected regions.
   - note the coordinates of the detected regions are noted and and crop the regions are cropped.
   -The cropped segments are then classified as handwritten or typed before being passed to OCR models for text extraction.


**Step 3 - OCR processing**  
   - conduct text extraction from scanned regions.   

---
### 📄 Voice Transcription Integration Points
```plaintext
------------------------------------------
This is the point where the OCR and voice transcription pipelines meet and integrate.
------------------------------------------
```
**Step 4 - Text and context Classification**
- Through classification, refine the extracted data with medically fine-tuned models.
   ```
   - refine the extracted text using a BERT model.
   - Group sentences by semantic meaning.
   ```

**Step 6 - Data structuring**
- Identify key entities from contextualized text
- Perform entity recognition on the extracted data to structure the data into fields such as (patient ID, date, medication, dosage).

**Step 7 - Validation and Error Checking**
 - Human-in-the-Loop and cross referencing.
 - users review the captured data via a dashboard and correct them as required.
 **EHR Integration**
_use postgreSQL to store structured data temporarily before EHR sync__
_ HL7 Compliance: Convert structured data into HL7 standards for EHR systems.__
_Enable Web Apps (PWAs) to work offline and sync later__

**Technical Requirements**
🌐 Languages
- Python 3
- JavaScript

📦 Python Modules
#### Core Processing
- subprocess  # OS calls


#### Machine Learning
- Google Cloud Vision AI
- Tesseract OCR
- Pytesseract
- BERT
- SpaCy
- YOLOv5

#### NLP Processing
- spacy
- datasets
- sklearn
- transformers

#### Utilities
- numpy
- evaluate  

  
### 🧠 Models
__Pretrained models:__
   [download_link](https://drive.google.com/drive/folders/1JPqmJOLDqAob1TiI3wN7B6YOVN_9-NXo?usp=drive_link)

__Custom Trained Models:__
   [download link](https://drive.google.com/drive/folders/1BP2W85IG9WiNkp2eSlhge30g5asz91xF?usp=drive_link)


