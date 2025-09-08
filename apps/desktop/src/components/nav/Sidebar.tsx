import { useTranslation } from "react-i18next";
import { NavLink } from "react-router-dom";
import AI from "AI";
import Assistant from "Assistant";
import Connected from "Connected";
import Connection from "Connection";
import Datasets from "Datasets";
import Desktop from "Desktop";
import Logs from "../../pages/Logs";
import Sidebar from "./Sidebar";
import Status from "../../pages/Status";
import ZETA from "ZETA";

const linkBase =
  "flex items-center px-3 py-2 rounded-lg transition-colors hover:bg-zinc-800";
const active = "bg-zinc-800 text-white";
const idle = "text-zinc-300 hover:text-white";

export function Sidebar() {
  const { t } = useTranslation();

  const navigationItems = [
    { to: "/dashboard", icon: "🏠", label: t("nav.dashboard") },
    { to: "/chat", icon: "💬", label: t("nav.chat") },
    { to: "/training", icon: "🧠", label: t("nav.training") },
    { to: "/datasets", icon: "📊", label: "Datasets" },
    { to: "/settings", icon: "⚙️", label: t("nav.settings") },
    { to: "/logs", icon: "📋", label: "Logs" },
  ];

  const renderNavItem = (to: string, icon: string, label: string) => (
    <NavLink
      key={to}
      to={to}
      className={({ isActive }) =>
        `${linkBase} ${isActive ? active : idle}`
      }
    >
      <span className="mr-3 text-lg">{icon}</span>
      <span className="flex-1">{label}</span>
    </NavLink>
  );

  return (
    <aside className="w-56 h-full bg-zinc-900 border-r border-zinc-800">
      <div className="p-4">
        <div className="mb-8">
          <h1 className="text-white text-xl font-bold">ZETA AI</h1>
          <p className="text-zinc-400 text-sm">Desktop Assistant</p>
        </div>
        
        <nav className="space-y-1">
          {navigationItems.map(item => 
            renderNavItem(item.to, item.icon, item.label)
          )}
        </nav>

        {/* Connection Status */}
        <div className="mt-8 pt-4 border-t border-zinc-800">
          <div className="flex items-center text-xs text-zinc-400">
            <div className="w-2 h-2 rounded-full bg-green-500 mr-2"></div>
            <span>Connected</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
