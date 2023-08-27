from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth import get_user_model
from .emails import *

User = get_user_model()


class RegisterUser(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                send_otp_via_email(serializer.data['email'])
                return Response({
                    'status':200,
                    'message': 'User succesfully registered'
                })
            
            return Response({
                'status':400,
                'message': serializer.errors
            })
        
        except Exception as e:
            print(e)

    def get(self, request):
        user_obj = CustomUser.objects.all()
        print(user_obj)
        serializer = UserSerializer(user_obj, many=True)
        return Response({'status':200, 'payload':serializer.data})


class VerifyOTP(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = VerifyOTPSerializer(data = data)

            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                user = CustomUser.objects.filter(email = email)
                if not user.exists():
                    return Response({
                        'status': 400,
                        'message': 'something went wrong',
                        'data': 'Invalid email' 
                    })

                if user[0].otp != otp:
                    return Response({
                        'status': 400,
                        'message': 'something went wrong',
                        'data': 'wrong otp' 
                    })
                
                user = user.first()
                user.is_verified = True
                user.save()
                return Response({
                        'status': 200,
                        'message': 'account verified',
                        'data': {} 
                    })

            return Response({
                        'status': 400,
                        'message': 'something went wrong',
                        'data': serializer.errors 
                    })

        except Exception as e:
            print(e)
