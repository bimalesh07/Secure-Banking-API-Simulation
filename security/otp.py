import random
import redis
from django.conf import settings

_redis = redis.from_url(settings.REDIS_URL)

OTP_PREFIX = 'otp:'


def _key(user_id):
    return f'{OTP_PREFIX}{user_id}'


def generate_otp(user_id: int) -> str:
    code = f'{random.randint(100000, 999999)}'
    _redis.setex(
        name=_key(user_id),
        time=settings.OTP_EXPIRY_SECONDS,
        value=code,
    )
    return code


def verify_otp(user_id: int, code: str) -> bool:
    stored = _redis.get(_key(user_id))
    if stored is None:
        return False
    if stored.decode() == code:
        _redis.delete(_key(user_id))
        return True
    return False
