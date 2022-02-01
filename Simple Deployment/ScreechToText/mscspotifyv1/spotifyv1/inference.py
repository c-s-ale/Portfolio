import torch
from transformers import Speech2TextProcessor, Speech2TextForConditionalGeneration
import librosa

class WakeWord:
    def __init__(self, wakeword="") -> None:
        self.wakeword = wakeword

    def get_wakeword(self):
        return self.wakeword

    def set_wakeword(self, wakeword):
        self.wakeword = wakeword

    def detect_wakeword_and_command(self, transcription):
        command = False
        command_string = []
        does_not_contain_string = []
        wake_word_string = ""
        for word in transcription[0].split(" "):
            if word == self.wakeword:
                command = True
                wake_word_string = word
                continue

            if command:
                command_string.append(word)
            else:
                does_not_contain_string.append(word)
            
            
        if command_string:
            return " ".join(command_string), wake_word_string, " ".join(does_not_contain_string)
        else:
            return "", wake_word_string, does_not_contain_string

def load_models():
    model = Speech2TextForConditionalGeneration.from_pretrained("facebook/s2t-small-librispeech-asr")
    processor = Speech2TextProcessor.from_pretrained("facebook/s2t-small-librispeech-asr")

    return model, processor

def convert_to_transcription(file):
    model, processor = load_models()
    #downsampling since this is recorded at a sample rate of 48,000 and the model is trained on 16,000
    signal, sr = librosa.load(file, sr=16000)
    inputs = processor(signal, sampling_rate=sr, return_tensors="pt")
    generated_ids = model.generate(input_features=inputs["input_features"], attention_mask=inputs["attention_mask"])
    transcription = processor.batch_decode(generated_ids)
    return transcription