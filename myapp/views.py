from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from myapp.models import MyUser
from myapp.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, SendPasswordResetMailSerializer, UserResetPasswordSerializer

from django.contrib.auth import authenticate
from myapp.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


# <-------------------------        Generate Token Manaually        ----------------->

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# <-----------------------------     User Registration API       ------------------------------>


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            # print("User is:", user)
            return Response({'msg':"Registration successfull","token":token, "status":status.HTTP_201_CREATED})
        else:
            return Response({"msg":serializer.errors, "status":status.HTTP_400_BAD_REQUEST})
        

# <----------------------------             User Login API                 --------------------------->

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            print("User is:", user)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'msg':"Login successfull", "token":token, "status":status.HTTP_200_OK})
            else:
                return Response({"msg":"Invalid Credentials", "status":status.HTTP_404_NOT_FOUND})
        else:            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# <------------------------------           User Profile View           -----------------------> 
        
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user) 
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
# <-------------------------------  User change Password    ------------------------------>

class UserchangePassword(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Successfully Updated', 'status':status.HTTP_200_OK})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# <----------------------------             Send Password Email             --------------------------->

class SendPasswordResetMailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetMailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Link Sent to Your Email', 'status':status.HTTP_200_OK})
        else:   
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    
# <------------------               User Password Reset view         ---------------------------->

class UserResetPasswordView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserResetPasswordSerializer(data=request.data, context={'uid':uid, 'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':"Password Reset Successfully", 'status':status.HTTP_200_OK})
        else:
            return Response({'msg':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})
        
# <--------------------------------               Code END                -- ------------------------>