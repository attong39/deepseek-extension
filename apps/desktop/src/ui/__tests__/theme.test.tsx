/**
 * UI Module Tests
 * Test suite cho Theme System và UI components
 */

import { act, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import ThemeToggle from '../components/ThemeToggle';
import { ThemeProvider, useThemeContext } from '../providers/ThemeProvider';
import { themes } from '../styles/themes';
import CSS from "CSS";
import Component from "Component";
import Custom from "Custom";
import Definitions from "Definitions";
import Initially from "Initially";
import Light from "Light";
import Mock from "Mock";
import Module from "Module";
import Override from "Override";
import Prefers from "Prefers";
import Properties from "Properties";
import Reset from "Reset";
import Setup from "Setup";
import Should from "Should";
import Suppress from "Suppress";
import Switch from "Switch";
import System from "System";
import Test from "../../Test/index";
import TestComponent from "TestComponent";
import Tests from "../../Tests/index";
import Theme from "Theme";
import Toggle from "Toggle";
import UI from "../index";

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
};

// Mock matchMedia
const matchMediaMock = vi.fn((query) => ({
  matches: false,
  media: query,
  onchange: null,
  addListener: vi.fn(),
  removeListener: vi.fn(),
  addEventListener: vi.fn(),
  removeEventListener: vi.fn(),
  dispatchEvent: vi.fn(),
}));

// Test component để sử dụng theme context
const TestComponent = () => {
  const { theme, toggleTheme, isDark, isLight } = useThemeContext();
  
  return (
    <div>
      <span data-testid="current-theme">{theme}</span>
      <span data-testid="is-dark">{isDark.toString()}</span>
      <span data-testid="is-light">{isLight.toString()}</span>
      <button data-testid="toggle-theme" onClick={toggleTheme}>
        Toggle Theme
      </button>
    </div>
  );
};

