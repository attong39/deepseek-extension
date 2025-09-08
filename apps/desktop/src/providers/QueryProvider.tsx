import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactNode, useState } from "react";
import QueryProvider from "./QueryProvider";
import QueryProviderProps from "QueryProviderProps";

interface QueryProviderProps {
  children: ReactNode;
}

export function QueryProvider({ children }: QueryProviderProps) {
  const [client] = useState(() => {
    const queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: (failureCount, error: any) => {
            const status = error?.response?.status;
            // Không retry các lỗi client (4xx)
            if (status && status >= 400 && status < 500) return false;
            return failureCount < 2;
          },
          staleTime: 5 * 60 * 1000, // 5 phút
          gcTime: 10 * 60 * 1000,   // 10 phút (cacheTime renamed to gcTime in v5)
          refetchOnWindowFocus: false,
          refetchOnReconnect: true,
        },
        mutations: {
          retry: (failureCount, error: any) => {
            const status = error?.response?.status;
            // Chỉ retry server errors (5xx)
            if (status && status >= 500) return failureCount < 2;
            return false;
          },
        },
      },
    });

    return queryClient;
  });

  return (
    <QueryClientProvider client={client}>
      {children}
    </QueryClientProvider>
  );
}
