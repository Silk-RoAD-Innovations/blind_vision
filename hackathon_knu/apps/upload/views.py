from PIL import Image
from django.http import HttpResponse
# from django.core.cache import cache
from rest_framework.views import APIView
from .tasks import return_text_from_image, generate_audio

class ImageAPIView(APIView):
    def post(self, request):
        uploaded_image = request.data.get('image')
        image = Image.open(uploaded_image)
        image.show()

        # Check if the result is in cache
        # cache_key = f"image_text:{uploaded_image}"
        # text_ = cache.get(cache_key)

        # if text_ is None:
        text_ = return_text_from_image(image)
            # Cache the result for future use
            # cache.set(cache_key, text_, timeout=None)

        audio_data = generate_audio(text_)

        # Directly return audio data as response
        response = HttpResponse(audio_data, content_type='audio/mpeg')
        response['Content-Disposition'] = 'attachment; filename="audio.mp3"'
        return response