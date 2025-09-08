import Error from "Error";
import IPC from "IPC";
import Uint8Array from "Uint8Array";
export async function saveTempPng(bytes: Uint8Array): Promise<string> {
  if (!(window as any).zeta?.file?.writeTemp) throw new Error("writeTemp IPC not available");
  const res = await (window as any).zeta.file.writeTemp(Array.from(bytes), ".png");
  if (!res?.ok || !res?.path) throw new Error(String(res?.error || "writeTemp failed"));
  return String(res.path);
}