describe('Theme System', () => {
  beforeEach(() => {
    // Reset mocks
    vi.clearAllMocks();
    
    // Setup localStorage mock
    Object.defineProperty(window, 'localStorage', {
      value: localStorageMock,
      writable: true,
    });
    
    // Setup matchMedia mock
    Object.defineProperty(window, 'matchMedia', {
      value: matchMediaMock,
      writable: true,
    });
    
    // Mock document.documentElement.style
    Object.defineProperty(document.documentElement, 'style', {
      value: { setProperty: vi.fn() },
      writable: true,
    });
    
    // Mock document.body.classList
    Object.defineProperty(document.body, 'classList', {
      value: { add: vi.fn(), remove: vi.fn() },
      writable: true,
    });
    
    // Mock className property
    Object.defineProperty(document.body, 'className', {
      value: '',
      writable: true,
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('ThemeProvider', () => {
    it('provides default light theme', () => {
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      expect(screen.getByTestId('current-theme')).toHaveTextContent('light');
      expect(screen.getByTestId('is-dark')).toHaveTextContent('false');
      expect(screen.getByTestId('is-light')).toHaveTextContent('true');
    });

    it('loads theme from localStorage', () => {
      localStorageMock.getItem.mockReturnValue('dark');

      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      expect(screen.getByTestId('current-theme')).toHaveTextContent('dark');
      expect(screen.getByTestId('is-dark')).toHaveTextContent('true');
    });

    it('toggles theme when toggle function is called', () => {
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      const toggleButton = screen.getByTestId('toggle-theme');
      
      // Initially light
      expect(screen.getByTestId('current-theme')).toHaveTextContent('light');

      // Toggle to dark
      act(() => {
        fireEvent.click(toggleButton);
      });

      expect(screen.getByTestId('current-theme')).toHaveTextContent('dark');
      expect(localStorageMock.setItem).toHaveBeenCalledWith('zeta-theme-preference', 'dark');

      // Toggle back to light
      act(() => {
        fireEvent.click(toggleButton);
      });

      expect(screen.getByTestId('current-theme')).toHaveTextContent('light');
      expect(localStorageMock.setItem).toHaveBeenCalledWith('zeta-theme-preference', 'light');
    });

    it('detects system preference when no localStorage value', () => {
      localStorageMock.getItem.mockReturnValue(null);
      
      // Override matchMedia for this test
      Object.defineProperty(window, 'matchMedia', {
        value: vi.fn(() => ({
          matches: true, // Prefers dark
          media: '(prefers-color-scheme: dark)',
          onchange: null,
          addListener: vi.fn(),
          removeListener: vi.fn(),
          addEventListener: vi.fn(),
          removeEventListener: vi.fn(),
          dispatchEvent: vi.fn(),
        })),
        writable: true,
      });

      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      expect(screen.getByTestId('current-theme')).toHaveTextContent('dark');
    });

    it('throws error when used outside provider', () => {
      // Suppress console.error cho test này
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      expect(() => {
        render(<TestComponent />);
      }).toThrow('useThemeContext must be used within a ThemeProvider');

      consoleSpy.mockRestore();
    });
  });

  describe('ThemeToggle Component', () => {
    it('renders with light theme icon by default', () => {
      render(
        <ThemeProvider>
          <ThemeToggle />
        </ThemeProvider>
      );

      const button = screen.getByRole('button');
      expect(button).toBeInTheDocument();
      expect(button).toHaveAttribute('aria-label', 'Switch to dark theme');
    });

    it('renders with dark theme icon when dark theme is active', () => {
      localStorageMock.getItem.mockReturnValue('dark');

      render(
        <ThemeProvider>
          <ThemeToggle />
        </ThemeProvider>
      );

      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('aria-label', 'Switch to light theme');
    });

    it('toggles theme when clicked', () => {
      render(
        <ThemeProvider>
          <ThemeToggle />
        </ThemeProvider>
      );

      const button = screen.getByRole('button');
      
      act(() => {
        fireEvent.click(button);
      });

      expect(localStorageMock.setItem).toHaveBeenCalledWith('zeta-theme-preference', 'dark');
    });

    it('supports different sizes', () => {
      const { rerender } = render(
        <ThemeProvider>
          <ThemeToggle size="sm" />
        </ThemeProvider>
      );

      let button = screen.getByRole('button');
      expect(button).toHaveClass('theme-toggle--sm');

      rerender(
        <ThemeProvider>
          <ThemeToggle size="lg" />
        </ThemeProvider>
      );

      button = screen.getByRole('button');
      expect(button).toHaveClass('theme-toggle--lg');
    });

    it('shows label when showLabel prop is true', () => {
      render(
        <ThemeProvider>
          <ThemeToggle showLabel />
        </ThemeProvider>
      );

      expect(screen.getByText('Light')).toBeInTheDocument();
    });

    it('supports custom className', () => {
      render(
        <ThemeProvider>
          <ThemeToggle className="custom-class" />
        </ThemeProvider>
      );

      const button = screen.getByRole('button');
      expect(button).toHaveClass('custom-class');
    });

    it('supports custom title attribute', () => {
      render(
        <ThemeProvider>
          <ThemeToggle title="Custom toggle title" />
        </ThemeProvider>
      );

      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('title', 'Custom toggle title');
    });
  });

  describe('Theme Definitions', () => {
    it('exports light and dark themes', () => {
      expect(themes.light).toBeDefined();
      expect(themes.dark).toBeDefined();
      
      expect(themes.light.name).toBe('light');
      expect(themes.dark.name).toBe('dark');
    });

    it('light theme has correct structure', () => {
      const lightTheme = themes.light;
      
      expect(lightTheme.colors).toBeDefined();
      expect(lightTheme.colors.background).toBeDefined();
      expect(lightTheme.colors.text).toBeDefined();
      expect(lightTheme.colors.border).toBeDefined();
      expect(lightTheme.colors.interactive).toBeDefined();
      expect(lightTheme.colors.status).toBeDefined();
      
      expect(lightTheme.shadows).toBeDefined();
      expect(lightTheme.typography).toBeDefined();
      expect(lightTheme.spacing).toBeDefined();
    });

    it('dark theme has correct structure', () => {
      const darkTheme = themes.dark;
      
      expect(darkTheme.colors).toBeDefined();
      expect(darkTheme.colors.background).toBeDefined();
      expect(darkTheme.colors.text).toBeDefined();
      expect(darkTheme.colors.border).toBeDefined();
      expect(darkTheme.colors.interactive).toBeDefined();
      expect(darkTheme.colors.status).toBeDefined();
      
      expect(darkTheme.shadows).toBeDefined();
      expect(darkTheme.typography).toBeDefined();
      expect(darkTheme.spacing).toBeDefined();
    });

    it('themes have different background colors', () => {
      expect(themes.light.colors.background.primary).not.toBe(
        themes.dark.colors.background.primary
      );
    });
  });

  describe('CSS Custom Properties', () => {
    it('sets CSS custom properties when theme changes', () => {
      const setPropertySpy = vi.spyOn(document.documentElement.style, 'setProperty');

      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      // Should set CSS properties for light theme
      expect(setPropertySpy).toHaveBeenCalled();
    });

    it('adds theme class to body', () => {
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      expect(document.body.classList.add).toHaveBeenCalledWith('theme-light');
    });
  });
});
