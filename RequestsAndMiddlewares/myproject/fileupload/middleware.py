import time
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

REQUEST_LIMIT = 5  # Максимальное количество запросов
TIME_PERIOD = 60  # Период времени в секундах

class ThrottlingMiddleware(MiddlewareMixin):
    user_requests = {}

    def process_request(self, request):
        ip = request.META.get('REMOTE_ADDR')
        current_time = time.time()

        if ip not in self.user_requests:
            self.user_requests[ip] = []

        # Удаляем старые запросы
        self.user_requests[ip] = [timestamp for timestamp in self.user_requests[ip] if current_time - timestamp < TIME_PERIOD]

        if len(self.user_requests[ip]) >= REQUEST_LIMIT:
            return JsonResponse({'error': 'Too many requests. Please try again later.'}, status=429)

        # Записываем текущий запрос
        self.user_requests[ip].append(current_time)