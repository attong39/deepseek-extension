/**
 * useTheme Hook
 * Theme management với localStorage persistence
 */

import { useCallback, useEffect, useState } from 'react';

import { themes, type ThemeName } from '../styles/themes';
import Add from "Add";
import Auto from "Auto";
import CSS from "CSS";
import Check from "Check";
import Current from "Current";
import Fallback from "Fallback";
import Features from "../../Features/index";
import Get from "Get";
import Hook from "Hook";
import Initialize from "Initialize";
import Inject from "Inject";
import Listen from "Listen";
import LocalStorage from "LocalStorage";
import MediaQueryListEvent from "MediaQueryListEvent";
import Only from "Only";
import Set from "Set";
import StorageEvent from "StorageEvent";
import THEME_STORAGE_KEY from "THEME_STORAGE_KEY";
import Theme from "Theme";
import ThemeName from "ThemeName";
import Toggle from "Toggle";
import Update from "Update";
import UseThemeReturn from "UseThemeReturn";

const THEME_STORAGE_KEY = 'zeta-theme-preference';

export interface UseThemeReturn {
  /** Current active theme name */
  theme: ThemeName;
  
  /** Current theme object */
  themeConfig: typeof themes.light;
  
  /** Toggle between light and dark theme */
  toggleTheme: () => void;
  
  /** Set specific theme */
  setTheme: (theme: ThemeName) => void;
  
  /** Check if current theme is dark */
  isDark: boolean;
  
  /** Check if current theme is light */
  isLight: boolean;
}

/**
 * Hook quản lý theme state và persistence
 * 
 * Features:
 * - Auto-detect system preference
 * - LocalStorage persistence
 * - CSS custom properties injection
 * - Theme switching animations
 */
export const useTheme = (): UseThemeReturn => {
  // Get initial theme từ localStorage hoặc system preference
  const getInitialTheme = useCallback((): ThemeName => {
    // Check localStorage first
    const stored = localStorage.getItem(THEME_STORAGE_KEY) as ThemeName;
    if (stored && themes[stored]) {
      return stored;
    }
    
    // Fallback to system preference
    if (typeof window !== 'undefined' && window.matchMedia) {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      return prefersDark ? 'dark' : 'light';
    }
    
    return 'light';
  }, []);

  const [theme, setThemeState] = useState<ThemeName>(() => getInitialTheme());
  
  // Update CSS custom properties khi theme thay đổi
  const updateCSSProperties = useCallback((themeName: ThemeName) => {
    const themeConfig = themes[themeName];
    const root = document.documentElement;
    
    // Inject theme colors as CSS custom properties
    Object.entries(themeConfig.colors.background).forEach(([key, value]) => {
      root.style.setProperty(`--color-bg-${key}`, value);
    });
    
    Object.entries(themeConfig.colors.text).forEach(([key, value]) => {
      root.style.setProperty(`--color-text-${key}`, value);
    });
    
    Object.entries(themeConfig.colors.border).forEach(([key, value]) => {
      root.style.setProperty(`--color-border-${key}`, value);
    });
    
    Object.entries(themeConfig.colors.interactive).forEach(([key, value]) => {
      root.style.setProperty(`--color-interactive-${key}`, value);
    });
    
    Object.entries(themeConfig.colors.status).forEach(([key, value]) => {
      root.style.setProperty(`--color-status-${key}`, value);
    });
    
    // Add theme class to body
    document.body.className = document.body.className.replace(/theme-\w+/g, '');
    document.body.classList.add(`theme-${themeName}`);
    
    // Update meta theme-color cho mobile browsers
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
      metaThemeColor.setAttribute('content', themeConfig.colors.background.primary);
    }
  }, []);

  // Set theme với persistence
  const setTheme = useCallback((newTheme: ThemeName) => {
    setThemeState(newTheme);
    localStorage.setItem(THEME_STORAGE_KEY, newTheme);
    updateCSSProperties(newTheme);
  }, [updateCSSProperties]);

  // Toggle between light and dark
  const toggleTheme = useCallback(() => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
  }, [theme, setTheme]);

  // Listen to system preference changes
  useEffect(() => {
    if (typeof window === 'undefined' || !window.matchMedia) return;
    
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    const handleChange = (e: MediaQueryListEvent) => {
      // Only auto-switch if user hasn't manually set a preference
      const hasManualPreference = localStorage.getItem(THEME_STORAGE_KEY);
      if (!hasManualPreference) {
        const newTheme = e.matches ? 'dark' : 'light';
        setTheme(newTheme);
      }
    };
    
    mediaQuery.addEventListener('change', handleChange);
    
    return () => {
      mediaQuery.removeEventListener('change', handleChange);
    };
  }, [setTheme]);

  // Initialize CSS properties on mount
  useEffect(() => {
    updateCSSProperties(theme);
  }, [theme, updateCSSProperties]);

  // Listen for storage changes (multi-tab sync)
  useEffect(() => {
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === THEME_STORAGE_KEY && e.newValue) {
        const newTheme = e.newValue as ThemeName;
        if (themes[newTheme] && newTheme !== theme) {
          setThemeState(newTheme);
          updateCSSProperties(newTheme);
        }
      }
    };
    
    window.addEventListener('storage', handleStorageChange);
    
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [theme, updateCSSProperties]);

  return {
    theme,
    themeConfig: themes[theme],
    toggleTheme,
    setTheme,
    isDark: theme === 'dark',
    isLight: theme === 'light',
  };
};
