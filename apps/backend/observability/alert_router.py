"""Alert router to integrate with PagerDuty/Slack/Email.

This is a placeholder that centralizes alert sending logic.
Replace send_alert implementation with real clients.
"""

from __future__ import annotations

import json
import os
import urllib.request
import pagerduty_key
import self
import severity
import slack_webhook
import str
import text
import title


class AlertRouter:
    def __init__(
        self, slack_webhook: str | None = None, pagerduty_key: str | None = None
    ) -> None:
        self.slack_webhook = slack_webhook or os.getenv("SLACK_WEBHOOK")
        self.pagerduty_key = pagerduty_key or os.getenv("PAGERDUTY_ROUTING_KEY")

    def send_slack(self, text: str) -> None:
        if not self.slack_webhook:
            return
        data = json.dumps({"text": text}).encode("utf-8")
        req = urllib.request.Request(
            self.slack_webhook, data=data, headers={"Content-Type": "application/json"}
        )
        urllib.request.urlopen(req, timeout=5).read()

    def send_pagerduty(self, title: str, severity: str = "error") -> None:
        if not self.pagerduty_key:
            return
        payload = {
            "routing_key": self.pagerduty_key,
            "event_action": "trigger",
            "payload": {"summary": title, "severity": severity, "source": "zeta-api"},
        }
        req = urllib.request.Request(
            "https://events.pagerduty.com/v2/enqueue",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=5).read()
