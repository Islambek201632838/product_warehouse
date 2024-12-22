from rest_framework import serializers

from store.models import City, WareHouse
from users.models import CustomUser


class CustomDefaultSerializer(serializers.ModelSerializer):
    @property
    def errors(self):
        ret = super().errors
        if ret:
            formatted_errors = []
            for field_name, error_messages in ret.items():
                field = self.fields.get(field_name)
                verbose_name = field.label if field else field_name

                if isinstance(error_messages, list):
                    if verbose_name in ['detail', 'non_field_errors']:
                        formatted_errors.extend([f"{str(msg)}" for msg in error_messages])
                    else:
                        formatted_errors.extend([f"{verbose_name}: {str(msg)}" for msg in error_messages])

                elif isinstance(error_messages, dict):
                    for key, value in error_messages.values():
                        if key in ['detail', 'non_field_errors']:
                            formatted_errors.append(str(value))
                        else:
                            formatted_errors.append(f"{key}: {str(value)}")

                else:
                    error_messages = str(error_messages)
                    if 'detail' in error_messages:
                        error_messages = error_messages.replace('detail: ', '')
                    elif 'non_field_errors' in error_messages:
                        error_messages = error_messages.replace('non_field_errors: ', '')
                    if '\n' in error_messages:
                        error_messages = error_messages.replace('\n', '')

                    formatted_errors.append(f"{verbose_name}: {str(error_messages)}")

            return {
                "detail": "Ошибка валидации",
                "errors": formatted_errors
            }

        return ret


class UserRegistrationSerializer(CustomDefaultSerializer):
    password = serializers.CharField(write_only=True, required=True, label="Пароль")
    re_password = serializers.CharField(write_only=True, required=True, label="Повтор пароля")

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 're_password', 'email', 'first_name', 'last_name', 'role']

    def validate(self, data):
        if data['password'] != data['re_password']:
            raise serializers.ValidationError("Пароли не совпадают.")
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role']
        )
        user.save()
        return user
