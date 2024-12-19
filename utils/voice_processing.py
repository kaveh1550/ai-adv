import deepspeech
import numpy as np
import librosa
import pyttsx3

# تبدیل فایل صوتی به متن با DeepSpeech
def convert_audio_to_text(file_path):
    model = deepspeech.Model("deepspeech-0.9.1-models.tflite")
    audio, sr = librosa.load(file_path, sr=16000)
    audio_data = np.array(audio, dtype=np.float32)
    text = model.stt(audio_data)
    return text

# تولید صدا از متن با PyDub
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
