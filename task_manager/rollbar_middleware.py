import os
from rollbar.contrib.django.middleware import RollbarNotifierMiddleware

ROLLBAR_ACCESS_TOKEN = os.getenv("ROLLBAR_ACCESS_TOKEN")
ROLLBAR_ENVIRONMENT = os.getenv("ROLLBAR_ENVIRONMENT", "development")


class CustomRollbarNotifierMiddleware(RollbarNotifierMiddleware):
    def __init__(self, get_response):
        super().__init__(
            get_response,
            access_token=ROLLBAR_ACCESS_TOKEN or None,
            environment=ROLLBAR_ENVIRONMENT,
        )
        self.disabled = not bool(ROLLBAR_ACCESS_TOKEN)

    def get_extra_data(self, request, exc):
        if getattr(self, "disabled", False):
            return {}
        extra_data = {}
        if hasattr(request, "session"):
            extra_data["session_id"] = request.session.session_key
        if hasattr(request, "resolver_match") and request.resolver_match:
            extra_data.update({
                "view_name": getattr(request.resolver_match, "view_name", None),
                "app_name": getattr(request.resolver_match, "app_name", None),
                "url_name": getattr(request.resolver_match, "url_name", None),
            })
        extra_data.update({"method": request.method, "path": request.path})
        return extra_data

    def get_payload_data(self, request, exc):
        if getattr(self, "disabled", False):
            return {}
        payload_data = {}
        if hasattr(request, "user") and not request.user.is_anonymous:
            payload_data["person"] = {
                "id": request.user.id,
                "username": request.user.username,
                "first_name": getattr(request.user, "first_name", ""),
                "last_name": getattr(request.user, "last_name", ""),
            }
        return payload_data
