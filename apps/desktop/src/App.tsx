import { AppBar, Box, Button, Chip, Container, Toolbar, Typography } from "@mui/material";
import { useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";

import { LearningPanel } from "./components/LearningPanel";
import { LoginForm } from "./components/LoginForm";
import { MainDashboard } from "./components/MainDashboard";
import { useChat } from "./hooks/useChat";
import { analytics } from "./services/analytics";
import { telemetry } from "./services/telemetry";
import { webhooks } from "./services/webhooks";
import AI from "AI";
import App from "./App";
import Connected from "Connected";
import Dashboard from "./analytics/components/Dashboard";
import Desktop from "Desktop";
import Disconnected from "Disconnected";
import Learning from "Learning";
import WS from "WS";
import ZETA from "ZETA";

export default function App() {
  const { t } = useTranslation();
  const [token, setToken] = useState<string | null>(() => localStorage.getItem("zeta_token"));
  const { wsConnected } = useChat();
  const status = useMemo(() => (wsConnected ? "WS: Connected" : "WS: Disconnected"), [wsConnected]);
  const [view, setView] = useState<"dashboard" | "learning">("dashboard");

  useEffect(() => {
    telemetry.start();
    analytics.appStart();
    // register a local webhook for audit/debug if desired
    try {
      webhooks.subscribe("http://localhost:9000/webhook-debug");
    } catch {
      /* noop */
    }
  }, []);

  return (
    <Box
      sx={{
        minHeight: "100vh",
        bgcolor: "background.default",
        color: "text.primary",
      }}
    >
      <AppBar position="static" color="transparent" elevation={0}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            {t("title", "ZETA AI Desktop")}
          </Typography>
          <Chip label={status} color={wsConnected ? "success" : "default"} size="small" />
        </Toolbar>
      </AppBar>
      <Container sx={{ py: 2 }}>
        {!token ? (
          <LoginForm onLoggedIn={() => setToken(localStorage.getItem("zeta_token"))} />
        ) : (
          <>
            <Box sx={{ display: "flex", gap: 1, mb: 2 }}>
              <Button
                variant={view === "dashboard" ? "contained" : "outlined"}
                onClick={() => setView("dashboard")}
              >
                Dashboard
              </Button>
              <Button
                variant={view === "learning" ? "contained" : "outlined"}
                onClick={() => setView("learning")}
              >
                Learning
              </Button>
            </Box>
            {view === "dashboard" ? <MainDashboard /> : <LearningPanel />}
          </>
        )}
      </Container>
    </Box>
  );
}
