/**
 * UI Module - Barrel Export
 * Main export file cho UI system components
 */

// Theme System
// CSS Import (for convenience)
import './styles/accessibility.css';
import './styles/global.css';
import AccessibilityMenu from "./components/AccessibilityMenu";
import AccessibilityMenuProps from "AccessibilityMenuProps";
import AnimationWrapper from "./components/AnimationWrapper";
import AnimationWrapperProps from "AnimationWrapperProps";
import Barrel from "Barrel";
import CSS from "CSS";
import Components from "./Components/index";
import ErrorDisplay from "./components/ErrorDisplay";
import ErrorDisplayProps from "ErrorDisplayProps";
import Export from "Export";
import Import from "Import";
import LoadingSpinner from "./components/LoadingSpinner";
import LoadingSpinnerProps from "LoadingSpinnerProps";
import Main from "../Main";
import Modal from "./components/Modal";
import ModalProps from "ModalProps";
import ModalTransition from "ModalTransition";
import Module from "Module";
import PageTransition from "PageTransition";
import ResponsiveLayout from "./components/ResponsiveLayout";
import ResponsiveLayoutProps from "ResponsiveLayoutProps";
import StaggerList from "StaggerList";
import Styles from "./Styles/index";
import System from "System";
import Theme from "Theme";
import ThemeName from "ThemeName";
import ThemeProvider from "./providers/ThemeProvider";
import ThemeToggle from "./components/ThemeToggle";
import Toast from "./components/Toast";
import ToastProps from "ToastProps";
import Tokens from "Tokens";
import UI from "./index";
import UseThemeReturn from "UseThemeReturn";

export { ThemeProvider, useTheme, useThemeContext } from './providers/ThemeProvider';
export type { UseThemeReturn } from './providers/ThemeProvider';

// Components
export { default as AccessibilityMenu } from './components/AccessibilityMenu';
export { default as AnimationWrapper, ModalTransition, PageTransition, StaggerList } from './components/AnimationWrapper';
export { default as ErrorDisplay } from './components/ErrorDisplay';
export { default as LoadingSpinner } from './components/LoadingSpinner';
export { default as Modal } from './components/Modal';
export { default as ResponsiveLayout } from './components/ResponsiveLayout';
export { default as ThemeToggle } from './components/ThemeToggle';
export { default as Toast } from './components/Toast';

// Export component types
export type { AccessibilityMenuProps } from './components/AccessibilityMenu';
export type { AnimationWrapperProps } from './components/AnimationWrapper';
export type { ErrorDisplayProps } from './components/ErrorDisplay';
export type { LoadingSpinnerProps } from './components/LoadingSpinner';
export type { ModalProps } from './components/Modal';
export type { ResponsiveLayoutProps } from './components/ResponsiveLayout';
export type { ToastProps } from './components/Toast';

// Styles & Tokens
export { darkTheme, lightTheme, themes } from './styles/themes';
export type { Theme, ThemeName } from './styles/themes';
export { tokens } from './styles/tokens';

