"""Security hardening and input validation system for ZETA AI.





This module provides comprehensive security hardening including:


- Advanced input validation and sanitization


- SQL injection prevention


- XSS protection


- CSRF protection


- Rate limiting with anomaly detection


- Security headers management


"""

from __future__ import annotations

import html
import ipaddress
import re
import secrets
import unicodedata
from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any
from urllib.parse import quote, urlparse
from uuid import uuid4

import bleach
from pydantic import BaseModel, Field
import Exception
import TypeError
import ValueError
import any
import bool
import code
import dict
import e
import err
import expiry
import field
import field_name
import float
import i
import int
import isinstance
import kwargs
import len
import list
import message
import raw_input
import required
import result
import sanitization_type
import sanitization_types
import secret_key
import self
import session_id
import severity
import start_time
import str
import super
import threat_type
import threat_types
import validation_type

# Input validation patterns


EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


PHONE_PATTERN = re.compile(
    r"^\+?1?-?\.?\s?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$"
)


URL_PATTERN = re.compile(
    r"^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$"
)


UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


# SQL injection patterns


SQL_INJECTION_PATTERNS = [
    r"('|(\\'))+.*(or|and|exec|execute|select|union|insert|update|delete|drop|create|alter)",
    r"(union|select|insert|update|delete|drop|create|alter).*('|(\\'))",
    r"(exec|execute)\s*(sp_|xp_)",
    r"(script|javascript|vbscript|onload|onerror|onclick)",
    r"(<|&lt;).*script.*(>|&gt;)",
]


# XSS patterns


XSS_PATTERNS = [
    r"<script[^>]*>.*?</script>",
    r"javascript:",
    r"vbscript:",
    r"onload\s*=",
    r"onerror\s*=",
    r"onclick\s*=",
    r"onmouseover\s*=",
    r"<iframe",
    r"<object",
    r"<embed",
    r"<form",
]


class ValidationError(Exception):
    """Custom validation error."""

    def __init__(self, message: str, field: str | None = None, code: str | None = None):
        """Initialize validation error.





        Args:


            message: Error message


            field: Field name that failed validation


            code: Error code


        """

        super().__init__(message)

        self.field = field

        self.code = code


class ValidationType(str, Enum):
    """Input validation types."""

    STRING = "string"

    EMAIL = "email"

    URL = "url"

    UUID = "uuid"

    INTEGER = "integer"

    FLOAT = "float"

    BOOLEAN = "boolean"

    JSON = "json"

    HTML = "html"

    SQL = "sql"

    PHONE = "phone"

    CREDIT_CARD = "credit_card"

    IP_ADDRESS = "ip_address"


class SanitizationType(str, Enum):
    """Data sanitization types."""

    HTML_ESCAPE = "html_escape"

    HTML_STRIP = "html_strip"

    HTML_CLEAN = "html_clean"

    SQL_ESCAPE = "sql_escape"

    URL_ENCODE = "url_encode"

    ALPHANUMERIC_ONLY = "alphanumeric_only"

    TRIM_WHITESPACE = "trim_whitespace"

    NORMALIZE_UNICODE = "normalize_unicode"


class SecurityThreatType(str, Enum):
    """Security threat types."""

    SQL_INJECTION = "sql_injection"

    XSS = "xss"

    CSRF = "csrf"

    DIRECTORY_TRAVERSAL = "directory_traversal"

    COMMAND_INJECTION = "command_injection"

    XXSS = "xxss"

    MALICIOUS_FILE = "malicious_file"

    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"


class ValidationRule(BaseModel):
    """Input validation rule."""

    field_name: str

    validation_type: ValidationType

    required: bool = Field(default=True)

    min_length: int | None = None

    max_length: int | None = None

    min_value: int | float | None = None

    max_value: int | float | None = None

    pattern: str | None = None

    allowed_values: list[Any] | None = None

    custom_validator: str | None = None

    sanitize: list[SanitizationType] = Field(default_factory=list)


