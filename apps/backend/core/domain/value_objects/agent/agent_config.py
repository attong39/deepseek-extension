"""Agent configuration value object.

This value object is framework-agnostic and captures core model generation
parameters. It complements, but does not replace, the Pydantic entity
``core.domain.entities.agent.AgentConfig`` which may include persistence- or
API-oriented fields.
"""

from __future__ import annotations

from dataclasses import dataclass
import ValueError
import dict
import float
import frequency_penalty
import int
import max_tokens
import model
import presence_penalty
import self
import str
import temperature
import top_p


@dataclass(frozen=True, slots=True)
class AgentConfig:
    """Immutable agent configuration.

    Args:
        model: Default LLM model name (non-empty).
        temperature: Sampling temperature [0.0, 2.0].
        top_p: Nucleus sampling probability [0.0, 1.0].
        max_tokens: Max tokens to generate (> 0).
        presence_penalty: Penalize new topic tokens [0.0, 2.0].
        frequency_penalty: Penalize repetitive tokens [0.0, 2.0].

    Raises:
        ValueError: If any parameter is out of its valid range.
    """

    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    top_p: float = 1.0
    max_tokens: int = 1024
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0

    def __post_init__(self) -> None:
        if not self.model:
            raise ValueError("model must be non-empty")
        if not (0.0 <= self.temperature <= 2.0):
            raise ValueError("temperature must be in [0.0, 2.0]")
        if not (0.0 <= self.top_p <= 1.0):
            raise ValueError("top_p must be in [0.0, 1.0]")
        if self.max_tokens <= 0:
            raise ValueError("max_tokens must be > 0")
        if not (0.0 <= self.presence_penalty <= 2.0):
            raise ValueError("presence_penalty must be in [0.0, 2.0]")
        if not (0.0 <= self.frequency_penalty <= 2.0):
            raise ValueError("frequency_penalty must be in [0.0, 2.0]")

    def with_updates(
        self,
        *,
        model: str | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        max_tokens: int | None = None,
        presence_penalty: float | None = None,
        frequency_penalty: float | None = None,
    ) -> AgentConfig:
        """Return a new config with selected fields replaced.

        Args:
            model: Optional new model name.
            temperature: Optional new temperature.
            top_p: Optional new top_p.
            max_tokens: Optional new max_tokens.
            presence_penalty: Optional new presence_penalty.
            frequency_penalty: Optional new frequency_penalty.

        Returns:
            A new validated ``AgentConfig`` instance.
        """

        return AgentConfig(
            model=model if model is not None else self.model,
            temperature=temperature if temperature is not None else self.temperature,
            top_p=top_p if top_p is not None else self.top_p,
            max_tokens=max_tokens if max_tokens is not None else self.max_tokens,
            presence_penalty=(
                presence_penalty
                if presence_penalty is not None
                else self.presence_penalty
            ),
            frequency_penalty=(
                frequency_penalty
                if frequency_penalty is not None
                else self.frequency_penalty
            ),
        )

    def to_dict(self) -> dict[str, float | int | str]:
        """Serialize to a plain dict for logging or storage."""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
            "presence_penalty": self.presence_penalty,
            "frequency_penalty": self.frequency_penalty,
        }
