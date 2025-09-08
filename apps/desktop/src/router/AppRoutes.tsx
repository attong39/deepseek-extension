import { lazy, Suspense } from "react";
import { HashRouter, Navigate, Route, Routes } from "react-router-dom";

import { ErrorBoundary } from "@/components/common/ErrorBoundary";
import LoadingFallback from "@/components/common/LoadingFallback";
import AnalyticsPage from "AnalyticsPage";
import AppRoutes from "./AppRoutes";
import AutomationPage from "../automation/AutomationPage";
import ChatUpload from "../pages/ChatUpload";
import Dashboard from "../analytics/components/Dashboard";
import Lazy from "Lazy";
import Settings from "../pages/Settings";
import TrainingPanel from "../components/TrainingPanel";

// Lazy load các pages để tối ưu bundle splitting - sử dụng barrel exports
const Dashboard = lazy(() => import("@/features/dashboard/Dashboard"));
const AnalyticsPage = lazy(() => import("@/analytics"));
const AutomationPage = lazy(() => import("@/automation"));
const ChatUpload = lazy(() => import("../pages/ChatUpload"));      // giữ nếu đã có
const TrainingPanel = lazy(() => import("../pages/TrainingPanel"));    // giữ nếu đã có
const Settings = lazy(() => import("../pages/Settings"));      // giữ nếu đã có

export default function AppRoutes() {
  return (
    <HashRouter>
      <ErrorBoundary fallback={<div className="p-4 text-red-500">Lỗi router</div>}>
        <Suspense fallback={<LoadingFallback />}>
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
            <Route path="/automation" element={<AutomationPage />} />
            <Route path="/chat" element={<ChatUpload />} />
            <Route path="/training" element={<TrainingPanel />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="*" element={<div className="p-4">404 - Không tìm thấy trang</div>} />
          </Routes>
        </Suspense>
      </ErrorBoundary>
    </HashRouter>
  );
}
