from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.text_processing import clean_text, analyze_text_with_parsbert

@api_view(['POST'])
def analyze_text(request):
    text = request.data.get('text')
    cleaned_text = clean_text(text)
    result = analyze_text_with_parsbert(cleaned_text)
    return Response({"analysis_result": result})
