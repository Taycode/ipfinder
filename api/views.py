from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from api.serializers import IPAddressSerializer, IPAddressGetSerializer
from api.models import IPAddress

ACCESS_KEY = '0a2d26de06ac50376c6e9508e00ffbe5'


# Function for accessing IPStack

def ip_find(address):
    import requests
    url = 'http://api.ipstack.com/{}'.format(address)
    print(url)
    params = {"access_key": ACCESS_KEY}
    response = requests.get(url, params=params)
    return response.json()


@api_view(['GET'])
def index(request):

    if request.method == 'GET':

        # serializer for getting IP address
        serializer = IPAddressGetSerializer(data=request.data)

        if serializer.is_valid():

            address = serializer.data['address']

            # get ip address data from cache

            data = cache.get(address)

            if data:

                # pass data into serializer so we can return as JSON

                serialized_data = IPAddressSerializer(data=data)

                if serialized_data.is_valid():

                    return Response(serialized_data.data, status=status.HTTP_200_OK)

            else:

                try:

                    ip = IPAddress.objects.get(address=address)

                except IPAddress.DoesNotExist:

                    ip = None

                if ip is not None:

                    serialized_data = IPAddressSerializer(ip)
                    cache.set(address, serialized_data.data, 60)
                    return Response(serialized_data.data, status=status.HTTP_200_OK)

                else:

                    response = ip_find(address)

                    data = {
                        "address": response['ip'],
                        "continent": response['continent_name'],
                        "country": response['country_name'],
                        "state": response['region_name'],
                        "latitude": response['latitude'],
                        "longitude": response['longitude']
                    }

                    serialized_data = IPAddressSerializer(data=data)

                    if serialized_data.is_valid():

                        serialized_data.save()
                        cache.set(address, serialized_data.data, 60)
                        return Response(serialized_data.data, status=status.HTTP_200_OK)

                    else:

                        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
