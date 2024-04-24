from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response


from api.serializers import UsersSerializer, UserLoginSerializer
from rest_framework import status
from referral.models import User, AuthCodeModel
from rest_framework.authtoken.models import Token

from django.shortcuts import get_object_or_404

from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


def send_code(user):
    try:
        new_write = AuthCodeModel.objects.create(user=user, code='123456')
        new_write.save()
    except:
        pass

@api_view(['POST'])
def send_me_code(request):
    try:
        phone_number = request.data['phone_number']
        user = get_object_or_404(User, phone_number=phone_number)
        serializer = UserLoginSerializer(instance=user)
        send_code(user)
        return Response({'response': 'CODE SENDED','user': serializer.data})
    except:
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            user = User.objects.create_user(phone_number=phone_number)
            send_code(user)
            return Response({'response': 'CODE SENDED','user': serializer.data})
    
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def auth(request):
    try:
        phone_number = request.data['phone_number']
        auth_code = request.data['auth_code']
        user = authenticate(phone_number=phone_number, auth_code=auth_code)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'response': 'SUCCES', 'token': str(token)})
        else:
            raise AuthenticationFailed('Invalid auth_code or phone_number')
    except KeyError as e:
        return Response(status=400, data={'error': f'Missing required field: {e.args[0]}'})
    except Exception as e:
        return Response(status=500, data={'error': str(e)})


























class UsersListAPIVIew(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer








