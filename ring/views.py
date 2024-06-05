from django.shortcuts import render, get_object_or_404
from .serializers import UserSerializer, CompanySerializer, AssitantSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .models import Assistant
from .permissions import IsOwner
from .utils.gpt import get_ai_response
from .utils.yandex import yandex_stt, yandex_tts
import io
from django.http import FileResponse


class RegisterLoginView(APIView):

    def post(self, request, *args, **kwargs):

        user = UserSerializer(data=request.data, context={"request": request})

        if user.is_valid(raise_exception=True):

            user = user.save()
            token = Token.objects.create(user=user)

            data = UserSerializer(user).data

            data["token"] = token.key

            return Response(data=data, status=status.HTTP_201_CREATED)


class Login(APIView):

    def post(self, request, *args, **kwargs):

        username = request.data.get("username", None)
        password = request.data.get("password", None)

        if not username or not password:
            return Response(data={"error": "you should provide both username and password"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if not user:

            return Response(data={"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


        token, created = Token.objects.get_or_create(user=user)

        return Response(data={"token": token.key}, status=status.HTTP_202_ACCEPTED)



class RetrieveToken(APIView):
    def post(self, request, *args, **kwargs):

        username = request.data.get("username", None)
        password = request.data.get("password", None)

        if not username or not password:
            return Response(data={"error": "you should provide both username and password"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if not user:

            return Response(data={"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

        if Token.objects.filter(user=user).exists():
            Token.objects.get(user=user).delete()

        token = Token.objects.create(user=user)

        return Response(data={"token": token.key}, status=status.HTTP_202_ACCEPTED)

class AssitantView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self, name):
        obj = get_object_or_404(Assistant, name=name)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        name = kwargs.pop("name", None)
        if name:
            object = self.get_object(name)
            return Response(AssitantSerializer(object).data, status=status.HTTP_200_OK)

        queryset = Assistant.objects.filter(company_id=request.user.company.pk)
        return Response(AssitantSerializer(queryset, many=True).data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['company_id'] = request.user.company.pk
        assistant = AssitantSerializer(data=data)
        if assistant.is_valid(raise_exception=True):
            assistant = assistant.save()
            return Response(AssitantSerializer(assistant).data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        assistant_id = kwargs.get('pk')

        assistant = self.get_object(assistant_id)
        serializer = AssitantSerializer(assistant, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        assistant_id = kwargs.get('pk')
        assistant = self.get_object(assistant_id)
        assistant.delete()
        return Response(data={"success": "The instance successfully deleted"}, status=status.HTTP_204_NO_CONTENT)




class TextView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    def get_object(self, name):
        obj = get_object_or_404(Assistant, name=name)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get(self, request):
        data = request.data
        name = data.get("assistant")
        request_message = data.get("request")
        print(name)
        if not Assistant.objects.filter(name=name).exists():
            return Response(data={
            "response": "Assitant name error"
        }, status=status.HTTP_404_NOT_FOUND)
        
        assistant = self.get_object(name=name)
        
        
        response = get_ai_response(user_message=request_message, content=assistant.content)
        
        return Response(data={
            "response": response
        }, status=status.HTTP_200_OK)

class VoiceView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    def get_object(self, name):
        obj = get_object_or_404(Assistant, name=name)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def post(self, request, **kwargs):
        audio_bytes = request.body
        
        name = kwargs.get("assistant")
        
        if not Assistant.objects.filter(name=name).exists():
            return Response(data={
            "response": "Assitant name error"
        }, status=status.HTTP_404_NOT_FOUND)
        
        assistant = self.get_object(name=name)
        
        
        
        
        text = yandex_stt(audio_bytes)
        
        
        text = get_ai_response(content=assistant.content, user_message=text)
        
        
        
        audio = yandex_tts(text)
        
        
        audio_stream = io.BytesIO(audio)
        audio_stream.seek(0)

        return FileResponse(audio_stream, content_type='audio/mpeg', as_attachment=True, filename="response.mp3")

        
    