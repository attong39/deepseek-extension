/**
 * ThemeToggle Component
 * Button để toggle giữa light và dark theme
 */

import React from 'react';

import { useThemeContext } from '../providers/ThemeProvider';
import './ThemeToggle.css';
import Accessible from "Accessible";
import Button from "Button";
import Component from "Component";
import Custom from "Custom";
import Dark from "Dark";
import FC from "FC";
import Features from "../../Features/index";
import Icon from "Icon";
import Light from "Light";
import M12 from "M12";
import M21 from "M21";
import Moon from "Moon";
import Multiple from "Multiple";
import Optional from "Optional";
import Show from "Show";
import Size from "Size";
import Smooth from "Smooth";
import Sun from "Sun";
import Switch from "Switch";
import Theme from "Theme";
import ThemeProvider from "../providers/ThemeProvider";
import ThemeToggle from "./ThemeToggle";
import ThemeToggleProps from "ThemeToggleProps";
import Tooltip from "Tooltip";
import Usage from "Usage";

interface ThemeToggleProps {
  /** Size of the toggle button */
  size?: 'sm' | 'md' | 'lg';
  
  /** Show text label alongside icon */
  showLabel?: boolean;
  
  /** Custom className */
  className?: string;
  
  /** Tooltip text */
  title?: string;
}

/**
 * ThemeToggle component cho theme switching
 * 
 * Features:
 * - Smooth icon transition
 * - Accessible keyboard support
 * - Multiple sizes
 * - Optional text labels
 * 
 * Usage:
 * ```tsx
 * <ThemeToggle size="md" showLabel />
 * ```
 */
export const ThemeToggle: React.FC<ThemeToggleProps> = ({
  size = 'md',
  showLabel = false,
  className = '',
  title,
}) => {
  const { toggleTheme, isDark } = useThemeContext();
  
  const sizeClasses = {
    sm: 'theme-toggle--sm',
    md: 'theme-toggle--md', 
    lg: 'theme-toggle--lg',
  };

  const buttonTitle = title || `Switch to ${isDark ? 'light' : 'dark'} theme`;

  return (
    <button
      className={`theme-toggle ${sizeClasses[size]} ${className}`}
      onClick={toggleTheme}
      title={buttonTitle}
      aria-label={buttonTitle}
      type="button"
    >
      <div className="theme-toggle__icon-container">
        {/* Sun Icon (Light Theme) */}
        <svg
          className={`theme-toggle__icon theme-toggle__sun ${isDark ? 'theme-toggle__icon--hidden' : ''}`}
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <circle cx="12" cy="12" r="5"/>
          <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
        </svg>
        
        {/* Moon Icon (Dark Theme) */}
        <svg
          className={`theme-toggle__icon theme-toggle__moon ${!isDark ? 'theme-toggle__icon--hidden' : ''}`}
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
        </svg>
      </div>
      
      {showLabel && (
        <span className="theme-toggle__label">
          {isDark ? 'Dark' : 'Light'}
        </span>
      )}
    </button>
  );
};

export default ThemeToggle;
