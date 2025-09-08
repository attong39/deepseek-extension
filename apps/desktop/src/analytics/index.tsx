import Dashboard from "./components/Dashboard";
import Analytics from "./index";
import AnalyticsPage from "AnalyticsPage";
import Implementation from "Implementation";
import Phase from "Phase";
import Real from "Real";

export default function AnalyticsPage() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Analytics Dashboard
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Real-time system performance metrics and monitoring
          </p>
        </div>
        
        <Dashboard />
        
        <div className="mt-8 text-center text-sm text-gray-500">
          Analytics v0.1 - Phase 1 Implementation
        </div>
      </div>
    </div>
  );
}
