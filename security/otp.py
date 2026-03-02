"""
Redis-backed OTP utility.
──────────────────────────
• generate_otp(user_id) → 6-digit code, stored in Redis with 5-min TTL.
• verify_otp(user_id, code) → True/False.  Deletes key on success.
"""
import random
import redis
from django.conf import settings

_redis = redis.from_url(settings.REDIS_URL)

OTP_PREFIX = 'otp:'


def _key(user_id):
    return f'{OTP_PREFIX}{user_id}'


def generate_otp(user_id: int) -> str:
    """Generate a 6-digit OTP and store in Redis with TTL."""
    code = f'{random.randint(100000, 999999)}'
    _redis.setex(
        name=_key(user_id),
        time=settings.OTP_EXPIRY_SECONDS,   # default 300 s = 5 min
        value=code,
    )
    return code


def verify_otp(user_id: int, code: str) -> bool:
    """Verify OTP. Deletes the key on success (single-use)."""
    stored = _redis.get(_key(user_id))
    if stored is None:
        return False
    if stored.decode() == code:
        _redis.delete(_key(user_id))
        return True
    return False
