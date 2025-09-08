import { useEffect, useState } from "react";
import Downloading from "Downloading";
import Install from "Install";
import Math from "Math";
import Restart from "Restart";
import Update from "Update";
import UpdateBanner from "./UpdateBanner";

export default function UpdateBanner() {
  const [available, setAvailable] = useState<any>(null);
  const [progress, setProgress] = useState<number | null>(null);
  const [downloaded, setDownloaded] = useState<any>(null);

  useEffect(() => {
    if (!(window as any).zeta?.update) return;
    const unsubA = (window as any).zeta.update.onAvailable((info: any) => setAvailable(info));
    const unsubP = (window as any).zeta.update.onProgress((p: any) =>
      setProgress(p.percent ?? null),
    );
    const unsubD = (window as any).zeta.update.onDownloaded((info: any) => setDownloaded(info));
    return () => {
      try {
        unsubA();
      } catch {}
      try {
        unsubP();
      } catch {}
      try {
        unsubD();
      } catch {}
    };
  }, []);

  if (!available && !downloaded) return null;
  return (
    <div
      style={{
        position: "fixed",
        right: 16,
        bottom: 16,
        background: "#fff",
        padding: 12,
        border: "1px solid #ddd",
        borderRadius: 8,
      }}
    >
      <div style={{ marginBottom: 8 }}>{downloaded ? "Update ready" : "Update available"}</div>
      {progress != null && (
        <div style={{ marginBottom: 8 }}>Downloading: {Math.round(progress)}%</div>
      )}
      {downloaded ? (
        <button onClick={() => (window as any).zeta.update.install()}>Install & Restart</button>
      ) : (
        <div>Downloading in background…</div>
      )}
    </div>
  );
}
