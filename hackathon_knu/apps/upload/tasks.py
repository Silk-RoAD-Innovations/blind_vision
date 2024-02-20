from transformers import BlipProcessor, BlipForConditionalGeneration
from googletrans import Translator
import json
import requests
import torch

# Check if CUDA is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Loading model (load it once)
model = BlipForConditionalGeneration.from_pretrained("models").to(device)
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")

url = "https://tts.ulut.kg/api/tts"


def translate_to_kyrgyz(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='kyrgyz').text
    return translated_text

def return_text_from_image(raw_image):
    inputs = processor(raw_image, return_tensors="pt", max_length=35).to(device)
    out = model.generate(**inputs)
    image_description = processor.decode(out[0], skip_special_tokens=True)
    kyrgyz_text = translate_to_kyrgyz(image_description)
    return kyrgyz_text

def generate_audio(text_):
    payload = json.dumps({
        "text": text_,
        "speaker_id": 1
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer zBvc7mkrGJHsFRkx7By91tUVSDpYuYji60bKyMjux80o3eFayeVPAq0mljwKmTvl'
    }
    response = requests.post(url, headers=headers, data=payload, verify=False)
    audio_data = response.content
    return audio_data