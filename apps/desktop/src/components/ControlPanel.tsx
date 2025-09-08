// jsx runtime from tsconfig (react-jsx)
import {
  Button,
  Card,
  CardContent,
  CardHeader,
  Checkbox,
  FormControlLabel,
  Grid,
  TextField,
  Typography,
} from "@mui/material";
import { useSnackbar } from "notistack";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { HashRouter, NavLink, Link, Routes, Route } from "react-router-dom";

import { executeAction, executeAppShortcut, panicMode } from "../controllers/inputController";
import { useVoice } from "../hooks/useVoice";
import {
  handleServerCommand,
  resetEmergencyStop,
  setCurrentBatchId,
} from "../services/commandHandler";
import { ingestText, ingestUrls } from "../services/learningRouter";
import { hasPermission, requestPermission } from "../services/permissionManager";
import { captureScreen } from "../services/screenCapture";
import { saveTempPng } from "../utils/fs";
import { ocrImage } from "../utils/ocr";

import EmergencyStop from "@/components/EmergencyStop";
import { actionQueue } from "@/services/actionQueue";
import Allow from "Allow";
import Alt from "Alt";
import App from "../App";
import Audio from "Audio";
import Batch from "Batch";
import Camera from "Camera";
import Cho from "Cho";
import Clear from "Clear";
import Control from "../pages/Control";
import ControlPanel from "./ControlPanel";
import Ctrl from "Ctrl";
import Dataset from "Dataset";
import Emergency from "Emergency";
import Enable from "Enable";
import Error from "Error";
import Free from "Free";
import Hello from "Hello";
import ID from "ID";
import IPC from "IPC";
import Ingest from "Ingest";
import InputProps from "InputProps";
import Keyboard from "Keyboard";
import Learning from "Learning";
import MAX_TEXT from "MAX_TEXT";
import Mouse from "Mouse";
import OCR from "OCR";
import Paddle from "Paddle";
import PaddleOCR from "PaddleOCR";
import Panel from "Panel";
import Panic from "Panic";
import Parameters from "Parameters";
import Photoshop from "Photoshop";
import Prefer from "Prefer";
import Queue from "Queue";
import Resume from "Resume";
import S from "S";
import STT from "STT";
import Screen from "Screen";
import Search from "Search";
import Send from "Send";
import Shortcut from "Shortcut";
import Speech from "Speech";
import Start from "Start";
import Stop from "Stop";
import Submitting from "Submitting";
import Text from "Text";
import Toggles from "Toggles";
import Transcript from "Transcript";
import URL from "URL";
import URLs from "URLs";
import Uint8Array from "Uint8Array";
import Wiki from "Wiki";
import Wikipedia from "Wikipedia";
import ZETA from "ZETA";

