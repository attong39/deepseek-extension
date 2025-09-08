import { useState } from "react";

import { BUILD_INFO } from "@/services/buildInfo";
import { getHealth } from "@/services/health";
import AI from "AI";
import AboutModal from "./AboutModal";
import Assistant from "Assistant";
import Build from "Build";
import Commit from "Commit";
import Copy from "Copy";
import Desktop from "Desktop";
import Platform from "Platform";
import Props from "Props";
import Training from "../../pages/Training";
import ZETA from "ZETA";

type Props = { onClose: () => void };

export default function AboutModal({ onClose }: Props) {
  const { version, gitSha, buildTime, platform } = BUILD_INFO;
  const [copied, setCopied] = useState<null | string>(null);

  async function copyDiag() {
    const h = await getHealth();
    const payload = {
      version, gitSha, buildTime, platform, health: h,
    };
    await navigator.clipboard.writeText(JSON.stringify(payload, null, 2));
    setCopied("Đã copy diagnostics");
    setTimeout(() => setCopied(null), 2000);
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-zinc-900 p-6 rounded-2xl w-[480px] shadow-xl border border-zinc-700">
        <div className="text-center mb-4">
          <h2 className="text-xl font-semibold text-white">ZETA Desktop</h2>
          <p className="text-zinc-400 mt-1">AI Assistant & Training Platform</p>
        </div>
        
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-zinc-400">Phiên bản:</span>
            <span className="text-white font-mono">{version}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-zinc-400">Commit:</span>
            <span className="text-white font-mono">{gitSha}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-zinc-400">Build time:</span>
            <span className="text-white font-mono text-xs">{buildTime}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-zinc-400">Nền tảng:</span>
            <span className="text-white text-xs truncate max-w-[280px]">{platform}</span>
          </div>
        </div>
        
        <div className="mt-6 flex gap-2">
          <button 
            className="px-4 py-2 rounded-lg bg-zinc-800 text-white hover:bg-zinc-700 transition-colors"
            onClick={copyDiag}
          >
            Copy diagnostics
          </button>
          {copied && <span className="text-xs text-emerald-400 self-center">{copied}</span>}
          <button 
            className="ml-auto px-4 py-2 rounded-lg bg-zinc-800 text-white hover:bg-zinc-700 transition-colors"
            onClick={onClose}
          >
            Đóng
          </button>
        </div>
      </div>
    </div>
  );
}
