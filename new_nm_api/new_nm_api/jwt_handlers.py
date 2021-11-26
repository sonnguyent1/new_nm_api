from rest_framework_jwt.utils import jwt_payload_handler
from rest_framework_jwt.settings import api_settings


def nm_jwt_playload_handler(user):
    payload = jwt_payload_handler(user)
    payload['first_name'] = user.first_name
    payload['last_name'] = user.last_name
    payload['ttl'] = api_settings.JWT_EXPIRATION_DELTA.total_seconds() * 1000
    return payload
