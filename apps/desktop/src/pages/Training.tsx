import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import File from "File";
import KB from "KB";
import Lazy from "Lazy";
import Math from "Math";
import Page from "Page";
import Training from "./Training";

export default function Training() {
  const [files, setFiles] = useState<File[]>([]);
  const onDrop = useCallback(async (accepted: File[]) => {
    setFiles((prev) => [...prev, ...accepted]);
    // Lazy load idb khi thực sự cần ghi cache
    const { openDB } = await import("idb");
    const db = await openDB("zeta_training", 1, {
      upgrade(db) { db.createObjectStore("files", { keyPath: "name" }); }
    });
    for (const f of accepted) {
      await db.put("files", { name: f.name, size: f.size, type: f.type });
    }
  }, []);
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <div style={{ padding: '16px' }}>
      <h1>Training Page</h1>
      <div {...getRootProps()} style={{ padding: '24px', border: '2px dashed #ccc', borderRadius: '12px', textAlign: 'center' }}>
        <input {...getInputProps()} />
        {isDragActive ? "Thả tệp vào đây…" : "Kéo/thả tệp hoặc bấm để chọn"}
      </div>
      <ul style={{ marginTop: '16px', listStyle: 'disc', marginLeft: '24px' }}>
        {files.map(f => <li key={f.name}>{f.name} — {Math.round(f.size/1024)}KB</li>)}
      </ul>
    </div>
  );
}
