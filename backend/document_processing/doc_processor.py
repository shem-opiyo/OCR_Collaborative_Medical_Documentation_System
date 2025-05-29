from django.conf import settings
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import os

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # goes from backend/ to project_root/
# MODEL_DIR = os.path.join(BASE_DIR, "models", "nlpie-distil-clinicalbert-0.66")
class GrammarCorrectionError(Exception):
    """Custom exception raised during grammar correction."""
    pass
class ClassifierError(Exception):
    """Custom exception raised during loading sentence classifier error."""
    pass

class LoadingNER_Error(Exception):
    """Custom exception raised during loading sentence classifier error."""
    pass

grammar_model = None
grammar_settings = None

classifier = None
tokenizer = None

entity_recognizers = []

# Lazy load modules
_torch = None

def get_torch():
    global _torch
    if _torch == None:
        import torch
        _torch = torch
        return _torch

def load_grammar():
    """Load the grammar correction model."""
    from happytransformer import HappyTextToText, TTSettings
    global grammar_model, grammar_settings
    try:
        print("Loading grammar correction model...")
        grammar_model = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
        grammar_settings = TTSettings(num_beams=5, min_length=1)
        print("Grammar correction model loaded successfully.")
    except Exception as e:
        raise GrammarCorrectionError(f"Failed to load grammar correction model: \n---------------\n{e}\n----------------")

def load_classifier():
    """Load the sentence classifier model."""
    from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoTokenizer
    model_name = "nlpie-distil-clinicalbert-0.66"
    global classifier, tokenizer

    try:
        print("Loading classifier model...")
        classifier = AutoModelForSequenceClassification.from_pretrained(f"self_trained_models/{model_name}")
        tokenizer = AutoTokenizer.from_pretrained(f"self_trained_models/{model_name}")        
        print("Classifier model successfully loaded")
    except Exception as e:
        raise ClassifierError(f"Failed to load sentence classifier model: \n---------------\n{e}\n----------------")

def load_entity_recognizers():
    import spacy
    global entity_recognizers
    ner_models = ["en_core_web_sm", "continual_learning_ner_combined"]
    for model_name in ner_models:
        try:
            print(f"Loading NER model... {model_name}")
            entity_recognizers.append(spacy.load(f"pretrained_models/{model_name}"))
            print(f"Successfully loaded {model_name}")
        except Exception as e:
            raise LoadingNER_Error(f"Failed to load NER model: {model_name} \n---------------\n{e}\n----------------")



if settings.LOAD_SPEECH_MODELS_ON_STARTUP:
    try:
        load_grammar()
        load_classifier()
        if grammar_model and classifier:
            print("----\nGrammar model loaded successfully\n---")
    
    except Exception as e:
        grammar_model = None
        grammar_settings = None

def correct_grammar(text):
    if not grammar_model or not grammar_settings:
        load_grammar()
    try:
        print(f"Correcting grammar for text: '{text}'")
        result = grammar_model.generate_text(text, args=grammar_settings)
        corrected_text = result.text
        print(f"Grammar corrected text: '{corrected_text}'")
        return corrected_text
    except Exception as e:
        raise GrammarCorrectionError(f"Error during grammar correction: {e}")
    
def classify_sentence(sentence):
    get_torch()
    if classifier == None:
        load_classifier()

        
    class_labels = ["SmallTalk", "Demographics", "treatmentPlan", "patientHistory", "symptoms", "Test_Results", "allergies", "pre_existingConditions", "diagnosis", "familyHistory"]
    inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding="max_length", max_length=128)
    outputs = classifier(**inputs)
    logits = outputs.logits
    probabilities = _torch.softmax(logits, dim=1).detach().cpu().numpy()[0]
    predicted_class = int(probabilities.argmax())
    return class_labels[predicted_class]
    
def extract_entities(sentence):
    """
    Extracts entities from a sentence and returns them as a dictionary
    where keys are entity labels and values are sets of entity texts.
    """
    output_dict = {}
    if len(entity_recognizers) == 0:
        load_entity_recognizers()
    for model in entity_recognizers:
        doc = model(sentence)
        for ent in doc.ents:
            label = ent.label_
            text = ent.text.replace("," , "")
            if label not in output_dict:
                output_dict[label] = set()
            output_dict[label].add(text)
            
    newOutput = dict()
    for output in output_dict:
        newOutput[output] = list(output_dict[output] )
        
    return newOutput

if __name__ == "__main__":
    text_to_correct = "Thes is an exmaple sentnce with mistaks."
    if grammar_model and grammar_settings:
        try:
            corrected_text = correct_grammar(text_to_correct)
            print(f"\nOriginal text: {text_to_correct}")
            print(f"Corrected text: {corrected_text}")
        except GrammarCorrectionError as e:
            print(f"\nError during grammar correction process: {e}")
