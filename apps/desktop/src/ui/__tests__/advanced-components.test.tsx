import { ThemeProvider, createTheme } from '@mui/material/styles';
import { fireEvent, render, screen } from '@testing-library/react';
import React from 'react';
import { vi } from 'vitest';

import AccessibilityMenu from '../components/AccessibilityMenu';
import AnimationWrapper, { ModalTransition, PageTransition, StaggerList } from '../components/AnimationWrapper';
import Accessibility from "Accessibility";
import Advanced from "Advanced";
import AnimatePresence from "AnimatePresence";
import Animated from "Animated";
import CSS from "CSS";
import Change from "Change";
import Check from "Check";
import Clean from "Clean";
import Click from "Click";
import Components from "../../Components/index";
import Custom from "Custom";
import Enable from "Enable";
import FC from "FC";
import Find from "Find";
import Framer from "Framer";
import Item from "Item";
import MUI from "MUI";
import Mock from "Mock";
import Modal from "../components/Modal";
import Motion from "Motion";
import Open from "Open";
import Page from "Page";
import ReactNode from "ReactNode";
import Reset from "Reset";
import Scale from "Scale";
import Settings from "../../pages/Settings";
import Slide from "Slide";
import Stagger from "Stagger";
import Test from "../../Test/index";
import TestWrapper from "TestWrapper";
import UI from "../index";

// Mock Framer Motion
vi.mock('framer-motion', () => ({
  motion: {
    div: ({ children, ...props }: any) => <div {...props}>{children}</div>
  },
  AnimatePresence: ({ children }: any) => children
}));

// Mock theme for MUI components
const mockTheme = createTheme();

// Test wrapper with MUI theme
const TestWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <ThemeProvider theme={mockTheme}>
    {children}
  </ThemeProvider>
);

