from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import userserializer, VerifyAccountSerialzer
from . emails import send_otp_via_email
from . models import user

# Create your views here.

class RegisterEmail(APIView):
    def post(self, request):
        try:
            query = request.data
            serializer = userserializer(data=query)
            if serializer.is_valid():
                serializer.save()
                send_otp_via_email(serializer.data['email'])
                return Response({
                    'status': status.HTTP_200_OK,
                    'message': 'User registered successfully.',
                    'data': serializer.data,
                })
            
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Validation Error.',
                'errors': serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Internal Server Error.'
            })
        

class VerifyOtp(APIView):
    def post(self, request):
            
        
            data = request.data
            serializer = VerifyAccountSerialzer(data = data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                User = user.objects.filter(email = email)
                if not User.exists():
                    return Response({
                        'status': 400,
                        'message': 'Something Thappu',
                        'data': 'invalid data'
                    })
                if User[0].otp != otp:
                    return Response({
                        'status': 400,
                        'message': 'Something Thappu',
                        'data': 'invalid Otp'

                    })
                
                User[0].is_verified = True
                User[0].save()

                return Response({
                'status': 200,
                'message': 'Verified Succesfull',
                'errors': serializer.data
            })


