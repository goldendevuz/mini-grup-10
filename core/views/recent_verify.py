import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from core.models.auth_models import User, VerifivationCode

class ResentVerifyCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', None)
        if not email:
            raise AuthenticationFailed("email kiritilishi shart")

        block_obj = f"block_{email}"
        if cache.get(block_obj):
            return Response({
                "error": "siz 10 minutda bloklangiz. Iltimos kuting."
            }, status=429)

        attempt_key = f"attempts_{email}"
        attempts = cache.get(attempt_key, 0)

        if attempts >= 3:
            cache.set(block_obj, True, timeout=600)

            cache.delete(attempt_key)
            return Response({
                "error": "siz juda ko'p urindingiz! Siz 10 daqiqaga bloklandingiz"
            }, status=429)

        if attempts == 0:

            cache.set(attempt_key, 1, timeout=1800)

        else:

            cache.set(attempt_key, attempts + 1, timeout=1800)

        user = User.objects.filter(email=email).first()

        if not user:
            raise AuthenticationFailed("foydalanuvchi yo'q kuuuuu")

        if user.is_active:
            return Response({
                "message": "Allaqachon tasdiqlandi"
            }, status=400)

        new_token = str(uuid.uuid4())
        VerifivationCode.objects.update_or_create(
            user=user,
            defaults={"code": new_token, "created_at": timezone.now()}
        )
        # 5. Отправляем письмо
        verify_link = f"{getattr(settings, 'FRONTEND_URL', 'http://127.0.0.1:8000')}/api/verify/{new_token}/"
        try:
            send_mail(
                subject="Hisobni tasdiqlash",
                message=f"Tasdiqlash uchun bosing: {verify_link}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
            )
        except Exception as e:
            return Response({"error": "Email yuborishda xatolik"}, status=500)

        # 6. Определяем почтовик для удобного редиректа на фронтенде
        domain = email.split('@')[-1]
        mail_links = {
            'gmail.com': 'https://mail.google.com',
            'mail.ru': 'https://e.mail.ru',
            'yandex.ru': 'https://mail.yandex.ru',
            'yandex.uz': 'https://mail.yandex.uz',
            'yahoo.com': 'https://mail.yahoo.com',
        }
        redirect_url = mail_links.get(domain, f"https://{domain}")

        return Response({
            "message": "Havola yuborildi",
            "redirect_to": redirect_url
        })
