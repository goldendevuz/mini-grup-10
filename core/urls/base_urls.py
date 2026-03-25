from django.urls import path
from core.views.auth_views import RegisterView
from core.views.recent_verify import ResentVerifyCodeView


urlpatterns = [
      path('register/', RegisterView.as_view()),
      path("resend-code/", ResentVerifyCodeView.as_view()),
]