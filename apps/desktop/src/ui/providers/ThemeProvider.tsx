/**
 * ThemeProvider - React Context Provider cho Theme System
 * Provides theme context throughout the application
 */

import React, { createContext, useContext, type ReactNode } from 'react';

import { useTheme, type UseThemeReturn } from '../hooks/useTheme';
import App from "../../App";
import CSS from "CSS";
import Context from "../../Context/index";
import Error from "Error";
import FC from "FC";
import Features from "../../Features/index";
import Hook from "Hook";
import Local from "Local";
import Props from "Props";
import Provider from "Provider";
import Provides from "Provides";
import Re from "Re";
import ReactNode from "ReactNode";
import System from "System";
import Theme from "Theme";
import ThemeContext from "ThemeContext";
import ThemeProvider from "./ThemeProvider";
import ThemeProviderProps from "ThemeProviderProps";
import Usage from "Usage";
import UseThemeReturn from "UseThemeReturn";

// Theme Context
const ThemeContext = createContext<UseThemeReturn | undefined>(undefined);

// Provider Props
interface ThemeProviderProps {
  children: ReactNode;
}

/**
 * ThemeProvider component cung cấp theme context cho toàn bộ app
 * 
 * Features:
 * - Theme state management
 * - CSS custom properties injection
 * - Local storage persistence
 * - System preference detection
 * 
 * Usage:
 * ```tsx
 * <ThemeProvider>
 *   <App />
 * </ThemeProvider>
 * ```
 */
export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const themeValue = useTheme();

  return (
    <ThemeContext.Provider value={themeValue}>
      {children}
    </ThemeContext.Provider>
  );
};

/**
 * Hook để sử dụng theme context
 * 
 * @throws Error if used outside of ThemeProvider
 * 
 * Usage:
 * ```tsx
 * const { theme, toggleTheme, isDark } = useThemeContext();
 * ```
 */
export const useThemeContext = (): UseThemeReturn => {
  const context = useContext(ThemeContext);
  
  if (context === undefined) {
    throw new Error('useThemeContext must be used within a ThemeProvider');
  }
  
  return context;
};

// Re-export for convenience
export { useTheme } from '../hooks/useTheme';
export type { UseThemeReturn } from '../hooks/useTheme';