describe('Advanced UI Components', () => {
  describe('AnimationWrapper', () => {
    it('renders children with default animation', () => {
      render(
        <AnimationWrapper>
          <div>Animated content</div>
        </AnimationWrapper>
      );
      
      expect(screen.getByText('Animated content')).toBeInTheDocument();
    });

    it('renders with slideIn variant', () => {
      render(
        <AnimationWrapper variant="slideIn">
          <div>Slide content</div>
        </AnimationWrapper>
      );
      
      expect(screen.getByText('Slide content')).toBeInTheDocument();
    });

    it('renders with scaleIn variant', () => {
      render(
        <AnimationWrapper variant="scaleIn">
          <div>Scale content</div>
        </AnimationWrapper>
      );
      
      expect(screen.getByText('Scale content')).toBeInTheDocument();
    });

    it('renders with stagger variant', () => {
      render(
        <AnimationWrapper variant="stagger">
          <div>Stagger content</div>
        </AnimationWrapper>
      );
      
      expect(screen.getByText('Stagger content')).toBeInTheDocument();
    });

    it('applies custom duration and delay', () => {
      render(
        <AnimationWrapper duration={1.5} delay={0.5}>
          <div>Custom timing</div>
        </AnimationWrapper>
      );
      
      expect(screen.getByText('Custom timing')).toBeInTheDocument();
    });
  });

  describe('PageTransition', () => {
    it('renders page transition wrapper', () => {
      render(
        <PageTransition>
          <div>Page content</div>
        </PageTransition>
      );
      
      expect(screen.getByText('Page content')).toBeInTheDocument();
    });
  });

  describe('ModalTransition', () => {
    it('renders modal transition wrapper', () => {
      render(
        <ModalTransition>
          <div>Modal content</div>
        </ModalTransition>
      );
      
      expect(screen.getByText('Modal content')).toBeInTheDocument();
    });
  });

  describe('StaggerList', () => {
    it('renders stagger list with children', () => {
      render(
        <StaggerList>
          <div>Item 1</div>
          <div>Item 2</div>
          <div>Item 3</div>
        </StaggerList>
      );
      
      expect(screen.getByText('Item 1')).toBeInTheDocument();
      expect(screen.getByText('Item 2')).toBeInTheDocument();
      expect(screen.getByText('Item 3')).toBeInTheDocument();
    });
  });

  describe('AccessibilityMenu', () => {
    beforeEach(() => {
      // Reset document state
      document.documentElement.className = '';
      document.documentElement.style.cssText = '';
    });

    it('renders accessibility icon button', () => {
      render(<AccessibilityMenu />, { wrapper: TestWrapper });
      
      const button = screen.getByLabelText('Mở menu accessibility');
      expect(button).toBeInTheDocument();
    });

    it('renders as button variant', () => {
      render(<AccessibilityMenu variant="button" />, { wrapper: TestWrapper });
      
      expect(screen.getByText('Accessibility')).toBeInTheDocument();
    });

    it('opens menu when clicked', () => {
      render(<AccessibilityMenu />, { wrapper: TestWrapper });
      
      const button = screen.getByLabelText('Mở menu accessibility');
      fireEvent.click(button);
      
      expect(screen.getByText('Accessibility Settings')).toBeInTheDocument();
    });

    it('changes font size when button is clicked', () => {
      render(<AccessibilityMenu />, { wrapper: TestWrapper });
      
      // Open menu
      const button = screen.getByLabelText('Mở menu accessibility');
      fireEvent.click(button);
      
      // Click large font size
      const largeButton = screen.getByText('Lớn');
      fireEvent.click(largeButton);
      
      // Check if CSS variable is set
      expect(document.documentElement.style.getPropertyValue('--accessibility-font-scale')).toBe('1.2');
    });

    it('toggles high contrast mode', () => {
      render(<AccessibilityMenu />, { wrapper: TestWrapper });
      
      // Open menu
      const button = screen.getByLabelText('Mở menu accessibility');
      fireEvent.click(button);
      
      // Find and toggle high contrast switch
      const contrastSwitch = screen.getByRole('checkbox', { name: /Chế độ tương phản cao/i });
      fireEvent.click(contrastSwitch);
      
      // Check if high-contrast class is added
      expect(document.documentElement.classList.contains('high-contrast')).toBe(true);
    });

    it('toggles reduce motion mode', () => {
      render(<AccessibilityMenu />, { wrapper: TestWrapper });
      
      // Open menu
      const button = screen.getByLabelText('Mở menu accessibility');
      fireEvent.click(button);
      
      // Find and toggle reduce motion switch
      const motionSwitch = screen.getByRole('checkbox', { name: /Giảm animation/i });
      fireEvent.click(motionSwitch);
      
      // Check if reduce-motion class is added
      expect(document.documentElement.classList.contains('reduce-motion')).toBe(true);
    });

    it('resets settings to default', () => {
      render(<AccessibilityMenu />, { wrapper: TestWrapper });
      
      // Open menu
      const button = screen.getByLabelText('Mở menu accessibility');
      fireEvent.click(button);
      
      // Change some settings first
      const largeButton = screen.getByText('Lớn');
      fireEvent.click(largeButton);
      
      const contrastSwitch = screen.getByRole('checkbox', { name: /Chế độ tương phản cao/i });
      fireEvent.click(contrastSwitch);
      
      // Reset settings
      const resetButton = screen.getByText('Reset về mặc định');
      fireEvent.click(resetButton);
      
      // Check if settings are reset
      expect(document.documentElement.style.getPropertyValue('--accessibility-font-scale')).toBe('1');
      expect(document.documentElement.classList.contains('high-contrast')).toBe(false);
    });

    it('announces to screen reader when enabled', () => {
      // Mock document.body.appendChild and removeChild
      const appendChildSpy = vi.spyOn(document.body, 'appendChild');
      const removeChildSpy = vi.spyOn(document.body, 'removeChild');
      
      render(<AccessibilityMenu />, { wrapper: TestWrapper });
      
      // Open menu
      const button = screen.getByLabelText('Mở menu accessibility');
      fireEvent.click(button);
      
      // Enable screen reader
      const screenReaderSwitch = screen.getByRole('checkbox', { name: /Hỗ trợ screen reader/i });
      fireEvent.click(screenReaderSwitch);
      
      // Check if announcement div was created
      expect(appendChildSpy).toHaveBeenCalled();
      
      // Clean up
      appendChildSpy.mockRestore();
      removeChildSpy.mockRestore();
    });
  });
});
