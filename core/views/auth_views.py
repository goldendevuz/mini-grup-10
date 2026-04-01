import random
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models.auth_models import User
from rest_framework.exceptions import AuthenticationFailed
from core.models.auth_models import VerifivationCode
from rest_framework.permissions import IsAuthenticated


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        fullname = request.data.get("fullname", None)
        username = request.data.get("username", None)
        email = request.data.get("email", None)
        age = request.data.get('age', None)
        gender = request.data.get("gender", None)
        role = request.data.get("role", None)
        password = request.data.get("password", None)

        if None in [fullname, username, age, gender, role, password]:
            return Response({
                "error": "kerakli, polyalar to'lliq emas"
            }, status=403)

        user = User.objects.filter(username=username).first()

        if user:
            raise AuthenticationFailed("user already exist")

        if 3 > len(password):
            return Response({
                "message": "parol judayam kichkina"
            })

        elif len(password) >= 14:
            return Response({
                "message": "parol judayam katta"
            })

        kerak = {
            "son": 0,
            "harf": 0
        }

        for i in password:
            if i.isdigit():
                kerak['son'] +=1
            if i.isalpha():
                kerak['harf'] +=1

        if 0 in [kerak['son'], kerak['harf']]:
            return Response({
                "message": "parolda harf bilan son qatnalishi shart"
            })

        clear_data = {
            "fullname": fullname,
            "username": username,
            "email": email,
            "age": age,
            "gender": gender,
            "role": role,
            "password": password
        }
        user = User.objects.create_user(**clear_data)

        user.is_active = False
        user.save()

        code = str(random.randint(100000, 999999))

        VerifivationCode.objects.create(user=user, code=code)

        try:
            user.is_active = True
            send_mail(
                subject="tasdiqlash kodi:",
                message=f'assalomu aleykum, {fullname},\n sizning tasdiqlash kodi: - {code}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False
            )
        except Exception as e:
            user.delete()
            return Response({
                "error": f"emailga yuborilvotkanida hatolik yuz berdi\n {str(e)} "
            }, status=500)

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Muvaffaqiyatli ro'yxatdan o'tdingiz. Emailingizga 6 xonali tasdiqlash kodi yuborildi!",
            "user": user.response(),
            "access_token": token.key
        }, status=201)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            raise AuthenticationFailed("email va password kirlishi shart")

        user = User.objects.filter(email=email).first()
        if not user:
            raise AuthenticationFailed("email topilmadi")

        if not user.is_active:
            return Response({
                "error": "user is baned"
            }, status=401)

        if not user.check_password(str(password)):
            raise AuthenticationFailed("password noto'g'ri")

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "email": user.email,
            "message": "successfull you are login",
            "token": token.key,
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated] # Только авторизованные

    def post(self, request):
        try:
            # Удаляем токен текущего пользователя
            request.user.auth_token.delete()
        except:
            pass
        return Response({
            "message": "successfully logout"
        }, status=200)







