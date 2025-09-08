import { Box, Button, Divider, TextField, Typography } from "@mui/material";
import { useMemo, useState } from "react";

import { configureSafety } from "@/services/ruleEngine";
import Capacity from "Capacity";
import Element from "Element";
import JSX from "JSX";
import Rate from "Rate";
import Refill from "Refill";
import Region from "Region";
import Safety from "Safety";
import SafetySettings from "./SafetySettings";

type Region = { x1: number; y1: number; x2: number; y2: number } | null;

const parseNum = (v: string, def = 0) => {
  const n = Number(v);
  return Number.isFinite(n) ? n : def;
};

export default function SafetySettings(): JSX.Element {
  const [region, setRegion] = useState<Region>(null);
  const [cap, setCap] = useState<string>("10");
  const [refill, setRefill] = useState<string>("10");

  const validRegion = useMemo(() => {
    if (!region) return null;
    const { x1, y1, x2, y2 } = region;
    const ok = [x1, y1, x2, y2].every((n) => Number.isFinite(n));
    return ok ? region : null;
  }, [region]);

  const onSave = () => {
    const payload: any = {};
    const capacity = parseNum(cap, 10);
    const refillPerSec = parseNum(refill, 10);
    if (Number.isFinite(capacity) && Number.isFinite(refillPerSec)) {
      payload.rate = { capacity, refillPerSec };
    }
    if (validRegion) payload.allowedRegion = validRegion;
    configureSafety(payload);
    alert("Đã cập nhật luật an toàn.");
  };

  const resetDefaults = () => {
    setRegion(null);
    setCap("10");
    setRefill("10");
    configureSafety({
      blockedShortcuts: ["alt+f4", "cmd+q", "control+q", "ctrl+q"],
      rate: { capacity: 10, refillPerSec: 10 },
    });
    alert("Đã khôi phục mặc định.");
  };

  return (
    <Box sx={{ border: "1px solid #333", borderRadius: 2, p: 2, mt: 2 }}>
      <Typography variant="h6" gutterBottom>
        Luật an toàn (Safety)
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        Giới hạn tốc độ thao tác, vùng cho phép với chuột, và chặn shortcut nguy hiểm.
      </Typography>
      <Divider sx={{ my: 1 }} />

      <Typography variant="subtitle2" gutterBottom>
        Rate limit
      </Typography>
      <Box sx={{ display: "flex", gap: 1, alignItems: "center", mb: 2 }}>
        <TextField
          size="small"
          label="Capacity"
          value={cap}
          onChange={(e) => setCap(e.target.value)}
          sx={{ width: 120 }}
          inputProps={{ inputMode: "numeric" }}
        />
        <TextField
          size="small"
          label="Refill/sec"
          value={refill}
          onChange={(e) => setRefill(e.target.value)}
          sx={{ width: 120 }}
          inputProps={{ inputMode: "numeric" }}
        />
      </Box>

      <Typography variant="subtitle2" gutterBottom>
        Vùng cho phép (mouse)
      </Typography>
      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: "repeat(4, 1fr)",
          gap: 1,
          maxWidth: 520,
        }}
      >
        <TextField
          size="small"
          label="x1"
          value={region?.x1 ?? ""}
          onChange={(e) =>
            setRegion((r) => ({
              ...(r ?? { x1: 0, y1: 0, x2: 0, y2: 0 }),
              x1: parseNum(e.target.value),
            }))
          }
          inputProps={{ inputMode: "numeric" }}
        />
        <TextField
          size="small"
          label="y1"
          value={region?.y1 ?? ""}
          onChange={(e) =>
            setRegion((r) => ({
              ...(r ?? { x1: 0, y1: 0, x2: 0, y2: 0 }),
              y1: parseNum(e.target.value),
            }))
          }
          inputProps={{ inputMode: "numeric" }}
        />
        <TextField
          size="small"
          label="x2"
          value={region?.x2 ?? ""}
          onChange={(e) =>
            setRegion((r) => ({
              ...(r ?? { x1: 0, y1: 0, x2: 0, y2: 0 }),
              x2: parseNum(e.target.value),
            }))
          }
          inputProps={{ inputMode: "numeric" }}
        />
        <TextField
          size="small"
          label="y2"
          value={region?.y2 ?? ""}
          onChange={(e) =>
            setRegion((r) => ({
              ...(r ?? { x1: 0, y1: 0, x2: 0, y2: 0 }),
              y2: parseNum(e.target.value),
            }))
          }
          inputProps={{ inputMode: "numeric" }}
        />
      </Box>

      <Box sx={{ display: "flex", gap: 1, mt: 2 }}>
        <Button variant="contained" onClick={onSave}>
          Lưu
        </Button>
        <Button variant="outlined" color="inherit" onClick={resetDefaults}>
          Mặc định
        </Button>
      </Box>
    </Box>
  );
}
