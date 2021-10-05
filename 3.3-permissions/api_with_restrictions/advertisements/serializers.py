from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""
    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        if data.get('status') == AdvertisementStatusChoices.CLOSED:
            return data
        else:
            adv_count = Advertisement.objects.filter(creator=self.context['request'].user.id,
                                                     status=AdvertisementStatusChoices.OPEN).count()
            if adv_count >= 1:
                raise ValidationError('Maximal active advertisements count reached.')
            return data
