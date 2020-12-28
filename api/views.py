from django.shortcuts import render
from rest_framework import filters, mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from recipes.models import Ingredient
from .models import Subscription
from .serializers import IngredientSerializer, SubscriptionSerializer


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    
    def perofrm_destroy(self, instance):
        return instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        success = self.perofrm_destroy(instance)
        return Response({'success': bool(success)}, status=status.HTTP_200_OK)


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^title',)


class SubscriptionViewSet(CreateDestroyViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'author'
