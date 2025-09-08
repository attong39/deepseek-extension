import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import RefreshIcon from "@mui/icons-material/Refresh";
import { AppBar, Button, Container, Grid, IconButton, Toolbar, Typography } from "@mui/material";
import { useSnackbar } from "notistack";
import { Suspense, useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

// Các panel/tiện ích trong dashboard
import { ChatPanel } from "./ChatPanel";
import { ControlPanel } from "./ControlPanel";
import { DatasetsPanel } from "./DatasetsPanel";
import { DataUploadModal } from "./DataUploadModal";
import { FeedbackPanel } from "./FeedbackPanel";
import { LanguageToggle } from "./LanguageToggle";
import { LearningPanel } from "./LearningPanel";
import { RateLimitBadge } from "./RateLimitBadge";
import { ResultsPanel } from "./ResultsPanel";
import { TrainingPanel } from "./TrainingPanel";
import AI from "AI";
import Chat from "../pages/Chat";
import CloudUpload from "CloudUpload";
import Control from "../pages/Control";
import Datasets from "Datasets";
import Desktop from "Desktop";
import Element from "Element";
import Feedback from "Feedback";
import File from "File";
import FileList from "FileList";
import Files from "Files";
import JSX from "JSX";
import Learning from "Learning";
import MUI from "MUI";
import MainDashboard from "./MainDashboard";
import Refresh from "Refresh";
import Results from "Results";
import Training from "../pages/Training";
import Upload from "Upload";
import Zeta from "Zeta";

/**
 * MainDashboard
 * - Bố cục tổng hợp: Chat/Feedback, Control/Results, Training/Learning
 * - Tương thích i18n, notistack, và MUI theo chuẩn dự án
 */
export function MainDashboard(): JSX.Element {
  const { t } = useTranslation();
  const { enqueueSnackbar } = useSnackbar();
  const [openUpload, setOpenUpload] = useState(false);

  const onOpenUpload = useCallback(() => setOpenUpload(true), []);
  const onCloseUpload = useCallback(() => setOpenUpload(false), []);
  const onUpload = useCallback(
    (files: File[]) => {
      // Gợi ý: route vào pipeline ingest ở services khi có
      const count = Array.isArray(files)
        ? files.length
        : (files as unknown as FileList)?.length || 0;
      enqueueSnackbar(t("upload_enqueued", { defaultValue: "Files enqueued", count }), {
        variant: "info",
      });
    },
    [enqueueSnackbar, t],
  );

  return (
    <>
      <AppBar position="static" elevation={0} color="transparent">
        <Toolbar>
          <Typography variant="h6" sx={{ flex: 1 }}>
            {t("app_title", "Zeta Desktop AI")}
          </Typography>
          <LanguageToggle />
          <RateLimitBadge />
          <IconButton size="small" onClick={() => window.location.reload()} aria-label="refresh">
            <RefreshIcon />
          </IconButton>
          <Button
            startIcon={<CloudUploadIcon />}
            variant="contained"
            onClick={onOpenUpload}
            sx={{ ml: 1 }}
          >
            {t("upload", "Upload")}
          </Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ py: 2 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={7} lg={8}>
            <ChatPanel />
          </Grid>
          <Grid item xs={12} md={5} lg={4}>
            <FeedbackPanel />
          </Grid>

          <Grid item xs={12} md={6}>
            <ControlPanel />
          </Grid>
          <Grid item xs={12} md={6}>
            <ResultsPanel />
          </Grid>

          <Grid item xs={12} md={6}>
            <TrainingPanel />
          </Grid>
          <Grid item xs={12} md={6}>
            <LearningPanel />
          </Grid>

          {/* Datasets smoke panel */}
          <Grid item xs={12}>
            <DatasetsPanel />
          </Grid>
        </Grid>
      </Container>

      <Suspense fallback={null}>
        <DataUploadModal open={openUpload} onClose={onCloseUpload} onUpload={onUpload} />
      </Suspense>
    </>
  );
}

export default MainDashboard;
