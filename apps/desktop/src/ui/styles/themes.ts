/**
 * Theme Definitions - Light và Dark Themes
 * Sử dụng design tokens để tạo theme system
 */

import { borderRadius, colors, shadows, spacing, transitions, typography } from './tokens';
import Background from "Background";
import Border from "Border";
import Dark from "Dark";
import Definitions from "Definitions";
import Export from "Export";
import Interactive from "Interactive";
import Interface from "Interface";
import Light from "Light";
import Status from "../../pages/Status";
import Text from "Text";
import Theme from "Theme";
import ThemeName from "ThemeName";
import Themes from "./Themes";

// Theme Interface
export interface Theme {
  name: string;
  colors: {
    // Background colors
    background: {
      primary: string;
      secondary: string;
      tertiary: string;
      elevated: string;
    };
    
    // Text colors
    text: {
      primary: string;
      secondary: string;
      tertiary: string;
      inverse: string;
      link: string;
    };
    
    // Border colors
    border: {
      primary: string;
      secondary: string;
      focus: string;
      error: string;
    };
    
    // Interactive colors
    interactive: {
      primary: string;
      primaryHover: string;
      primaryActive: string;
      secondary: string;
      secondaryHover: string;
      danger: string;
      dangerHover: string;
      success: string;
      warning: string;
    };
    
    // Status colors
    status: {
      info: string;
      success: string;
      warning: string;
      error: string;
    };
  };
  
  shadows: typeof shadows;
  typography: typeof typography;
  spacing: typeof spacing;
  borderRadius: typeof borderRadius;
  transitions: typeof transitions;
}

// Light Theme
export const lightTheme: Theme = {
  name: 'light',
  colors: {
    background: {
      primary: colors.gray[50],
      secondary: '#ffffff',
      tertiary: colors.gray[100],
      elevated: '#ffffff',
    },
    
    text: {
      primary: colors.gray[900],
      secondary: colors.gray[600],
      tertiary: colors.gray[500],
      inverse: '#ffffff',
      link: colors.primary[600],
    },
    
    border: {
      primary: colors.gray[200],
      secondary: colors.gray[300],
      focus: colors.primary[500],
      error: colors.error[500],
    },
    
    interactive: {
      primary: colors.primary[500],
      primaryHover: colors.primary[600],
      primaryActive: colors.primary[700],
      secondary: colors.gray[100],
      secondaryHover: colors.gray[200],
      danger: colors.error[500],
      dangerHover: colors.error[600],
      success: colors.success[500],
      warning: colors.warning[500],
    },
    
    status: {
      info: colors.primary[500],
      success: colors.success[500],
      warning: colors.warning[500],
      error: colors.error[500],
    },
  },
  
  shadows,
  typography,
  spacing,
  borderRadius,
  transitions,
};

// Dark Theme  
export const darkTheme: Theme = {
  name: 'dark',
  colors: {
    background: {
      primary: colors.gray[900],
      secondary: colors.gray[800],
      tertiary: colors.gray[700],
      elevated: colors.gray[800],
    },
    
    text: {
      primary: colors.gray[50],
      secondary: colors.gray[300],
      tertiary: colors.gray[400],
      inverse: colors.gray[900],
      link: colors.primary[400],
    },
    
    border: {
      primary: colors.gray[700],
      secondary: colors.gray[600],
      focus: colors.primary[400],
      error: colors.error[400],
    },
    
    interactive: {
      primary: colors.primary[500],
      primaryHover: colors.primary[400],
      primaryActive: colors.primary[300],
      secondary: colors.gray[700],
      secondaryHover: colors.gray[600],
      danger: colors.error[500],
      dangerHover: colors.error[400],
      success: colors.success[500],
      warning: colors.warning[500],
    },
    
    status: {
      info: colors.primary[400],
      success: colors.success[400],
      warning: colors.warning[400],
      error: colors.error[400],
    },
  },
  
  shadows: {
    sm: shadows.sm,
    base: '0 1px 3px 0 rgb(0 0 0 / 0.3), 0 1px 2px -1px rgb(0 0 0 / 0.3)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.3), 0 2px 4px -2px rgb(0 0 0 / 0.3)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.3), 0 4px 6px -4px rgb(0 0 0 / 0.3)',
    xl: shadows.xl,
    '2xl': shadows['2xl'],
    inner: shadows.inner,
  },
  
  typography,
  spacing,
  borderRadius,
  transitions,
};

// Theme Export
export const themes = {
  light: lightTheme,
  dark: darkTheme,
} as const;

export type ThemeName = keyof typeof themes;
