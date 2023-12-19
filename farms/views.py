import json
from .filters import FarmFilters, ParcelFilters
from rest_framework.views import APIView
from .serializers import FarmSerializer, ParcelSerializer
from .models import Farm, Parcel
from seeds.models import Seeds
from rest_framework.response import Response
from rest_framework import status
from .utils import obtener_info_usuario, crear_granja, crear_parcela
import jwt


class CreateFarmView(APIView):
    allowed_methods = ['POST']
    def post(self, request):
        try:
            data = request.data
            token = data.get('token', None)
            user_id = jwt.decode(token, options={"verify_signature": False})['userId']
            farm_name = data.get('farm_name', None)
            farm_latitude = data.get('latitude', None)
            farm_longitude = data.get('longitude', None)

            if not token or not user_id:
                return Response({'Client Error': 'Missing required parameters token or inexistent user'},
                                status=status.HTTP_400_BAD_REQUEST
                                )
            user_data = obtener_info_usuario(token, user_id)
            if 'error' in user_data:
                return Response({'error': str(user_data['error'])}, status= user_data['status_code'])
            if not farm_name or not farm_latitude or not farm_longitude:
                return Response({'Client Error': 'Missing required parameters farm_name, farm_latitude  or farm_longitude'},
                                status=status.HTTP_400_BAD_REQUEST
                                )
            farm = crear_granja(
                int(user_id),
                farm_name,
                float(farm_latitude),
                float(farm_longitude)
                )
            if farm is None:
                return Response({'error': 'The user has reached the limit of farms'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = FarmSerializer(farm)
                serialized_data = serializer.data
                return Response(serialized_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateParcelView(APIView):
    allowed_methods = ['POST']
    def post(self, request):
        try:
            data = request.data
            token = data.get('token', None)
            user_id = jwt.decode(token, options={"verify_signature": False})['userId']
            farm_id = data.get('farm_id', None)
            seed_id = data.get('seed_id', None)
            width = data.get('width', None)
            length = data.get('length', None)
            crop_modality = data.get('crop_modality', None)

            if not token or not user_id:
                return Response({'Client Error': 'Missing required parameters token or inexistent user'},
                                status=status.HTTP_400_BAD_REQUEST
                                )
            user_data = obtener_info_usuario(token, user_id)
            if 'error' in user_data:
                return Response({'error': str(user_data['error'])}, status= user_data['status_code'])
            if farm_id is None or seed_id is None or width is None or length is None or crop_modality is None:
                return Response({'Client Error': 'Missing required parameters in the request body'},
                                status=status.HTTP_400_BAD_REQUEST
                                )
            try:
                farm = Farm.objects.get(id=farm_id)
                seed = Seeds.objects.get(pk=seed_id)
            except Exception as e:
                return Response({'error': str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
            if farm.user_id != int(user_id):
                return Response({'Client Error': 'This farm does not belong to the user'},
                                status=status.HTTP_400_BAD_REQUEST
                                )
            parcel = crear_parcela(
                user_id,
                farm,
                seed,
                float(width),
                float(length),
                crop_modality
            )
            if parcel is None:
                return Response({'error': 'The user has reached the limit of parcels'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = ParcelSerializer(parcel)
                serialized_data = serializer.data
                return Response(serialized_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)


class FarmUpdateAPIView(APIView):
    allowed_methods = ['PUT']
    def put(self, request, pk, format=None):
        try:
            data = request.data
            token = data.get('token', None)
            user_id = jwt.decode(token, options={"verify_signature": False})['userId']
            try:
                farm = Farm.objects.get(id=pk)
            except Farm.DoesNotExist:
                raise Response({'Client Error': 'This farm does not exist'},
                                    status=status.HTTP_400_BAD_REQUEST
                                    )
            if farm.user_id != int(user_id):
                    return Response({'Client Error': 'This farm does not belong to the user'},
                                    status=status.HTTP_400_BAD_REQUEST
                                    )
            user_data = obtener_info_usuario(token, user_id)
            if 'error' in user_data:
                    return Response({'error': str(user_data['error'])}, status= user_data['status_code'])
            
            data.pop('token', None)
            farm = farm.update_farm(data)
            serializer = FarmSerializer(farm)
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)

class ParcelUpdateAPIView(APIView):
    allowed_methods = ['PUT']
    def put(self, request, pk, format=None):
        try:
            data = request.data
            token = data.get('token', None)
            user_id = jwt.decode(token, options={"verify_signature": False})['userId']
            try:
                parcel = Parcel.objects.get(id=pk)
            except Parcel.DoesNotExist:
                raise Response({'Client Error': 'This parcel does not exist'},
                                    status=status.HTTP_400_BAD_REQUEST
                                    )
            if parcel.farm.user_id != int(user_id):
                    return Response({'Client Error': 'This parcel does not belong to the user'},
                                    status=status.HTTP_400_BAD_REQUEST
                                    )
            user_data = obtener_info_usuario(token, user_id)
            if 'error' in user_data:
                    return Response({'error': str(user_data['error'])}, status= user_data['status_code'])
            
            data.pop('token', None)
            parcel = parcel.update_parcel(data)
            serializer = ParcelSerializer(parcel)
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)

class FarmListAPIView(APIView):
    allowed_methods = ['GET']
    filterset_class = FarmFilters
    serializer_class = FarmSerializer
    queryset = Farm.objects.all()

    def get(self, request):
        try:
            data = request.headers
            token = data.get('Authorization', None).split(' ')[1] if ' ' in token else None
            user_id = jwt.decode(token, options={"verify_signature": False})['userId']
            if not token or not user_id:
                return Response({'Client Error': 'Missing required parameters token or inexistent user'},
                                status=status.HTTP_400_BAD_REQUEST
                                )
            user_data = obtener_info_usuario(token, user_id)
            if 'error' in user_data:
                return Response({'error': str(user_data['error'])}, status= user_data['status_code'])
            queryset = self.queryset.filter(user_id=user_id)
            queryset = self.filterset_class(request.GET, queryset=self.queryset).qs
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ParcelListAPIView(APIView):
    allowed_methods = ['GET']
    filterset_class = ParcelFilters
    serializer_class = ParcelSerializer
    queryset = Parcel.objects.all()

    def get(self, request):
        try:
            data = request.headers
            token = data.get('Authorization', None).split(' ')[1] if ' ' in token else None
            user_id = jwt.decode(token, options={"verify_signature": False})['userId']
            if not token or not user_id:
                return Response({'Client Error': 'Missing required parameters token or inexistent user'},
                                status=status.HTTP_400_BAD_REQUEST
                                )
            user_data = obtener_info_usuario(token, user_id)
            if 'error' in user_data:
                return Response({'error': str(user_data['error'])}, status= user_data['status_code'])
            queryset = self.filterset_class(request.GET, queryset=self.queryset).qs
            print(queryset)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
