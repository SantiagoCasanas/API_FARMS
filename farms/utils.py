from typing import Dict, Any
import json
from rest_framework import status
import requests
from .models import Farm, Parcel

URL_API_CRUD = "https://weedweb-crud.onrender.com/users/api/"
URL_API_FREEMIUN = "http://localhost:9000/freemiun/"

def obtener_info_usuario(access_token, user_id)-> Dict[str, Any]:
    """
    Función para consultar en la API del CRUD si existe un usuario en especifico
    Y así obtener su información.
    Params:
    -Token
    -Id
    Return:
    -JSON con la info del usuario
    """
    headers = {
    'token': access_token,
    'Authorization': f'Bearer {access_token}',
    }

    try:
        response = requests.get(URL_API_CRUD+str(user_id), headers=headers)
        response.raise_for_status()
        data = response.json()
        return {'data': data, 'status_code': response.status_code}

    except requests.exceptions.HTTPError as err:
        return {'error': err, 'status_code': response.status_code}
    except json.JSONDecodeError as err:
        return {'error': err, 'status_code': response.status_code}
    except Exception as err:
        return {'error': err, 'status_code': response.status_code}

def obtener_info_sub(user_id)-> Dict[str, Any]:
    extra_url = f'current-subscription/{user_id}/'

    try:
        response = requests.get(URL_API_FREEMIUN+extra_url)
        response.raise_for_status()
        data = response.json()
        return {'data': data, 'status_code': response.status_code}

    except requests.exceptions.HTTPError as err:
        return {'error': err, 'status_code': response.status_code}
    except json.JSONDecodeError as err:
        return {'error': err, 'status_code': response.status_code}
    except Exception as err:
        return {'error': err, 'status_code': response.status_code}
    
def obtener_info_plan_sub(plan_id)-> Dict[str, Any]:
    extra_url = f'plan-subscription/{plan_id}/'

    try:
        response = requests.get(URL_API_FREEMIUN+extra_url)
        response.raise_for_status()
        data = response.json()
        return {'data': data, 'status_code': response.status_code}

    except requests.exceptions.HTTPError as err:
        return {'error': err, 'status_code': response.status_code}
    except json.JSONDecodeError as err:
        return {'error': err, 'status_code': response.status_code}
    except Exception as err:
        return {'error': err, 'status_code': response.status_code}
    
def crear_granja(user_id, farm_name, farm_latitude, farm_longitude):
    data_sub = obtener_info_sub(user_id)['data']
    
    if 'Freemiun' in data_sub:
        if Farm.objects.filter(user_id=user_id).exists():
            return None
        else:
            farm = Farm.create_farm(
                int(user_id),
                farm_name,
                float(farm_latitude),
                float(farm_longitude)
                )
            return farm
    else:
        data_plan = obtener_info_plan_sub(data_sub["plan_subscription"])['data']
        max_farms = int(data_plan["farms"])
        if Farm.objects.filter(user_id=user_id).count() >= max_farms:
            return None
        else:
            farm = Farm.create_farm(
                int(user_id),
                farm_name,
                float(farm_latitude),
                float(farm_longitude)
                )
            return farm

def crear_parcela(user_id, farm, seed, width, length, crop_modality):
    data_sub = obtener_info_sub(user_id)['data']
    
    if 'Freemiun' in data_sub:
        if Farm.objects.filter(user_id=user_id).exists():
            return None
        else:
            parcel = Parcel.create_parcel(
                farm.id,
                seed.id,
                float(width),
                float(length),
                crop_modality
                )
            return parcel
    else:
        data_plan = obtener_info_plan_sub(data_sub["plan_subscription"])['data']
        max_farms = int(data_plan["farms"])
        if Farm.objects.filter(user_id=user_id).count() >= max_farms:
            return None
        else:
            parcel = Parcel.create_parcel(
                farm.id,
                seed.id,
                float(width),
                float(length),
                crop_modality
                )
            return parcel