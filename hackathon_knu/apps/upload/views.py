from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import UploadImagesSerializer
from .models import Photo
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from googletrans import Translator
import json
import requests
from django.http import HttpResponse
import torch
from django.core.cache import cache


# Check if CUDA is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Loading model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("models").to(device)
url = "https://tts.ulut.kg/api/tts"

# Store the model in cache
cache.set('blip_model', model, timeout=None)

def translate_to_kyrgyz(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='kyrgyz').text
    return translated_text


def return_text_from_image(raw_image: Image):
    # Get the model from cache
    cached_model = cache.get('blip_model')

    if cached_model is None:
        # Load the model if not in cache
        cached_model = BlipForConditionalGeneration.from_pretrained("models").to(device)
        cache.set('blip_model', cached_model, timeout=None)

    # unconditional image captioning
    inputs = processor(raw_image, return_tensors="pt", max_length=35).to(device)
    out = model.generate(**inputs)
    image_description = processor.decode(out[0], skip_special_tokens=True)

    print(image_description)

    kyrgyz_text = translate_to_kyrgyz(image_description)
    print(kyrgyz_text)
    return kyrgyz_text


def download_audio(text_):
    payload = json.dumps({
    "text": text_,
    "speaker_id": 1
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer zBvc7mkrGJHsFRkx7By91tUVSDpYuYji60bKyMjux80o3eFayeVPAq0mljwKmTvl'
    }
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    audio_data = response.content
    file_name = "audio_file.mp3"

    with open(file_name, "wb") as audio_file:
        audio_file.write(audio_data)


class ImageAPIVIew(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = UploadImagesSerializer
    
    def create(self, request, *args, **kwargs):
        uploaded_image = request.data.get('image')
        image = Image.open(uploaded_image)

        text_ = return_text_from_image(image)
        download_audio(text_)
        with open('audio_file.mp3', 'rb') as audio_file:
            response = HttpResponse(audio_file, content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename="audio.mp3"'
        return response