import { useEffect, useState } from "react";
import LoadingFallback from "./LoadingFallback";
import LoadingFallbackProps from "LoadingFallbackProps";
import Timeout from "Timeout";
import Vui from "Vui";

interface LoadingFallbackProps {
  message?: string;
  timeout?: number;
}

export default function LoadingFallback({ 
  message = "Đang tải...", 
  timeout = 10000 
}: LoadingFallbackProps) {
  const [isTimeout, setIsTimeout] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsTimeout(true);
    }, timeout);

    return () => clearTimeout(timer);
  }, [timeout]);

  if (isTimeout) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div className="text-center">
          <div className="text-red-500 text-lg mb-2">⚠️ Timeout</div>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            Tải trang quá lâu. Vui lòng thử lại.
          </p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            Tải lại
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
      <div className="text-center">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mb-4"></div>
        <p className="text-gray-600 dark:text-gray-400">{message}</p>
      </div>
    </div>
  );
}
