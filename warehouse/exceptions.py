from django.http.response import Http404
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler

from utils.translate_response import translate_text


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, ValidationError):
            if len(response.data) == 1 and 'detail' in response.data:
                errors = response.data['detail']
                if isinstance(errors, list) and len(errors) == 1:
                    response.data = {'detail': translate_text(errors[0])}
                else:
                    response.data = {'detail': translate_text(' '.join(errors))}

        elif isinstance(exc, Http404):
            print(context)
            view = context.get('view', None)
            model_verbose_name = "Объект"
            if view and hasattr(view, 'get_serializer_class'):
                serializer_class = view.get_serializer_class()
                if hasattr(serializer_class, 'Meta') and hasattr(serializer_class.Meta, 'model'):
                    model = serializer_class.Meta.model
                    model_verbose_name = model._meta.verbose_name.capitalize()

            response.data = {
                "detail": f"{model_verbose_name} не найден"
            }

        if response.status_code == 500:
            response.data = {
                "detail": f"Ошибка сервера 500"
            }

    return response
