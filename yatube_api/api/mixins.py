from rest_framework import mixins, viewsets


class CreateOrGetListMixin(mixins.CreateModelMixin, mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    pass