export function ControlPanel() {
  const { t } = useTranslation();
  const { enqueueSnackbar } = useSnackbar();
  // Learning mini-form state
  const [urlsInput, setUrlsInput] = useState("");
  const [textInput, setTextInput] = useState("");
  const [dataset, setDataset] = useState("");
  const [submittingUrls, setSubmittingUrls] = useState(false);
  const [submittingText, setSubmittingText] = useState(false);
  const MAX_TEXT = 8000;
  // Toggles
  const [enableLearning, setEnableLearning] = useState<boolean>(() => {
    try {
      return localStorage.getItem("zeta_enable_learning") !== "0";
    } catch {
      return true;
    }
  });
  const [enableAppCtl, setEnableAppCtl] = useState<boolean>(() => {
    try {
      return localStorage.getItem("zeta_enable_appctl") !== "0";
    } catch {
      return true;
    }
  });
  const [enableBatchQueue, setEnableBatchQueue] = useState<boolean>(() => {
    try {
      return localStorage.getItem("zeta_enable_batch_queue") === "1";
    } catch {
      return false;
    }
  });
  useEffect(() => {
    try {
      localStorage.setItem("zeta_enable_learning", enableLearning ? "1" : "0");
    } catch {
      /* noop */
    }
  }, [enableLearning]);
  useEffect(() => {
    try {
      localStorage.setItem("zeta_enable_appctl", enableAppCtl ? "1" : "0");
    } catch {
      /* noop */
    }
  }, [enableAppCtl]);
  useEffect(() => {
    try {
      localStorage.setItem("zeta_enable_batch_queue", enableBatchQueue ? "1" : "0");
    } catch {
      /* noop */
    }
  }, [enableBatchQueue]);
  useEffect(() => {
    // Bật/tắt hàng đợi tác vụ theo toggle
    try {
      if (enableBatchQueue) actionQueue.enable();
      else actionQueue.disable();
    } catch {
      /* noop */
    }
  }, [enableBatchQueue]);
  // App shortcut form
  const [appName, setAppName] = useState("Photoshop");
  const [shortcut, setShortcut] = useState("Ctrl+Alt+S");
  const [panic, setPanic] = useState(false);
  const [batchId, setBatchId] = useState<string>("");
  const [queueSize, setQueueSize] = useState<number>(() => actionQueue.size());
  const voice = useVoice();
  const [transcript, setTranscript] = useState("");
  useEffect(() => {
    setTranscript(voice.transcript);
  }, [voice.transcript]);
  useEffect(() => {
    const off = actionQueue.subscribe((s) => setQueueSize(s));
    return () => {
      off();
    };
  }, []);

  const isValidUrl = (s: string): boolean => {
    try {
      const u = new URL(s);
      return u.protocol === "http:" || u.protocol === "https:";
    } catch {
      return false;
    }
  };
  const permDesc = (p: Parameters<typeof hasPermission>[0]): string => {
    switch (p) {
      case "screen":
        return t(
          "permission.desc.screen",
          "Cho phép truy cập màn hình để chụp ảnh phục vụ OCR/ghi chú.",
        );
      case "keyboard":
        return t(
          "permission.desc.keyboard",
          "Cho phép gửi tổ hợp phím để tự động hóa thao tác ứng dụng.",
        );
      case "mouse":
        return t("permission.desc.mouse", "Cho phép click/di chuyển chuột cho các tác vụ tự động.");
      case "audio":
        return t("permission.desc.audio", "Cho phép truy cập micro để nhận diện giọng nói (STT).");
      case "camera":
        return t("permission.desc.camera", "Cho phép truy cập camera cho các tính năng thị giác.");
      default:
        return t("permission.allow", "Allow access to {{capability}}?", {
          capability: p as string,
        });
    }
  };

  const check = async (p: Parameters<typeof hasPermission>[0]) => {
    if (!hasPermission(p)) await requestPermission(p, permDesc(p));
    enqueueSnackbar(`${p}: ${hasPermission(p) ? "granted" : "denied"}`, {
      variant: hasPermission(p) ? "success" : "warning",
    });
  };
  const ensure = async (perm: Parameters<typeof hasPermission>[0]) => {
    if (!hasPermission(perm)) {
      const ok = await requestPermission(perm, permDesc(perm));
      if (!ok) return false;
    }
    return true;
  };

  const onScreen = async () => {
    if (!(await ensure("screen"))) return;
    const blob = await captureScreen();
    if (!blob) {
      enqueueSnackbar(t("error.capture", "Không chụp được màn hình"), {
        variant: "error",
      });
      return;
    }
    try {
      // Prefer IPC PaddleOCR if available
      const asFile = await (async () => {
        const buf = await blob.arrayBuffer();
        const tmpPath = await saveTempPng(new Uint8Array(buf));
        return tmpPath;
      })();
      if (window.zeta?.ocr?.paddle) {
        const r = await window.zeta.ocr.paddle(asFile);
        if (r?.ok && r.text) {
          enqueueSnackbar(t("ocr.paddle.ok", "OCR (Paddle) thành công"), {
            variant: "success",
          });
          return;
        }
      }
      // fallback tesseract
      await ocrImage(blob, "vie");
      enqueueSnackbar(t("ocr.tesseract.ok", "OCR (tesseract) thành công"), {
        variant: "success",
      });
    } catch (e) {
      enqueueSnackbar(t("ocr.fail", "OCR thất bại: {{msg}}", { msg: (e as Error).message }), {
        variant: "error",
      });
    }
  };

  const onKeyboard = async () => {
    if (!(await ensure("keyboard"))) return;
    executeAction({ type: "type_text", payload: { text: "Hello from ZETA" } });
  };

  const onMouse = async () => {
    if (!(await ensure("mouse"))) return;
    executeAction({ type: "click", payload: { button: "left" } });
  };

  const onWiki = async () => {
    const q = window.prompt(t("wiki.prompt", "Wikipedia query?"))?.trim();
    if (!q) return;
    handleServerCommand({ type: "wiki.search", payload: { query: q } });
    enqueueSnackbar(t("wiki.sent", "Đã gửi yêu cầu Wikipedia"), {
      variant: "info",
    });
  };

  const onArXiv = async () => {
    const q = window.prompt(t("arxiv.prompt", "arXiv query?"))?.trim();
    if (!q) return;
    handleServerCommand({
      type: "arxiv.search",
      payload: { query: q, maxResults: 5 },
    });
    enqueueSnackbar(t("arxiv.sent", "Đã gửi yêu cầu arXiv"), {
      variant: "info",
    });
  };

  const onIngestUrls = async () => {
    const tokens = urlsInput
      .split(/[\s,;]+/)
      .map((s: string) => s.trim())
      .filter(Boolean);
    if (tokens.length === 0) return;
    const invalid = tokens.filter((t: string) => !isValidUrl(t));
    if (invalid.length) {
      enqueueSnackbar(t("urls.invalid", "URL không hợp lệ"), {
        variant: "warning",
      });
      return;
    }
    try {
      setSubmittingUrls(true);
      await ingestUrls(tokens, dataset ? { dataset } : undefined);
      enqueueSnackbar(t("ingest.urls.ok", "Đã gửi yêu cầu ingest URLs"), {
        variant: "success",
      });
    } catch (e) {
      enqueueSnackbar(
        t("ingest.urls.fail", "Ingest URLs lỗi: {{msg}}", {
          msg: (e as Error).message,
        }),
        { variant: "error" },
      );
    } finally {
      setSubmittingUrls(false);
    }
  };

  const onIngestText = async () => {
    const txt = textInput.trim();
    if (!txt) return;
    if (txt.length > MAX_TEXT) {
      enqueueSnackbar(t("ingest.text.tooLong", "Text quá dài"), {
        variant: "warning",
      });
      return;
    }
    try {
      setSubmittingText(true);
      await ingestText(txt, dataset ? { dataset } : undefined);
      enqueueSnackbar(t("ingest.text.ok", "Đã gửi yêu cầu ingest text"), {
        variant: "success",
      });
    } catch (e) {
      enqueueSnackbar(
        t("ingest.text.fail", "Ingest text lỗi: {{msg}}", {
          msg: (e as Error).message,
        }),
        { variant: "error" },
      );
    } finally {
      setSubmittingText(false);
    }
  };

  const onSendShortcut = async () => {
    const app = appName.trim();
    const sc = shortcut.trim();
    if (!app || !sc) return;
    try {
      const ok = await executeAppShortcut(app, sc);
      enqueueSnackbar(
        ok ? t("shortcut.ok", "Đã gửi shortcut") : t("shortcut.rejected", "Shortcut bị từ chối"),
        { variant: ok ? "success" : "warning" },
      );
    } catch (e) {
      enqueueSnackbar(
        t("shortcut.fail", "Shortcut lỗi: {{msg}}", {
          msg: (e as Error).message,
        }),
        { variant: "error" },
      );
    }
  };

  const onTogglePanic = async () => {
    const next = !panic;
    const ok = await panicMode(next);
    if (ok) setPanic(next);
  };

  return (
    <Card variant="outlined">
      <CardHeader
        title={<Typography variant="h6">Control Panel</Typography>}
        action={
          <Typography variant="caption" color="text.secondary">
            {t("batch.active", "Batch:")} {batchId || "-"}
          </Typography>
        }
      />
      <CardContent>
        <Grid container spacing={2}>
          <Grid item xs={12} md={12} lg={12}>
            <Grid container spacing={1} alignItems="center">
              <Grid item>
                <Button onClick={() => void onScreen()}>{t("btn.screen", "Screen")}</Button>
              </Grid>
              <Grid item>
                <Button onClick={() => void onKeyboard()}>{t("btn.keyboard", "Keyboard")}</Button>
              </Grid>
              <Grid item>
                <Button onClick={() => void onMouse()}>{t("btn.mouse", "Mouse")}</Button>
              </Grid>
              <Grid item>
                <Button onClick={() => void onWiki()}>{t("btn.wiki", "Wiki Search")}</Button>
              </Grid>
              <Grid item>
                <Button onClick={() => void onArXiv()}>{t("btn.arxiv", "arXiv Search")}</Button>
              </Grid>
              <Grid item>
                <Button onClick={() => void check("audio")}>{t("btn.audio", "Audio")}</Button>
              </Grid>
              <Grid item>
                <Button onClick={() => void check("camera")}>{t("btn.camera", "Camera")}</Button>
              </Grid>
              <Grid item xs>
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={enableLearning}
                      onChange={(e) => setEnableLearning(e.target.checked)}
                    />
                  }
                  label={t("toggle.learning", "Enable Learning")}
                />
              </Grid>
              <Grid item>
                <Typography variant="body2" color="text.secondary">
                  {t("queue.size", "Queue:")} {queueSize}
                </Typography>
              </Grid>
              <Grid item>
                <Button
                  size="small"
                  variant="outlined"
                  onClick={() => {
                    actionQueue.clear();
                    enqueueSnackbar(t("queue.cleared", "Queue cleared"), {
                      variant: "info",
                    });
                  }}
                  disabled={!enableBatchQueue || queueSize === 0}
                >
                  {t("queue.clear", "Clear")}
                </Button>
              </Grid>
              <Grid item>
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={enableBatchQueue}
                      onChange={(e) => setEnableBatchQueue(e.target.checked)}
                    />
                  }
                  label={t("toggle.batch", "Batch mode (queue)")}
                />
              </Grid>
              <Grid item>
                <EmergencyStop />
              </Grid>
              <Grid item>
                <Button
                  onClick={() => {
                    resetEmergencyStop();
                    enqueueSnackbar(t("emergency.resume", "Đã reset trạng thái Emergency Stop"), {
                      variant: "info",
                    });
                  }}
                >
                  {t("emergency.resume.btn", "Resume")}
                </Button>
              </Grid>
              <Grid item>
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={enableAppCtl}
                      onChange={(e) => setEnableAppCtl(e.target.checked)}
                    />
                  }
                  label={t("toggle.appctl", "Enable App Control")}
                />
              </Grid>
              <Grid item>
                <FormControlLabel
                  control={<Checkbox checked={panic} onChange={() => void onTogglePanic()} />}
                  label={t("toggle.panic", "Panic/Stop")}
                />
              </Grid>
            </Grid>
          </Grid>

          <Grid item xs={12}>
            <Typography variant="subtitle1" gutterBottom>
              {t("stt.title", "Speech-to-Text")}
            </Typography>
            <Grid container spacing={1} alignItems="center">
              <Grid item>
                <Button onClick={() => voice.start()} disabled={voice.listening}>
                  {t("btn.start", "Start")}
                </Button>
              </Grid>
              <Grid item>
                <Button onClick={() => voice.stop()} disabled={!voice.listening}>
                  {t("btn.stop", "Stop")}
                </Button>
              </Grid>
              {voice.error && (
                <Grid item>
                  <Typography color="error">{voice.error}</Typography>
                </Grid>
              )}
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  minRows={3}
                  value={transcript}
                  placeholder={t("stt.transcript", "Transcript...")}
                  InputProps={{ readOnly: true }}
                />
              </Grid>
            </Grid>
          </Grid>

          <Grid item xs={12}>
            <Typography variant="subtitle1" gutterBottom>
              {t("learning.title", "Learning")}
            </Typography>
            <Grid container spacing={1}>
              <Grid item xs={12} md={4}>
                <TextField
                  label={t("batch.id", "Batch ID (optional)")}
                  value={batchId}
                  onChange={(e) => {
                    const v = e.target.value;
                    setBatchId(v);
                    setCurrentBatchId(v || null);
                  }}
                  fullWidth
                />
              </Grid>
              <Grid item xs={12} md={4}>
                <TextField
                  label={t("learning.dataset", "Dataset (optional)")}
                  value={dataset}
                  onChange={(e) => setDataset(e.target.value)}
                  fullWidth
                  disabled={!enableLearning}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label={t("learning.urls", "URLs (comma/space/newline separated)")}
                  value={urlsInput}
                  onChange={(e) => setUrlsInput(e.target.value)}
                  fullWidth
                  multiline
                  minRows={3}
                  disabled={!enableLearning}
                />
                <Button
                  sx={{ mt: 1 }}
                  onClick={() => void onIngestUrls()}
                  disabled={submittingUrls || !enableLearning}
                >
                  {submittingUrls
                    ? t("btn.submitting", "Submitting…")
                    : t("btn.ingestUrls", "Ingest URLs")}
                </Button>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label={t("learning.text", "Free text to ingest")}
                  value={textInput}
                  onChange={(e) => setTextInput(e.target.value)}
                  fullWidth
                  multiline
                  minRows={3}
                  disabled={!enableLearning}
                />
                <Button
                  sx={{ mt: 1 }}
                  onClick={() => void onIngestText()}
                  disabled={submittingText || !enableLearning}
                >
                  {submittingText
                    ? t("btn.submitting", "Submitting…")
                    : t("btn.ingestText", "Ingest Text")}
                </Button>
              </Grid>
            </Grid>
          </Grid>

          <Grid item xs={12}>
            <Typography variant="subtitle1" gutterBottom>
              {t("appctl.title", "App Control")}
            </Typography>
            <Grid container spacing={1} alignItems="center">
              <Grid item xs={12} md={4}>
                <TextField
                  label={t("appctl.app", "App name (e.g., Photoshop)")}
                  value={appName}
                  onChange={(e) => setAppName(e.target.value)}
                  fullWidth
                  disabled={!enableAppCtl}
                />
              </Grid>
              <Grid item xs={12} md={4}>
                <TextField
                  label={t("appctl.shortcut", "Shortcut (e.g., Ctrl+Alt+S)")}
                  value={shortcut}
                  onChange={(e) => setShortcut(e.target.value)}
                  fullWidth
                  disabled={!enableAppCtl}
                />
              </Grid>
              <Grid item>
                <Button onClick={() => void onSendShortcut()} disabled={!enableAppCtl}>
                  {t("btn.sendShortcut", "Send Shortcut")}
                </Button>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
}
