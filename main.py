from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from googletrans import Translator

# Loading model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("models")

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