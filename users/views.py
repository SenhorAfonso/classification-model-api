from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_http_methods
from users.user_service import UserService


class UserController(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.userService = UserService()

    def get(self, request):
        users = self.userService.getAllUsers()
        return JsonResponse({'users': users})
