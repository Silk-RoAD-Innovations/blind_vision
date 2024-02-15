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


# Loading model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("models")
url = "https://tts.ulut.kg/api/tts"

def return_text_from_image(raw_image: Image):
    # unconditional image captioning
    inputs = processor(raw_image, return_tensors="pt")
    out = model.generate(**inputs)
    image_description = processor.decode(out[0], skip_special_tokens=True)
    def translate_to_kyrgyz(text):
        translator = Translator()
        translated_text = translator.translate(text, dest='kyrgyz').text
        return translated_text

    return translate_to_kyrgyz(image_description)

def download_audio(text_):
    payload = json.dumps({
    "text": text_,
    "speaker_id": 1
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer itS2UoaWjrEcIwmToywRykwLVvdmJFLBZKBzcLTV3FIqCmbiiRvHKZ8c04zQx350'
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
        image = Image.open("sample1.jpg")
        text_ = return_text_from_image(image)
        download_audio(text_)
        with open('audio_file.mp3', 'rb') as audio_file:
            response = HttpResponse(audio_file, content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename="audio.mp3"'
        return response