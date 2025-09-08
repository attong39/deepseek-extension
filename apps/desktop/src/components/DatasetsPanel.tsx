import RefreshIcon from "@mui/icons-material/Refresh";
import {
  Card,
  CardContent,
  CardHeader,
  Divider,
  IconButton,
  List,
  ListItem,
  ListItemText,
  Typography,
} from "@mui/material";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";

import { listFiles, type FileItem } from "../services/files";
import BE from "BE";
import DatasetInfo from "DatasetInfo";
import Datasets from "Datasets";
import DatasetsPanel from "./DatasetsPanel";
import Failed from "Failed";
import FileItem from "FileItem";
import Loading from "Loading";
import Map from "Map";
import Minimal from "Minimal";
import No from "No";
import OpenAPI from "OpenAPI";
import Refresh from "Refresh";
import Size from "Size";
import Unknown from "Unknown";

// Minimal type aligned with OpenAPI schema for display
type DatasetInfo = FileItem & {
  description?: string | null;
  created_at?: string | null;
};

export function DatasetsPanel() {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const q = useQuery({
    queryKey: ["datasets"],
    queryFn: async (): Promise<DatasetInfo[]> => {
      // Ưu tiên service mỏng mới tạo (đọc từ /files) để đồng bộ BE v1/files
      const items = await listFiles();
      // Map nhẹ sang DatasetInfo nếu cần; tránh gán undefined cho optional prop
      return items.map(
        (f): DatasetInfo => ({
          id: f.id,
          name: f.name,
          size: f.size,
          created_at: f.createdAt ?? null,
          description: null,
          ...(f.contentType ? { contentType: f.contentType } : {}),
        }),
      );
    },
  });

  const onRefresh = () => {
    queryClient.invalidateQueries({ queryKey: ["datasets"] });
  };

  const formatSecondary = (d: DatasetInfo): string | undefined => {
    const parts: string[] = [];
    if (d.description) parts.push(d.description);
    if (typeof d.size === "number")
      parts.push(`${t("datasets.size", "Size")}: ${d.size.toLocaleString()}`);
    if (d.created_at) {
      let ts = "";
      try {
        ts = new Date(d.created_at).toLocaleString();
      } catch {
        ts = String(d.created_at);
      }
      parts.push(ts);
    }
    return parts.length ? parts.join(" • ") : undefined;
  };

  return (
    <Card variant="outlined">
      <CardHeader
        title={<Typography variant="h6">{t("datasets.title", "Datasets")}</Typography>}
        action={
          <IconButton aria-label="refresh" onClick={onRefresh} disabled={q.isFetching} size="small">
            <RefreshIcon fontSize="small" />
          </IconButton>
        }
      />
      <CardContent>
        {q.isLoading && <Typography>{t("loading", "Loading...")}</Typography>}
        {q.isError && (
          <Typography color="error">{t("error.load", "Failed to load datasets")}</Typography>
        )}
        {q.data && q.data.length === 0 && (
          <Typography>{t("datasets.empty", "No datasets")}</Typography>
        )}
        {q.data && q.data.length > 0 && (
          <List dense>
            {q.data.map((d: DatasetInfo, idx: number) => (
              <>
                <ListItem key={d.id ?? String(idx)}>
                  <ListItemText
                    primary={d.name ?? d.id ?? t("datasets.unknown", "Unknown")}
                    secondary={formatSecondary(d)}
                  />
                </ListItem>
                {idx < q.data.length - 1 && <Divider component="li" />}
              </>
            ))}
          </List>
        )}
      </CardContent>
    </Card>
  );
}
