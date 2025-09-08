import {
  Button,
  Checkbox,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControlLabel,
  Typography,
} from "@mui/material";
import { useState } from "react";
import { useTranslation } from "react-i18next";
import Allow from "Allow";
import Capability from "Capability";
import Deny from "Deny";
import Element from "Element";
import Grant from "Grant";
import JSX from "JSX";
import MUI from "MUI";
import Permission from "Permission";
import PermissionDialog from "./PermissionDialog";
import Props from "Props";
import Readonly from "Readonly";
import Remember from "Remember";

type Capability = "screen" | "keyboard" | "mouse" | "audio" | "camera";

type Props = Readonly<{
  open: boolean;
  capability: Capability;
  description?: string;
  onGrant: (remember: boolean) => void;
  onDeny: () => void;
}>;

/**
 * PermissionDialog
 * Hộp thoại xin quyền truy cập (screen/keyboard/mouse/audio/camera) chuẩn MUI + i18n.
 */
export function PermissionDialog({
  open,
  capability,
  description,
  onGrant,
  onDeny,
}: Props): JSX.Element | null {
  const { t } = useTranslation();
  const [remember, setRemember] = useState(true);

  if (!open) return null;

  const title = t("permission.title", "Grant Permission");
  const desc =
    description || t("permission.allow", "Allow access to {{capability}}?", { capability });
  const rememberLabel = t("permission.remember", "Remember for this session");
  const denyText = t("permission.deny", "Deny");
  const allowText = t("permission.allow_btn", "Allow");

  return (
    <Dialog open={open} onClose={onDeny} maxWidth="xs" fullWidth>
      <DialogTitle>{title}</DialogTitle>
      <DialogContent>
        <Typography variant="body2" sx={{ mb: 1 }}>
          {desc}
        </Typography>
        <FormControlLabel
          control={<Checkbox checked={remember} onChange={(e) => setRemember(e.target.checked)} />}
          label={rememberLabel}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onDeny}>{denyText}</Button>
        <Button variant="contained" onClick={() => onGrant(remember)}>
          {allowText}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default PermissionDialog;
