import React, { useRef } from "react";

import { uploadFile } from "../services/files";
import ChangeEvent from "ChangeEvent";
import Close from "Close";
import Data from "Data";
import DataUploadModal from "./DataUploadModal";
import Fallback from "Fallback";
import File from "File";
import HTMLInputElement from "HTMLInputElement";
import Props from "Props";
import Readonly from "Readonly";
import UI from "../UI/index";
import Upload from "Upload";

type Props = Readonly<{
  open: boolean;
  onClose: () => void;
  onUpload?: (files: File[]) => void;
}>;

export function DataUploadModal({ open, onClose, onUpload }: Props) {
  const pickedRef = useRef<File[]>([]);
  const onPick = (e: React.ChangeEvent<HTMLInputElement>) => {
    pickedRef.current = Array.from(e.target.files || []);
  };
  const doUpload = async () => {
    const files = pickedRef.current;
    if (files.length === 0) return onClose();
    try {
      if (onUpload) {
        onUpload(files);
      } else {
        // Fallback: tự upload nếu không truyền onUpload
        await Promise.all(files.map((f: File) => uploadFile(f)));
      }
    } catch (e) {
      // Giữ tối giản: không đổi UI framework hiện tại
      console.error("Upload failed", e);
      try {
        alert("Upload thất bại");
      } catch {}
    } finally {
      onClose();
    }
  };
  if (!open) return null;
  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.35)" }}>
      <div
        style={{
          background: "#fff",
          maxWidth: 520,
          margin: "10% auto",
          padding: 16,
          borderRadius: 8,
        }}
      >
        <h3>Upload Data</h3>
        <p style={{ marginTop: 0, color: "#555" }}>
          Hỗ trợ: hình ảnh, video, âm thanh, tài liệu văn bản
        </p>
        <input
          type="file"
          multiple
          onChange={onPick}
          accept="image/*,video/*,audio/*,.txt,.md,.pdf,.doc,.docx"
        />
        <div style={{ marginTop: 8 }}>
          <button onClick={doUpload} style={{ marginRight: 8 }}>
            Upload
          </button>
          <button onClick={onClose}>Close</button>
        </div>
      </div>
    </div>
  );
}
