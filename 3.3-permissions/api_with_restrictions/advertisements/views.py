from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from rest_framework.exceptions import ValidationError

from logistic.permissions import IsOwner, IsAdmin, IsOwnerOrAdmin


class AdvertisementViewSet(ModelViewSet, ):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_class = AdvertisementFilter

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    # def perform_update(self, serializer):
    #     if self.get_object().creator != self.request.user:
    #         raise ValidationError('Access denied: wrong owner token')
    #     serializer.save(creator=self.request.user)
    #
    # def perform_destroy(self, instance):
    #     if self.request.user != instance.creator:
    #         raise ValidationError('Access denied: wrong owner token')
    #     else:
    #         instance.delete()

    def get_permissions(self):
        """Получение прав для действий."""

        if self.action in ["create"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrAdmin()]
        else:
            return []


