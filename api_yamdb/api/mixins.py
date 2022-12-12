from rest_framework import mixins, viewsets


class ModelMixinSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pass
