from functools import wraps

from flask import request


def validate_request(required_keys: list = [], optional_keys: list = [], root_key: str = "data"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            payload = request.get_json(force=True)
            data = payload.get(root_key, None)
            if data is None:
                return {'error': 'Invalid payload.'}

            data_keys = set(data.keys())
            missing_keys = set(required_keys) - data_keys
            wrong_keys = data_keys - set(required_keys)
            wrong_keys -= set(optional_keys)

            if missing_keys or wrong_keys:
                return {'error': 'Invalid payload.'}

            return func(*args, **kwargs)

        return wrapper

    return decorator
