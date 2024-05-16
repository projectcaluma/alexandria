import base64
import functools
import hashlib

import requests
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured, SuspiciousOperation
from django.utils.encoding import force_bytes
from django.utils.module_loading import import_string
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


def get_user_and_group(request):
    if request is None:  # pragma: no cover
        return None, None

    user = getattr(request.user, settings.ALEXANDRIA_CREATED_BY_USER_PROPERTY, None)
    group = getattr(request.user, settings.ALEXANDRIA_CREATED_BY_GROUP_PROPERTY, None)
    return user, group


class AlexandriaAuthenticationBackend(OIDCAuthenticationBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.OIDC_USERNAME_CLAIM = self.get_settings("OIDC_USERNAME_CLAIM")
        self.OIDC_OP_INTROSPECT_ENDPOINT = self.get_settings(
            "OIDC_OP_INTROSPECT_ENDPOINT"
        )
        self.OIDC_BEARER_TOKEN_REVALIDATION_TIME = self.get_settings(
            "OIDC_BEARER_TOKEN_REVALIDATION_TIME"
        )
        self.OIDC_VERIFY_SSL = self.get_settings("OIDC_VERIFY_SSL", True)

    def _oidc_user(self, *args, **kwargs):
        factory = import_string(settings.ALEXANDRIA_OIDC_USER_FACTORY)
        return factory(*args, **kwargs)

    def get_introspection(self, access_token, id_token, payload):
        """Return user details dictionary."""

        basic = base64.b64encode(
            f"{self.OIDC_RP_CLIENT_ID}:{self.OIDC_RP_CLIENT_SECRET}".encode("utf-8")
        ).decode()
        headers = {
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = requests.post(
            self.OIDC_OP_INTROSPECT_ENDPOINT,
            verify=self.OIDC_VERIFY_SSL,
            headers=headers,
            data={"token": access_token},
        )
        response.raise_for_status()
        return response.json()

    def get_userinfo_or_introspection(self, access_token) -> dict:
        try:
            claims = self.cached_request(
                self.get_userinfo, access_token, "auth.userinfo"
            )
        except requests.HTTPError as e:
            if not (
                e.response.status_code in [401, 403]
                and self.OIDC_OP_INTROSPECT_ENDPOINT
            ):
                raise e

            # check introspection if userinfo fails (confidental client)
            claims = self.cached_request(
                self.get_introspection, access_token, "auth.introspection"
            )
            if "client_id" not in claims:
                raise SuspiciousOperation("client_id not present in introspection")

        return claims

    def get_or_create_user(self, access_token, id_token, payload):
        """Verify claims and return user, otherwise raise an Exception."""

        claims = self.get_userinfo_or_introspection(access_token)
        user = self._oidc_user(access_token, claims)

        return user

    def cached_request(self, method, token, cache_prefix):
        token_hash = hashlib.sha256(force_bytes(token)).hexdigest()

        func = functools.partial(method, token, None, None)

        return cache.get_or_set(
            f"{cache_prefix}.{token_hash}",
            func,
            timeout=self.OIDC_BEARER_TOKEN_REVALIDATION_TIME,
        )


class DevelopmentAuthenticationBackend(AlexandriaAuthenticationBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not settings.DEBUG:
            raise ImproperlyConfigured(
                "The Dev auth backend can only be used in DEBUG mode!"
            )

    def get_introspection(self, access_token, id_token, payload):  # pragma: no cover
        return {
            settings.OIDC_USERNAME_CLAIM: "dev",
            settings.OIDC_GROUPS_CLAIM: ["dev-group", "secondary-group"],
        }

    def get_userinfo_or_introspection(self, access_token) -> dict:  # pragma: no cover
        return {
            settings.OIDC_USERNAME_CLAIM: "dev",
            settings.OIDC_GROUPS_CLAIM: ["dev-group", "secondary-group"],
        }

    def get_or_create_user(self, access_token, id_token, payload):
        return self._oidc_user(
            access_token,
            {
                settings.OIDC_USERNAME_CLAIM: "dev",
                settings.OIDC_GROUPS_CLAIM: ["dev-group", "secondary-group"],
            },
        )
