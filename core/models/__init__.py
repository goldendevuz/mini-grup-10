# Импортируем все модели, чтобы Django "увидел" их при создании миграций
from .models import *
from .auth_models import *