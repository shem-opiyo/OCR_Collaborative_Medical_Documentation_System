from django.conf import settings


class LibraryLoadError(Exception):
    """Custom exception raised when library loading fails."""
    pass

class AudioProcessingError(Exception):
    """Custom exception raised during audio processing."""
    pass

class TranscriptionError(Exception):
    """Custom exception raised during audio transcription."""
    pass

libraries_loaded = False
denoising_model = None
transcription_model = None
diarization_classifier = None

# Utilities
_torchaudio = None
def get_torch_audio():
    global _torchaudio
    if _torchaudio == None:
        import torchaudio
        _torchaudio = torchaudio



def load_donoising():
    """Load the denoising model."""
    from denoiser import pretrained
    global denoising_model
    try:
        print("Loading denoising model...")
        denoising_model = pretrained.dns64()
        print("Denoising model loaded successfully.")
    except Exception as e:
        raise AudioProcessingError(f"Failed to load denoising model: \n---------------\n{e}\n----------------")

def load_whisper():
    """Load the Whisper transcription model."""
    from faster_whisper import WhisperModel
    global transcription_model
    try:
        print("Loading Whisper transcription model...")
        transcription_model = WhisperModel("tiny")
        print("Whisper transcription model loaded successfully.")
    except Exception as e:
        raise TranscriptionError(f"Failed to load Whisper transcription model: \n---------------\n{e}\n----------------")    

def load_diarization():
    """Load the diarization classifier."""
    from speechbrain.inference import EncoderClassifier
    global diarization_classifier
    try:
        print("Loading diarization classifier...")
        diarization_classifier = EncoderClassifier.from_hparams(
            source="pretrained_models/spkrec-xvect-voxceleb",
            run_opts={"device": "cpu"} # Change to "cuda" if using GPU
        )
        print("Diarization classifier loaded successfully.")
    except Exception as e:
        raise AudioProcessingError(f"Failed to load diarization classifier: \n---------------\n{e}\n----------------")

if settings.LOAD_SPEECH_MODELS_ON_STARTUP:
    try:
        print("Loading libraries...")
        import torchaudio
        libraries_loaded = True
        print("Libraries loaded successfully.\n---------------------------------------------------------------------\n")

        print("Loading pre-trained models...\n")
        

        load_donoising()
        load_whisper()
        load_diarization()

        if diarization_classifier and transcription_model and denoising_model:
            print("Pre-trained models loaded successfully.\n---------------------------------------------------------------------\n")
        else:
            print("Some models failed to load. Please check the logs above for details.")

    except ImportError as e:
        print(f"Error loading libraries: {e}")
        print("Some libraries are not installed. Please install them using the following command:")
        print("pip install torchaudio denoiser faster-whisper sklearn speechbrain happytransformer")
        raise LibraryLoadError("Failed to load one or more required libraries.")

    except LibraryLoadError as e:
        print(f"Critical error: {e}")
        # Handle the critical error of missing libraries - perhaps exit the script
        exit(1)

    except AudioProcessingError as e:
        print(f"Error during audio processing setup: {e}")
        # Handle specific audio processing setup errors
        denoising_model = None # Ensure the model is not used if loading failed

    except TranscriptionError as e:
        print(f"Error during transcription setup: {e}")
        # Handle specific transcription setup errors
        transcription_model = None # Ensure the model is not used if loading failed

    except Exception as e:
        print(f"An unexpected error occurred during initialization: {e}")
        # Handle any other unexpected errors during the initial setup
        denoising_model = None
        transcription_model = None
        diarization_classifier = None

def clean_audio(audio_path):
    if not denoising_model:
        get_torch_audio()
        load_donoising()
    try:
        print(f"Cleaning audio: {audio_path}")
        wav, sr = _torchaudio.load(audio_path)
        print("Done loading file to torch audio")
        denoised = denoising_model(wav[None])[0]
        print('Audio cleaned. Saving...')
        _torchaudio.save("temp_denoised.wav", denoised.detach().cpu().float(), denoising_model.sample_rate)
        print(f"Saved to temp_denoised.wav")
        return "temp_denoised.wav"
    except Exception as e:
        raise AudioProcessingError(f"Error during audio cleaning: {e}")

def transcribe_audio(audio_path):
    if not transcription_model:
        load_whisper()
    try:
        print(f"Transcribing audio: {audio_path}")
        # cleaned_path = clean_audio(audio_path)
        cleaned_path = audio_path
        segments, _ = transcription_model.transcribe(cleaned_path)
        transcription_results = [[s.start, s.end, s.text] for s in segments]
        print(f"Audio transcribed successfully.")
        print(transcription_results)
        return transcription_results
    except AudioProcessingError as e:
        raise TranscriptionError(f"Error during audio cleaning for transcription: {e}")
    except Exception as e:
        raise TranscriptionError(f"Error during audio transcription: {e}")

# Example usage with try-except blocks for individual functions
if __name__ == "__main__":
    audio_file = "audio.wav"  # Replace with your audio file path

    if libraries_loaded:
        try:
            cleaned_audio_path = clean_audio(audio_file)
            print(f"\nCleaned audio path: {cleaned_audio_path}")
        except AudioProcessingError as e:
            print(f"\nError during audio cleaning process: {e}")

        try:
            transcription = transcribe_audio(audio_file)
            print("\nTranscription:")
            for segment in transcription:
                print(f"[{segment[0]:.2f} - {segment[1]:.2f}] {segment[2]}")
        except TranscriptionError as e:
            print(f"\nError during audio transcription process: {e}")