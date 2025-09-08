"""User preferences value object.

This module contains user preferences value objects for customization and settings.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field
import bool
import default
import dict
import float
import getattr
import hasattr
import int
import key
import notification_type
import self
import setattr
import str
import value


class Theme(str, Enum):
    """UI theme enumeration."""

    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"


class Language(str, Enum):
    """Language enumeration."""

    VIETNAMESE = "vi"
    ENGLISH = "en"
    CHINESE = "zh"
    JAPANESE = "ja"
    KOREAN = "ko"


class Timezone(str, Enum):
    """Common timezone enumeration."""

    ASIA_HO_CHI_MINH = "Asia/Ho_Chi_Minh"
    UTC = "UTC"
    ASIA_TOKYO = "Asia/Tokyo"
    ASIA_SEOUL = "Asia/Seoul"
    ASIA_SHANGHAI = "Asia/Shanghai"
    US_PACIFIC = "US/Pacific"
    US_EASTERN = "US/Eastern"
    EUROPE_LONDON = "Europe/London"


class NotificationPreferences(BaseModel):
    """User notification preferences."""

    email_enabled: bool = Field(default=True)
    sms_enabled: bool = Field(default=False)
    push_enabled: bool = Field(default=True)
    in_app_enabled: bool = Field(default=True)

    # Notification types
    system_alerts: bool = Field(default=True)
    agent_updates: bool = Field(default=True)
    chat_notifications: bool = Field(default=True)
    workflow_notifications: bool = Field(default=True)
    security_alerts: bool = Field(default=True)

    # Timing
    quiet_hours_start: str = Field(
        default="22:00", description="Quiet hours start (HH:MM)"
    )
    quiet_hours_end: str = Field(default="08:00", description="Quiet hours end (HH:MM)")
    weekend_notifications: bool = Field(default=False)

    class Config:
        """Pydantic configuration."""

        use_enum_values = True
        validate_assignment = True


class PrivacyPreferences(BaseModel):
    """User privacy preferences."""

    data_collection_consent: bool = Field(default=False)
    analytics_consent: bool = Field(default=False)
    marketing_consent: bool = Field(default=False)

    # Data sharing
    share_usage_data: bool = Field(default=False)
    share_performance_data: bool = Field(default=False)
    share_error_reports: bool = Field(default=True)

    # Data retention
    auto_delete_old_chats: bool = Field(default=False)
    chat_retention_days: int = Field(default=90, ge=1, le=365)
    auto_delete_old_files: bool = Field(default=False)
    file_retention_days: int = Field(default=30, ge=1, le=365)

    class Config:
        """Pydantic configuration."""

        validate_assignment = True


class AIPreferences(BaseModel):
    """User AI interaction preferences."""

    # Model preferences
    preferred_model: str = Field(default="gpt-4")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2048, ge=100, le=32000)

    # Interaction style
    conversation_style: str = Field(
        default="balanced", description="professional, casual, balanced"
    )
    response_length: str = Field(default="medium", description="short, medium, long")
    explain_reasoning: bool = Field(default=False)

    # Memory and learning
    enable_memory: bool = Field(default=True)
    enable_learning: bool = Field(default=True)
    memory_retention_days: int = Field(default=30, ge=1, le=365)

    # Safety and filtering
    content_filter_level: str = Field(default="medium", description="low, medium, high")
    block_harmful_content: bool = Field(default=True)
    family_safe_mode: bool = Field(default=False)

    class Config:
        """Pydantic configuration."""

        validate_assignment = True


class UIPreferences(BaseModel):
    """User interface preferences."""

    # Appearance
    theme: Theme = Field(default=Theme.AUTO)
    font_size: str = Field(default="medium", description="small, medium, large")
    compact_mode: bool = Field(default=False)
    show_animations: bool = Field(default=True)

    # Layout
    sidebar_position: str = Field(default="left", description="left, right")
    sidebar_collapsed: bool = Field(default=False)
    show_chat_avatars: bool = Field(default=True)
    show_timestamps: bool = Field(default=True)

    # Chat interface
    auto_scroll: bool = Field(default=True)
    typing_indicators: bool = Field(default=True)
    read_receipts: bool = Field(default=True)
    message_grouping: bool = Field(default=True)

    # Advanced
    developer_mode: bool = Field(default=False)
    show_debug_info: bool = Field(default=False)
    keyboard_shortcuts: bool = Field(default=True)

    class Config:
        """Pydantic configuration."""

        use_enum_values = True
        validate_assignment = True


class AccessibilityPreferences(BaseModel):
    """User accessibility preferences."""

    # Visual
    high_contrast: bool = Field(default=False)
    large_text: bool = Field(default=False)
    reduced_motion: bool = Field(default=False)
    color_blind_friendly: bool = Field(default=False)

    # Audio
    screen_reader_support: bool = Field(default=False)
    audio_descriptions: bool = Field(default=False)
    sound_notifications: bool = Field(default=True)

    # Interaction
    sticky_keys: bool = Field(default=False)
    slow_keys: bool = Field(default=False)
    mouse_keys: bool = Field(default=False)
    voice_control: bool = Field(default=False)

    class Config:
        """Pydantic configuration."""

        validate_assignment = True


class UserPreferences(BaseModel):
    """Complete user preferences value object."""

    # Basic preferences
    language: Language = Field(default=Language.VIETNAMESE)
    timezone: Timezone = Field(default=Timezone.ASIA_HO_CHI_MINH)
    date_format: str = Field(default="DD/MM/YYYY")
    time_format: str = Field(default="24h", description="12h or 24h")

    # Detailed preferences
    notifications: NotificationPreferences = Field(
        default_factory=lambda: NotificationPreferences()
    )
    privacy: PrivacyPreferences = Field(default_factory=lambda: PrivacyPreferences())
    ai: AIPreferences = Field(default_factory=lambda: AIPreferences())
    ui: UIPreferences = Field(default_factory=lambda: UIPreferences())
    accessibility: AccessibilityPreferences = Field(
        default_factory=lambda: AccessibilityPreferences()
    )

    # Custom preferences
    custom_settings: dict[str, Any] = Field(default_factory=dict)

    def update_notification_preference(self, key: str, value: bool) -> None:
        """Update a notification preference."""
        if hasattr(self.notifications, key):
            setattr(self.notifications, key, value)

    def update_privacy_preference(self, key: str, value: bool | int) -> None:
        """Update a privacy preference."""
        if hasattr(self.privacy, key):
            setattr(self.privacy, key, value)

    def update_ai_preference(self, key: str, value: Any) -> None:
        """Update an AI preference."""
        if hasattr(self.ai, key):
            setattr(self.ai, key, value)

    def update_ui_preference(self, key: str, value: Any) -> None:
        """Update a UI preference."""
        if hasattr(self.ui, key):
            setattr(self.ui, key, value)

    def update_accessibility_preference(self, key: str, value: bool) -> None:
        """Update an accessibility preference."""
        if hasattr(self.accessibility, key):
            setattr(self.accessibility, key, value)

    def set_custom_setting(self, key: str, value: Any) -> None:
        """Set a custom setting."""
        self.custom_settings[key] = value

    def get_custom_setting(self, key: str, default: Any = None) -> Any:
        """Get a custom setting."""
        return self.custom_settings.get(key, default)

    def remove_custom_setting(self, key: str) -> None:
        """Remove a custom setting."""
        self.custom_settings.pop(key, None)

    def is_notification_enabled(self, notification_type: str) -> bool:
        """Check if a notification type is enabled."""
        return getattr(self.notifications, notification_type, False)

    def get_effective_theme(self) -> str:
        """Get the effective theme based on preferences."""
        if self.ui.theme == Theme.AUTO:
            # In a real implementation, this would check system theme
            return "light"  # Default fallback
        return self.ui.theme

    def get_locale_string(self) -> str:
        """Get locale string for i18n."""
        return f"{self.language}_{self.timezone.split('/')[1] if '/' in self.timezone else 'VN'}"

    class Config:
        """Pydantic configuration."""

        use_enum_values = True
        validate_assignment = True
