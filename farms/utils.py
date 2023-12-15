from typing import Dict, Any
import json
import requests

URL_API_CRUD = "https://weedweb-crud.onrender.com/users/api/"

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