class SecurityIncident(BaseModel):
    """Security incident detected during validation."""

    incident_id: str = Field(default_factory=lambda: str(uuid4()))

    threat_type: SecurityThreatType

    severity: str = Field(default="medium")  # low, medium, high, critical

    field_name: str | None = None

    raw_input: str

    sanitized_input: str | None = None

    ip_address: str | None = None

    user_agent: str | None = None

    user_id: str | None = None

    session_id: str | None = None

    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    blocked: bool = Field(default=True)


class RateLimitRule(BaseModel):
    """Rate limiting rule."""

    name: str

    max_requests: int

    time_window_seconds: int

    scope: str = Field(default="ip")  # ip, user, session, global

    burst_allowance: int = Field(default=0)

    block_duration_seconds: int = Field(default=300)  # 5 minutes default


class InputValidator:
    """Advanced input validation system."""

    def __init__(self):
        """Initialize input validator."""

        self._sql_patterns = [
            re.compile(pattern, re.IGNORECASE) for pattern in SQL_INJECTION_PATTERNS
        ]

        self._xss_patterns = [
            re.compile(pattern, re.IGNORECASE) for pattern in XSS_PATTERNS
        ]

        self._incidents: list[SecurityIncident] = []

        # Bleach configuration for HTML cleaning

        self._allowed_html_tags = [
            "p",
            "br",
            "strong",
            "em",
            "u",
            "ol",
            "ul",
            "li",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "blockquote",
        ]

        self._allowed_html_attributes = {
            "*": ["class"],
            "a": ["href", "title"],
            "img": ["src", "alt", "width", "height"],
        }

    def validate_input(
        self,
        data: Any,
        validation_type: ValidationType,
        field_name: str | None = None,
        **kwargs,
    ) -> Any:
        """Validate input data.





        Args:


            data: Data to validate


            validation_type: Type of validation to perform


            field_name: Field name for error reporting


            **kwargs: Additional validation parameters





        Returns:


            Validated data





        Raises:


            ValidationError: If validation fails


        """

        if data is None:
            if kwargs.get("required", True):
                raise ValidationError(
                    f"Field {field_name or 'unknown'} is required", field_name
                )

            return None

        try:
            if validation_type == ValidationType.STRING:
                return self._validate_string(data, field_name, **kwargs)

            elif validation_type == ValidationType.EMAIL:
                return self._validate_email(data, field_name)

            elif validation_type == ValidationType.URL:
                return self._validate_url(data, field_name)

            elif validation_type == ValidationType.UUID:
                return self._validate_uuid(data, field_name)

            elif validation_type == ValidationType.INTEGER:
                return self._validate_integer(data, field_name, **kwargs)

            elif validation_type == ValidationType.FLOAT:
                return self._validate_float(data, field_name, **kwargs)

            elif validation_type == ValidationType.BOOLEAN:
                return self._validate_boolean(data, field_name)

            elif validation_type == ValidationType.JSON:
                return self._validate_json(data, field_name)

            elif validation_type == ValidationType.HTML:
                return self._validate_html(data, field_name, **kwargs)

            elif validation_type == ValidationType.PHONE:
                return self._validate_phone(data, field_name)

            elif validation_type == ValidationType.IP_ADDRESS:
                return self._validate_ip_address(data, field_name)

            else:
                raise ValidationError(
                    f"Unsupported validation type: {validation_type}", field_name
                )

        except ValidationError:
            raise

        except Exception as e:
            raise ValidationError(f"Validation error: {e!s}", field_name) from e

    def _validate_string(self, data: Any, field_name: str | None, **kwargs) -> str:
        """Validate string input."""

        if not isinstance(data, str):
            data = str(data)

        # Check length constraints

        min_length = kwargs.get("min_length")

        max_length = kwargs.get("max_length")

        if min_length is not None and len(data) < min_length:
            raise ValidationError(
                f"Field {field_name} must be at least {min_length} characters",
                field_name,
            )

        if max_length is not None and len(data) > max_length:
            raise ValidationError(
                f"Field {field_name} must be at most {max_length} characters",
                field_name,
            )

        # Check pattern

        pattern = kwargs.get("pattern")

        if pattern and not re.match(pattern, data):
            raise ValidationError(
                f"Field {field_name} does not match required pattern", field_name
            )

        # Check allowed values

        allowed_values = kwargs.get("allowed_values")

        if allowed_values and data not in allowed_values:
            raise ValidationError(
                f"Field {field_name} must be one of: {allowed_values}", field_name
            )

        return data

    def _validate_email(self, data: Any, field_name: str | None) -> str:
        """Validate email input."""

        email = str(data).strip().lower()

        if not EMAIL_PATTERN.match(email):
            raise ValidationError(
                f"Field {field_name} is not a valid email address", field_name
            )

        if len(email) > 254:  # RFC 5321 limit
            raise ValidationError(
                f"Field {field_name} email address is too long", field_name
            )

        return email

    def _validate_url(self, data: Any, field_name: str | None) -> str:
        """Validate URL input."""

        url = str(data).strip()

        if not URL_PATTERN.match(url):
            raise ValidationError(f"Field {field_name} is not a valid URL", field_name)

        # Additional security checks

        parsed = urlparse(url)

        if parsed.scheme not in ["http", "https"]:
            raise ValidationError(
                f"Field {field_name} URL must use HTTP or HTTPS", field_name
            )

        return url

    def _validate_uuid(self, data: Any, field_name: str | None) -> str:
        """Validate UUID input."""

        uuid_str = str(data).strip()

        if not UUID_PATTERN.match(uuid_str):
            raise ValidationError(f"Field {field_name} is not a valid UUID", field_name)

        return uuid_str.lower()

    def _validate_integer(self, data: Any, field_name: str | None, **kwargs) -> int:
        """Validate integer input."""

        try:
            value = int(data)

        except (ValueError, TypeError) as err:
            raise ValidationError(
                f"Field {field_name} must be an integer", field_name
            ) from err

        min_value = kwargs.get("min_value")

        max_value = kwargs.get("max_value")

        if min_value is not None and value < min_value:
            raise ValidationError(
                f"Field {field_name} must be at least {min_value}", field_name
            )

        if max_value is not None and value > max_value:
            raise ValidationError(
                f"Field {field_name} must be at most {max_value}", field_name
            )

        return value

    def _validate_float(self, data: Any, field_name: str | None, **kwargs) -> float:
        """Validate float input."""

        try:
            value = float(data)

        except (ValueError, TypeError) as err:
            raise ValidationError(
                f"Field {field_name} must be a number", field_name
            ) from err

        min_value = kwargs.get("min_value")

        max_value = kwargs.get("max_value")

        if min_value is not None and value < min_value:
            raise ValidationError(
                f"Field {field_name} must be at least {min_value}", field_name
            )

        if max_value is not None and value > max_value:
            raise ValidationError(
                f"Field {field_name} must be at most {max_value}", field_name
            )

        return value

    def _validate_boolean(self, data: Any, field_name: str | None) -> bool:
        """Validate boolean input."""

        if isinstance(data, bool):
            return data

        if isinstance(data, str):
            lower_data = data.lower().strip()

            if lower_data in ("true", "1", "yes", "on"):
                return True

            elif lower_data in ("false", "0", "no", "off"):
                return False

        raise ValidationError(f"Field {field_name} must be a boolean value", field_name)

    def _validate_json(self, data: Any, field_name: str | None) -> Any:
        """Validate JSON input."""

        if isinstance(data, (dict, list)):
            return data

        if isinstance(data, str):
            try:
                import json

                return json.loads(data)

            except json.JSONDecodeError as err:
                raise ValidationError(
                    f"Field {field_name} is not valid JSON", field_name
                ) from err

        raise ValidationError(f"Field {field_name} must be valid JSON", field_name)

    def _validate_html(self, data: Any, field_name: str | None, **kwargs) -> str:
        """Validate HTML input."""

        html_content = str(data)

        # Check for XSS patterns

        if self._detect_xss(html_content):
            self._log_security_incident(
                SecurityThreatType.XSS, field_name, html_content, "high"
            )

            raise ValidationError(
                f"Field {field_name} contains potentially malicious content", field_name
            )

        # Clean HTML if requested

        if kwargs.get("clean_html", True):
            html_content = bleach.clean(
                html_content,
                tags=self._allowed_html_tags,
                attributes=self._allowed_html_attributes,
                strip=True,
            )

        return html_content

    def _validate_phone(self, data: Any, field_name: str | None) -> str:
        """Validate phone number input."""

        phone = str(data).strip()

        if not PHONE_PATTERN.match(phone):
            raise ValidationError(
                f"Field {field_name} is not a valid phone number", field_name
            )

        return phone

    def _validate_ip_address(self, data: Any, field_name: str | None) -> str:
        """Validate IP address input."""

        # ipaddress imported at module level

        ip_str = str(data).strip()

        try:
            # Validate as IPv4 or IPv6

            ipaddress.ip_address(ip_str)

            return ip_str

        except ValueError as err:
            raise ValidationError(
                f"Field {field_name} is not a valid IP address", field_name
            ) from err

    def sanitize_input(
        self, data: Any, sanitization_types: list[SanitizationType]
    ) -> Any:
        """Sanitize input data.





        Args:


            data: Data to sanitize


            sanitization_types: Types of sanitization to apply





        Returns:


            Sanitized data


        """

        if data is None:
            return None

        _ = data

        for sanitization_type in sanitization_types:
            if sanitization_type == SanitizationType.HTML_ESCAPE:
                _ = html.escape(str(result))

            elif sanitization_type == SanitizationType.HTML_STRIP:
                _ = bleach.clean(str(result), tags=[], strip=True)

            elif sanitization_type == SanitizationType.HTML_CLEAN:
                _ = bleach.clean(
                    str(result),
                    tags=self._allowed_html_tags,
                    attributes=self._allowed_html_attributes,
                    strip=True,
                )

            elif sanitization_type == SanitizationType.SQL_ESCAPE:
                _ = str(result).replace("'", "''").replace('"', '""')

            elif sanitization_type == SanitizationType.URL_ENCODE:
                _ = quote(str(result))

            elif sanitization_type == SanitizationType.ALPHANUMERIC_ONLY:
                _ = re.sub(r"[^a-zA-Z0-9]", "", str(result))

            elif sanitization_type == SanitizationType.TRIM_WHITESPACE:
                _ = str(result).strip()

            elif sanitization_type == SanitizationType.NORMALIZE_UNICODE:
                # unicodedata imported at module level
                _ = unicodedata.normalize("NFKC", str(result))

        return result

    def detect_threats(
        self,
        data: Any,
        field_name: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> list[SecurityIncident]:
        """Detect security threats in input data.





        Args:


            data: Data to analyze


            field_name: Field name


            context: Additional context (user_id, ip_address, etc.)





        Returns:


            List of detected security incidents


        """

        if data is None:
            return []

        data_str = str(data)

        incidents = []

        # SQL injection detection

        if self._detect_sql_injection(data_str):
            incident = self._create_security_incident(
                SecurityThreatType.SQL_INJECTION, field_name, data_str, "high", context
            )

            incidents.append(incident)

        # XSS detection

        if self._detect_xss(data_str):
            incident = self._create_security_incident(
                SecurityThreatType.XSS, field_name, data_str, "high", context
            )

            incidents.append(incident)

        # Directory traversal detection

        if self._detect_directory_traversal(data_str):
            incident = self._create_security_incident(
                SecurityThreatType.DIRECTORY_TRAVERSAL,
                field_name,
                data_str,
                "medium",
                context,
            )

            incidents.append(incident)

        # Command injection detection

        if self._detect_command_injection(data_str):
            incident = self._create_security_incident(
                SecurityThreatType.COMMAND_INJECTION,
                field_name,
                data_str,
                "critical",
                context,
            )

            incidents.append(incident)

        # Store incidents

        self._incidents.extend(incidents)

        return incidents

    def _detect_sql_injection(self, data: str) -> bool:
        """Detect SQL injection patterns."""

        data_lower = data.lower()

        return any(pattern.search(data_lower) for pattern in self._sql_patterns)

    def _detect_xss(self, data: str) -> bool:
        """Detect XSS patterns."""

        data_lower = data.lower()

        return any(pattern.search(data_lower) for pattern in self._xss_patterns)

    def _detect_directory_traversal(self, data: str) -> bool:
        """Detect directory traversal patterns."""

        patterns = ["../", "..\\", "%2e%2e%2f", "%2e%2e%5c"]

        data_lower = data.lower()

        return any(pattern in data_lower for pattern in patterns)

    def _detect_command_injection(self, data: str) -> bool:
        """Detect command injection patterns."""

        patterns = [";", "|", "&", "$", "`", "$(", "${"]

        return any(pattern in data for pattern in patterns)

    def _create_security_incident(
        self,
        threat_type: SecurityThreatType,
        field_name: str | None,
        raw_input: str,
        severity: str,
        context: dict[str, Any] | None = None,
    ) -> SecurityIncident:
        """Create security incident record."""

        context = context or {}

        return SecurityIncident(
            threat_type=threat_type,
            severity=severity,
            field_name=field_name,
            raw_input=raw_input,
            ip_address=context.get("ip_address"),
            user_agent=context.get("user_agent"),
            user_id=context.get("user_id"),
            session_id=context.get("session_id"),
        )

    def _log_security_incident(
        self,
        threat_type: SecurityThreatType,
        field_name: str | None,
        raw_input: str,
        severity: str,
    ) -> None:
        """Log security incident."""

        incident = self._create_security_incident(
            threat_type, field_name, raw_input, severity
        )

        self._incidents.append(incident)

    def get_security_incidents(
        self,
        start_time: datetime | None = None,
        threat_types: list[SecurityThreatType] | None = None,
        severity: str | None = None,
    ) -> list[SecurityIncident]:
        """Get security incidents with optional filtering.





        Args:


            start_time: Filter by start time


            threat_types: Filter by threat types


            severity: Filter by severity





        Returns:


            List of security incidents


        """

        incidents = self._incidents

        if start_time:
            incidents = [i for i in incidents if i.timestamp >= start_time]

        if threat_types:
            incidents = [i for i in incidents if i.threat_type in threat_types]

        if severity:
            incidents = [i for i in incidents if i.severity == severity]

        return incidents


class CSRFProtection:
    """CSRF protection system."""

    def __init__(self, secret_key: str | None = None):
        """Initialize CSRF protection.





        Args:


            secret_key: Secret key for token generation


        """

        self.secret_key = secret_key or secrets.token_urlsafe(32)

        self._tokens: dict[str, datetime] = {}

    def generate_token(self, session_id: str) -> str:
        """Generate CSRF token for session.





        Args:


            session_id: Session ID





        Returns:


            CSRF token


        """

        token = secrets.token_urlsafe(32)

        self._tokens[f"{session_id}:{token}"] = datetime.now(UTC) + timedelta(hours=24)

        return token

    def validate_token(self, session_id: str, token: str) -> bool:
        """Validate CSRF token.





        Args:


            session_id: Session ID


            token: CSRF token to validate





        Returns:


            True if token is valid


        """

        key = f"{session_id}:{token}"

        if key not in self._tokens:
            return False

        if datetime.now(UTC) > self._tokens[key]:
            del self._tokens[key]

            return False

        return True

    def cleanup_expired_tokens(self) -> None:
        """Clean up expired CSRF tokens."""

        current_time = datetime.now(UTC)

        expired_keys = [
            key for key, expiry in self._tokens.items() if current_time > expiry
        ]

        for key in expired_keys:
            del self._tokens[key]


# Factory functions


def create_input_validator() -> InputValidator:
    """Create input validator instance.





    Returns:


        InputValidator instance


    """

    return InputValidator()


def create_csrf_protection(secret_key: str | None = None) -> CSRFProtection:
    """Create CSRF protection instance.





    Args:


        secret_key: Optional secret key





    Returns:


        CSRFProtection instance


    """

    return CSRFProtection(secret_key)


def create_validation_rule(
    field_name: str, validation_type: ValidationType, required: bool = True, **kwargs
) -> ValidationRule:
    """Create validation rule.





    Args:


        field_name: Field name


        validation_type: Validation type


        required: Whether field is required


        **kwargs: Additional validation parameters





    Returns:


        Validation rule


    """

    return ValidationRule(
        field_name=field_name,
        validation_type=validation_type,
        required=required,
        **kwargs,
    )
