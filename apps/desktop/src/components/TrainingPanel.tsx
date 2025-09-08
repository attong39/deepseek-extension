import React, { useState } from "react";

import { uploadFile } from "../services/files";
import { cancelJob, listJobs, startTraining, type TrainingJob } from "../services/training";
import AI from "AI";
import Cancel from "Cancel";
import ChangeEvent from "ChangeEvent";
import ChangeEventHandler from "ChangeEventHandler";
import File from "File";
import HTMLInputElement from "HTMLInputElement";
import HTMLTextAreaElement from "HTMLTextAreaElement";
import Jobs from "Jobs";
import Math from "Math";
import Progress from "Progress";
import Refresh from "Refresh";
import Running from "Running";
import Start from "Start";
import Status from "../pages/Status";
import Training from "../pages/Training";
import TrainingJob from "TrainingJob";
import TrainingPanel from "./TrainingPanel";
import Upload from "Upload";

export function TrainingPanel() {
  const [desc, setDesc] = useState("");
  const [files, setFiles] = useState<File[]>([]);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState<string>("idle");

  const onSelect: React.ChangeEventHandler<HTMLInputElement> = (
    e: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const list = Array.from((e.target as HTMLInputElement).files || []);
    setFiles(list);
  };

  const start = async () => {
    setStatus("uploading");
    setProgress(0);
    try {
      // Upload files trước (nếu có)
      for (const f of files) {
        await uploadFile(f);
      }
      setStatus("starting");
      // Khởi động training (payload demo)
      await startTraining({
        description: desc,
        files: files.map((f: File) => f.name),
      });
      setStatus("running");
      // cập nhật progress demo; thực tế nên poll listJobs/getJob
      let p = 0;
      const timer = setInterval(() => {
        p = Math.min(100, p + 10);
        setProgress(p);
        if (p >= 100) {
          clearInterval(timer);
          setStatus("done");
        }
      }, 300);
    } catch (e: unknown) {
      console.error("start training failed", e);
      setStatus("error");
    }
  };

  const refresh = async () => {
    try {
      const jobs: TrainingJob[] = await listJobs();
      // Gợi ý hiển thị count jobs trong status
      setStatus(`jobs:${jobs.length}`);
    } catch (e: unknown) {
      console.debug("refresh jobs failed", e);
    }
  };

  const cancelLatest = async () => {
    try {
      const jobs: TrainingJob[] = await listJobs();
      const running = jobs.find((j) => j.status === "running");
      if (running) await cancelJob(running.id);
      await refresh();
    } catch (e: unknown) {
      console.debug("cancel job failed", e);
    }
  };
  return (
    <div style={{ border: "1px solid #eee", padding: 12, borderRadius: 8 }}>
      <h3>Training</h3>
      <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        <textarea
          placeholder="Mô tả yêu cầu AI học..."
          value={desc}
          onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setDesc(e.target.value)}
        />
        <input type="file" multiple onChange={onSelect} />
        {files.length > 0 && (
          <ul style={{ margin: 0, paddingLeft: 18 }}>
            {files.map((f: File) => (
              <li key={f.name}>{f.name}</li>
            ))}
          </ul>
        )}
      </div>
      <div style={{ marginTop: 8 }}>
        <button onClick={start} disabled={status === "uploading"}>
          Start
        </button>
        <span style={{ marginLeft: 8 }}>Progress: {progress}%</span>
        <span style={{ marginLeft: 8 }}>Status: {status}</span>
        <button style={{ marginLeft: 8 }} onClick={refresh}>
          Refresh Jobs
        </button>
        <button style={{ marginLeft: 8 }} onClick={cancelLatest}>
          Cancel Running
        </button>
      </div>
    </div>
  );
}
