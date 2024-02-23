import os
import uuid
from PIL import Image
from django.http import HttpResponse
from rest_framework.views import APIView
from .tasks import return_text_from_image, generate_audio

class ImageAPIView(APIView):
    def post(self, request):
        uploaded_image = request.data.get('image')
        image = Image.open(uploaded_image)
        image.save(os.path.join("images", f"{uuid.uuid4()}.png"))
        text_ = return_text_from_image(image)
        audio_data = generate_audio(text_)

        # Directly return audio data as response
        response = HttpResponse(audio_data, content_type='audio/mpeg')
        response['Content-Disposition'] = 'attachment; filename="audio.mp3"'
        return response