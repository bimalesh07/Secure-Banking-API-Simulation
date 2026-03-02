from rest_framework.throttling import SimpleRateThrottle


class OTPRateThrottle(SimpleRateThrottle):
    scope = 'otp'

    def get_cache_key(self, request, view):
        return self.cache_format % {
            'scope': self.scope,
            'ident': request.user.pk if request.user.is_authenticated else self.get_ident(request),
        }


class TransferRateThrottle(SimpleRateThrottle):
    scope = 'transfer'

    def get_cache_key(self, request, view):
        return self.cache_format % {
            'scope': self.scope,
            'ident': request.user.pk if request.user.is_authenticated else self.get_ident(request),
        }


class AuthRateThrottle(SimpleRateThrottle):
    scope = 'auth'

    def get_cache_key(self, request, view):
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request),
        }
