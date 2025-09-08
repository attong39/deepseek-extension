import { Component, ReactNode } from "react";
import Chi from "Chi";
import ERROR from "ERROR";
import Error from "Error";
import ErrorBoundary from "./ErrorBoundary";
import M12 from "M12";
import Props from "Props";
import State from "State";
import TODO from "TODO";
import UI from "../../UI/index";
import Vui from "Vui";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  override state: State = { hasError: false };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  override componentDidCatch(error: Error, errorInfo: any) {
    console.error("[UI-ERROR]", error, errorInfo);
    
    // TODO: Gửi error lên analytics service nếu có
    // if (window.zeta?.analytics?.trackError) {
    //   window.zeta.analytics.trackError(error.message, {
    //     stack: error.stack,
    //     componentStack: errorInfo.componentStack,
    //   });
    // }
  }

  override render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
          <div className="max-w-md w-full bg-white dark:bg-gray-800 shadow-lg rounded-lg p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <svg className="h-6 w-6 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800 dark:text-red-200">
                  Đã xảy ra lỗi
                </h3>
                <div className="mt-2 text-sm text-red-700 dark:text-red-300">
                  <p>Ứng dụng gặp lỗi không mong muốn. Vui lòng thử lại.</p>
                  {this.state.error && (
                    <details className="mt-2">
                      <summary className="cursor-pointer">Chi tiết lỗi</summary>
                      <pre className="mt-2 text-xs whitespace-pre-wrap bg-gray-100 dark:bg-gray-700 p-2 rounded">
                        {this.state.error.message}
                      </pre>
                    </details>
                  )}
                </div>
                <div className="mt-4">
                  <button
                    type="button"
                    className="bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 px-3 py-2 rounded-md text-sm font-medium hover:bg-red-200 dark:hover:bg-red-800 transition-colors"
                    onClick={() => window.location.reload()}
                  >
                    Tải lại ứng dụng
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
