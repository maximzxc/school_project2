from rest_framework.routers import DefaultRouter
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin
)

from core.models import (
    User,
    Note,
)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note


class UserViewSet(
        ListModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        DestroyModelMixin,
        CreateModelMixin,
        GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = ["email", ]

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('pk') == 'current':
            kwargs['pk'] = request.user.pk

        return super(UserViewSet, self).dispatch(request, *args, **kwargs)


class NoteViewSet(
        ListModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        DestroyModelMixin,
        CreateModelMixin,
        GenericViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    filter_fields = ["sender", "text", ]


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'notes', NoteViewSet)
