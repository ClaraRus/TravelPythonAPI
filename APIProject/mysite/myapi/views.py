# Create your views here.
import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from requests import Response
from rest_framework import viewsets, status
from rest_framework.decorators import api_view

from .TextMining.ActivitiesNER import get_activities, get_final_result
from .TextMining.ExtractTags import get_tags
from .TextMining.ParagraphExtraction import extract_paragraph
from .models import Tags, Activities, FinalResult, Paragraphs
from .serializers import TagsSerializer


# def get_queryset(self):
#   text = self.request.query_params.get('text')
#  text = get_tags(text)

# queryset = text

# return queryset

# class TagsViewSet(viewsets.ModelViewSet):
#   queryset = Tags.objects.all()
#  serializer_class = TagsSerializer

# def get_Tags(request, text=""):
#    response_text = get_tags(text)
#   return HttpResponse(response_text)

# def get_object(self):
#   queryset = self.filter_queryset(self.get_queryset())

@csrf_exempt
def gettags(request):
    model = Tags
    try:
        #print("The input:")
        #text = request.GET['text']
        #print(text)
        text = str(request.body).split("\"")[3]
        tags = get_tags(text)
        #print("The output:")
        #print(tags)
        #print("Json:")
        #print(JsonResponse(tags, safe=False).getvalue())
        return JsonResponse(tags, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def getactivities(request):
    model = Activities
    try:
        #print("The input:")
        #print(request.body)
        text = str(request.body).split("\"")[3]
        destination=str(request.body).split("\"")[7]
        #text = request.POST.get('text')
        #print(text)
        #text = received_json_data['text']
        #print(text)
        result = get_activities(text, destination)
        #print("The output:")
        #print(result)
        #print("Json:")
        #print(JsonResponse(result, safe=False).getvalue())
        return JsonResponse(result, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def getfinalresult(request):
    model = FinalResult
    try:
        #print("The input:")
        #print(request.body)
        result = str(request.body)
        #print(result)
        result = get_final_result(result)
        #print("The output:")
        #print(result)
        #print("Json:")
        #print(JsonResponse(result, safe=False).getvalue())
        return JsonResponse(result, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def getparagraphs(request):
    model = Paragraphs
    try:
        #print("The input:")
        #print(request.body)
        text = str(request.body).split("\"")[3]
        location = str(request.body).split("\"")[7]
        #text = request.POST.get('text')
        #print(text)
        #text = received_json_data['text']
        #print(text)
        result = extract_paragraph(text, location)
        #print("The output:")
        #print(result)
        #print("Json:")
        #print(JsonResponse(result, safe=False).getvalue())
        return JsonResponse(result, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

#class TagsViewSet(viewsets.ModelViewSet):
 #   def get_context_data(self, **kwargs):
  #      return JsonResponse(get_tags(kwargs['text']))



