from django.utils import translation


class ForceAdminRussianMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        translation.activate('ru')
        request.LANGUAGE_CODE = 'ru'

        response = self.get_response(request)
        translation.deactivate()
        return response
