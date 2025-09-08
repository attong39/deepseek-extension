import React from "react";

import { sendEmergencyStop } from "@/services/emergency";
import Confirm from "Confirm";
import Element from "Element";
import Emergency from "Emergency";
import EmergencyStop from "./EmergencyStop";
import Failed from "Failed";
import JSX from "JSX";
import Stop from "Stop";
import Stopping from "Stopping";

export function EmergencyStop(): JSX.Element {
  const [busy, setBusy] = React.useState(false);
  const onClick = async () => {
    if (!confirm("Confirm Emergency Stop?")) return;
    setBusy(true);
    try {
      await sendEmergencyStop({ reason: "user_stop" });
      alert("Emergency stop dispatched");
    } catch (e: any) {
      alert("Failed: " + String(e?.message || e));
    } finally {
      setBusy(false);
    }
  };
  return (
    <button disabled={busy} onClick={onClick} className="btn btn-danger">
      {busy ? "Stopping..." : "Emergency Stop"}
    </button>
  );
}
export default EmergencyStop;
