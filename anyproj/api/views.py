from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.views import APIView

from api.serializers import UsersSerializer, UserLoginSerializer
from rest_framework import status
from referral.models import User
from rest_framework.authtoken.models import Token

from django.shortcuts import get_object_or_404

from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication

from referral.tasks import send_auth_code





@api_view(['POST'])
def send_me_code(request):
    try:
        phone_number = request.data['phone_number']
        user = get_object_or_404(User, phone_number=phone_number)
        serializer = UserLoginSerializer(instance=user)
        send_auth_code.delay(user.id)
        return Response({'response': 'CODE SENDED','user': serializer.data})
    except:
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            user = User.objects.create_user(phone_number=phone_number)
            send_auth_code.delay(user.id)
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


class UserProfileAPIVIew(RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        invited = User.objects.filter(inviter=user)
        content = {
            'user': str(user),
            'referral_code': user.referral_code,
            'invite_code': 'Инвайт код введен' if user.inviter is not None else 'Инвайт код не введен',
            'invited_users': [_.phone_number for _ in invited]
        }
        return Response(content)
    

class EnterInviteAPIVIew(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            referral_code = request.data['referral_code']
            invite_code_owner = User.objects.get(referral_code=referral_code)
            if user.inviter is None:
                if invite_code_owner is not user:
                    user.inviter = invite_code_owner
                    user.save()
                    return Response({'response': 'SUCCES'})
                else:
                    raise AuthenticationFailed('Invalid referral_code')
            else:
                raise ValueError('Инвай код уже введен')
        except KeyError as e:
            return Response(status=400, data={'error': f'Missing required field: {e.args[0]}'})
        except Exception as e:
            return Response(status=500, data={'error': str(e)})


class UserProfilesAPIVIew(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UsersSerializer
    queryset = User.objects.all()






