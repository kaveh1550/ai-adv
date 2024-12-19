from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.voice_processing import convert_audio_to_text, text_to_speech

@api_view(['POST'])
def audio_to_text(request):
    audio_file = request.FILES['audio']
    file_path = f'/uploads/{audio_file.name}'
    with open(file_path, 'wb+') as destination:
        for chunk in audio_file.chunks():
            destination.write(chunk)
    converted_text = convert_audio_to_text(file_path)
    return Response({"converted_text": converted_text})

@api_view(['POST'])
def text_to_audio(request):
    text = request.data.get('text')
    text_to_speech(text)
    return Response({"status": "Audio generated successfully"})
