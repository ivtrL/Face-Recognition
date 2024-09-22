from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
import urllib.request
import face_recognition

class faceRecognition(APIView):
    def post(self, request):
        try:
            users = User.objects.all()
            knownFacesEncodingList = []
            for user in users:
                knownFacesImage = face_recognition.load_image_file(urllib.request.urlopen(user.imageurl))
                knownFacesEncodingList.append(face_recognition.face_encodings(knownFacesImage)[0])

            unknownFaceImageUrl = request.data['imageUrl']
            unknownFaceImage = face_recognition.load_image_file(urllib.request.urlopen(unknownFaceImageUrl))
            unknownFaceEncodings = face_recognition.face_encodings(unknownFaceImage)

            if len(unknownFaceEncodings) > 0:
                unknownFaceEncoding = unknownFaceEncodings[0]
            else:
                return Response({"status": True, "message": "No face Detected", "data": 0})

            results = face_recognition.compare_faces(knownFacesEncodingList, unknownFaceEncoding)
            print(results)
            if results[0] == False:
                return Response({"status": True, "message": "Face Not Recognized", "data": 1})

            return Response({"status": True, "message": "Face Recognized", "data": 2})
        
        except Exception as e:
            return Response({"status": False, "message": str(e)})