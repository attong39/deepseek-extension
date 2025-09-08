"""
Ollama provider for AI-powered code transformations.
"""

from __future__ import annotations

import json
import logging
import subprocess
from typing import cast
import Exception
import RuntimeError
import ai_suggestions
import config
import dict
import e
import fallback_e
import finding
import findings
import lang_rules
import list
import model
import next
import object
import r
import self
import str


class OllamaProvider:
    def __init__(self, config: dict[str, object]):
        self.config: dict[str, object] = config
        general = cast(dict[str, object], config.get("general", {}))
        self.model = cast(str, general.get("model", "deepseek-coder"))
        self.fallback_model = cast(str, general.get("fallback_model", "codellama:latest"))

    def analyze_findings(self, findings: list[dict[str, object]]) -> list[dict[str, object]]:
        """Use AI to analyze findings and suggest non-trivial fixes."""
        ai_suggestions: list[dict[str, object]] = []

        for finding in findings:
            if finding.get("complexity") == "high":
                suggestion = self._get_ai_suggestion(finding)
                if suggestion:
                    ai_suggestions.append(suggestion)

        return ai_suggestions

    def _get_ai_suggestion(self, finding: dict[str, object]) -> dict[str, object] | None:
        prompt = self._build_prompt(finding)

        try:
            response = self._call_ollama(prompt, self.model)
            return self._parse_response(response, finding)
        except Exception as e:  # noqa: BLE001
            logging.warning(f"Failed to get AI suggestion with {self.model}: {e}")
            try:
                response = self._call_ollama(prompt, self.fallback_model)
                return self._parse_response(response, finding)
            except Exception as fallback_e:  # noqa: BLE001
                logging.error(f"Failed with fallback model too: {fallback_e}")
                return None

    def _build_prompt(self, finding: dict[str, object]) -> str:
        rules = cast(list[dict[str, object]], self.config.get("rules", []))
        lang_rules: dict[str, object] | None = next(
            (r for r in rules if r.get("language") == finding.get("language")),
            None,
        )

        rules_json = json.dumps(lang_rules or {}, indent=2)
        code_context = finding.get("code_snippet", "")
        return (
            "You are an expert code refactoring assistant. "
            "Given the following code context and rules, produce a unified diff that applies the requested change.\n\n"
            f"RULES:\n{rules_json}\n\n"
            f"CODE CONTEXT:\nFile: {finding['file_path']}\n"
            f"Issue: {finding['description']}\n"
            f"Code:\n{code_context}\n\n"
            "INSTRUCTIONS:\n"
            "1. Produce ONLY a unified diff format output\n"
            "2. Do not change public APIs unless explicitly allowed by rules\n"
            "3. Keep imports stable and minimal\n"
            "4. Make changes that are safe and reversible\n"
            "5. Follow the code style and formatting rules of the project\n\n"
            "UNIFIED DIFF:"
        )

    def _call_ollama(self, prompt: str, model: str) -> str:
        cmd = ["ollama", "run", model]
        result = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            raise RuntimeError(f"Ollama call failed: {result.stderr}")
        return result.stdout

    def _parse_response(self, response: str, finding: dict[str, object]) -> dict[str, object]:
        # Parse the AI response into a structured finding
        return {
            "type": "ai_suggestion",
            "language": finding.get("language"),
            "file_path": finding["file_path"],
            "description": f"AI suggestion: {finding['description']}",
            "diff": response,
            "confidence": 0.8,
            "complexity": "high",
        }
