
# Medical Application Documentation System  
*Focused on Robust Voice Transcription Pipeline*

---

## Process Overview  

### 🎤 Audio Processing Pipeline
**Step 1 - Audio Input**  
   _How we take and segment audio input_

**Step 2 - Audio Preprocessing**  
   _Amplification and denoising the audio_

**Step 3 - Transcription**  
   _Convert audio to text using speech recognition_

**Step 3.5 - Speaker Diarization**  
   _Classify speakers and timestamp their utterances_

---
### 📄 OCR Integration Points
```plaintext
------------------------------------------
Non-classified OCR input enters here
------------------------------------------
```
**Step 4 - Text Classification**
_Group contextualized text using diarization data_

**Step 5 - Context Classification**
_Group sentences by semantic meaning_

**Step 6 - Entity Extraction**
_Identify key entities from contextualized text_
```
------------------------------------------
Classified OCR input enters here
------------------------------------------
```
**Step 7 - Data Processing**
__Route extracted data to appropriate destinations__


**Technical Requirements**
🌐 Languages
- Python 3
- JavaScript

📦 Python Modules
#### Core Processing
- subprocess  # OS calls
- ffmpeg      # Audio modification

#### Machine Learning
- torch
- torchaudio
- denoiser
- pyannote.audio
- faster_whisper
- speechbrain

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


