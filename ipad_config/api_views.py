# Django Imports
from django.http import JsonResponse

# Restframework Imports
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework import status

# Project Imports
from .models import Hotel, JavaConfig, FQDN
from .serializers import JavaConfigSerializer


class JavaConfigList(ListAPIView):
    serializer_class = JavaConfigSerializer

    def get_queryset(self):
        hotel_code = self.kwargs['hotel_code']
        related_hotel = Hotel.objects.get(hotel_code=hotel_code)
        return JavaConfig.objects.filter(related_hotel=related_hotel, is_synced=False)


@api_view(['GET'])
def ack_java_configs_sync(request, hotel_code):
    hotel = Hotel.objects.get(hotel_code=hotel_code)
    for config in hotel.java_configs.filter(is_synced=False):
        config.is_synced = True
        config.save()
    return JsonResponse({"User": str(request.user)}, status=200)


class SyncFqdn(ListAPIView):

    def get(self, request, *args, **kwargs):

        try:
            hotel = Hotel.objects.get(hotel_code=kwargs["hotel_code"])
            fqdns = FQDN.objects.filter(hotel=hotel).values_list('server', 'fqdn')
            if fqdns:
                fqdns = {data[0]: data[1] for data in fqdns}
                return JsonResponse({"data": fqdns}, status=status.HTTP_200_OK)
            return JsonResponse({
                "data": "No fqdns in digivalet-setup"
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return JsonResponse({
                "data": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
