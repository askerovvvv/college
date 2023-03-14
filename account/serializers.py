from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import serializers

User = get_user_model()

class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer checks email if email in database it will send activation code to change password
    """
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Account not found!')
        return email

    def send_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        user.save()
        send_mail(
            'Password recovery College',
            f'Confirmation code:{user.activation_code}',
            'bekbol.2019@gmail.com',
            [email]
        )


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    """
    Serializer checks email if email in database it will check password1 and password2 if it is True Serializer change
    password
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True, min_length=6)
    activation_code = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Account not found!')
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        code = attrs.get('activation_code')
        email = attrs.get('email')

        if password != password2:
            raise serializers.ValidationError('Passwords do not match!')

        if not User.objects.filter(activation_code=code, email=email).exists():
            raise serializers.ValidationError('Invalid activation code!')
        return attrs

    def create_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ''
        user.save()

