from __future__ import annotations

from collections.abc import Callable
from threading import Lock
from typing import Any

from core.exceptions import AuthenticationError, ConfigurationError
from core.settings import Settings
from shared.schemas import CurrentUser


_firebase_app: Any | None = None
_firebase_app_lock = Lock()


class FirebaseAuthService:
    """Verifies Firebase ID tokens using Firebase Admin and Google ADC."""

    def __init__(
        self,
        settings: Settings,
        *,
        token_verifier: Callable[[str], dict[str, Any]] | None = None,
    ) -> None:
        self.settings = settings
        self._token_verifier = token_verifier

    def verify_id_token(self, token: str) -> CurrentUser:
        if not token or not token.strip():
            raise AuthenticationError("Authentication token is missing.")

        try:
            decoded = self._verifier()(token)
        except AuthenticationError:
            raise
        except ConfigurationError:
            raise
        except Exception as error:
            raise AuthenticationError("Invalid or expired authentication token.") from error

        uid = decoded.get("uid") or decoded.get("sub")
        if not isinstance(uid, str) or not uid:
            raise AuthenticationError("Authentication token has no valid user identity.")

        sensitive_claims = {"access_token", "id_token", "refresh_token"}
        claims = {key: value for key, value in decoded.items() if key not in sensitive_claims}
        return CurrentUser(
            uid=uid,
            email=decoded.get("email"),
            name=decoded.get("name"),
            picture=decoded.get("picture"),
            email_verified=bool(decoded.get("email_verified", False)),
            claims=claims,
        )

    def _verifier(self) -> Callable[[str], dict[str, Any]]:
        if self._token_verifier is not None:
            return self._token_verifier

        app, auth = self._get_firebase_components()
        return lambda token: auth.verify_id_token(token, app=app, check_revoked=True)

    def _get_firebase_components(self) -> tuple[Any, Any]:
        project_id = self.settings.firebase_project_id
        if not project_id:
            raise ConfigurationError(
                "FIREBASE_PROJECT_ID or GOOGLE_CLOUD_PROJECT is required for Firebase Auth."
            )

        try:
            import firebase_admin
            from firebase_admin import auth, credentials
        except ImportError as error:
            raise ConfigurationError("firebase-admin is required for Firebase Auth.") from error

        global _firebase_app
        if _firebase_app is None:
            with _firebase_app_lock:
                if _firebase_app is None:
                    try:
                        _firebase_app = firebase_admin.get_app()
                    except ValueError:
                        _firebase_app = firebase_admin.initialize_app(
                            credentials.ApplicationDefault(),
                            options={"projectId": project_id},
                        )
        return _firebase_app, auth

    # Compatibility alias for callers of the previous skeleton.
    def verify_token(self, token: str) -> CurrentUser:
        return self.verify_id_token(token)
