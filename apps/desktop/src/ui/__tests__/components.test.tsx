import { ThemeProvider, createTheme } from '@mui/material/styles';
import { fireEvent, render, screen } from '@testing-library/react';
import React from 'react';
import { vi } from 'vitest';

import ErrorDisplay from '../components/ErrorDisplay';
import LoadingSpinner from '../components/LoadingSpinner';
import Modal from '../components/Modal';
import ResponsiveLayout from '../components/ResponsiveLayout';
import Toast from '../components/Toast';
import Action from "Action";
import After from "After";
import Button from "Button";
import Click from "Click";
import Close from "Close";
import Components from "../../Components/index";
import Content from "Content";
import Detailed from "Detailed";
import Error from "Error";
import FC from "FC";
import MUI from "MUI";
import Main from "../../Main";
import Mock from "Mock";
import Network from "Network";
import ReactNode from "ReactNode";
import Retry from "Retry";
import Should from "Should";
import Sidebar from "../../components/nav/Sidebar";
import Success from "Success";
import Test from "../../Test/index";
import TestWrapper from "TestWrapper";
import Thu from "Thu";
import UI from "../index";
import Xem from "Xem";

// Mock theme for MUI components
const mockTheme = createTheme();

// Test wrapper with MUI theme
const TestWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <ThemeProvider theme={mockTheme}>
    {children}
  </ThemeProvider>
);

describe('UI Components', () => {
  describe('LoadingSpinner', () => {
    it('renders basic spinner', () => {
      render(<LoadingSpinner />, { wrapper: TestWrapper });
      expect(screen.getByRole('progressbar')).toBeInTheDocument();
    });

    it('renders with message', () => {
      render(<LoadingSpinner message="Đang tải..." />, { wrapper: TestWrapper });
      expect(screen.getByText('Đang tải...')).toBeInTheDocument();
    });

    it('renders fullscreen variant', () => {
      render(
        <LoadingSpinner variant="fullscreen" message="Đang xử lý..." backdrop />,
        { wrapper: TestWrapper }
      );
      expect(screen.getByText('Đang xử lý...')).toBeInTheDocument();
    });
  });

  describe('ErrorDisplay', () => {
    it('renders basic error', () => {
      render(<ErrorDisplay message="Đã có lỗi xảy ra" />, { wrapper: TestWrapper });
      expect(screen.getByText('Đã có lỗi xảy ra')).toBeInTheDocument();
    });

    it('renders retry button and calls handler', () => {
      const mockRetry = vi.fn();
      
      render(
        <ErrorDisplay 
          message="Network error" 
          showRetry 
          onRetry={mockRetry} 
        />, 
        { wrapper: TestWrapper }
      );
      
      const retryButton = screen.getByText('Thử lại');
      fireEvent.click(retryButton);
      expect(mockRetry).toHaveBeenCalledOnce();
    });

    it('renders expand button when collapsible', () => {
      render(
        <ErrorDisplay 
          message="Error" 
          details="Detailed error information"
          collapsible 
        />, 
        { wrapper: TestWrapper }
      );
      
      // Should have expand button
      const expandButton = screen.getByLabelText('Xem chi tiết');
      expect(expandButton).toBeInTheDocument();
      
      // Click expand button
      fireEvent.click(expandButton);
      
      // Button label should change to collapse
      expect(screen.getByLabelText('Thu gọn')).toBeInTheDocument();
    });
  });

  describe('Modal', () => {
    it('renders when open', () => {
      render(
        <Modal open={true} onClose={() => {}} title="Test Modal">
          <div>Modal content</div>
        </Modal>,
        { wrapper: TestWrapper }
      );
      
      expect(screen.getByText('Test Modal')).toBeInTheDocument();
      expect(screen.getByText('Modal content')).toBeInTheDocument();
    });

    it('does not render when closed', () => {
      render(
        <Modal open={false} onClose={() => {}} title="Test Modal">
          <div>Modal content</div>
        </Modal>,
        { wrapper: TestWrapper }
      );
      
      expect(screen.queryByText('Test Modal')).not.toBeInTheDocument();
    });

    it('calls onClose when close button is clicked', () => {
      const mockClose = vi.fn();
      
      render(
        <Modal open={true} onClose={mockClose} title="Test Modal">
          <div>Content</div>
        </Modal>,
        { wrapper: TestWrapper }
      );
      
      const closeButton = screen.getByLabelText('Đóng');
      fireEvent.click(closeButton);
      expect(mockClose).toHaveBeenCalledOnce();
    });

    it('renders primary and secondary actions', () => {
      const mockPrimary = vi.fn();
      const mockSecondary = vi.fn();
      
      render(
        <Modal 
          open={true} 
          onClose={() => {}}
          title="Action Modal"
          primaryAction={{ label: "Xác nhận", onClick: mockPrimary }}
          secondaryAction={{ label: "Hủy", onClick: mockSecondary }}
        >
          <div>Content</div>
        </Modal>,
        { wrapper: TestWrapper }
      );
      
      const primaryButton = screen.getByText('Xác nhận');
      const secondaryButton = screen.getByText('Hủy');
      
      fireEvent.click(primaryButton);
      fireEvent.click(secondaryButton);
      
      expect(mockPrimary).toHaveBeenCalledOnce();
      expect(mockSecondary).toHaveBeenCalledOnce();
    });
  });

  describe('Toast', () => {
    it('renders when open', () => {
      render(
        <Toast open={true} message="Success message" onClose={() => {}} />,
        { wrapper: TestWrapper }
      );
      
      expect(screen.getByText('Success message')).toBeInTheDocument();
    });

    it('calls onClose when close button is clicked', () => {
      const mockClose = vi.fn();
      
      render(
        <Toast 
          open={true} 
          message="Test message" 
          onClose={mockClose}
          showCloseButton={true}
        />,
        { wrapper: TestWrapper }
      );
      
      const closeButton = screen.getByLabelText('Close');
      fireEvent.click(closeButton);
      expect(mockClose).toHaveBeenCalledOnce();
    });

    it('renders action button', () => {
      const mockAction = vi.fn();
      
      render(
        <Toast 
          open={true} 
          message="Error occurred" 
          onClose={() => {}}
          action={{ label: "Retry", onClick: mockAction }}
        />,
        { wrapper: TestWrapper }
      );
      
      const actionButton = screen.getByText('Retry');
      fireEvent.click(actionButton);
      expect(mockAction).toHaveBeenCalledOnce();
    });
  });

  describe('ResponsiveLayout', () => {
    it('renders children without sidebar', () => {
      render(
        <ResponsiveLayout>
          <div>Main content</div>
        </ResponsiveLayout>
      );
      
      expect(screen.getByText('Main content')).toBeInTheDocument();
    });

    it('renders with sidebar', () => {
      render(
        <ResponsiveLayout 
          sidebar 
          sidebarContent={<div>Sidebar content</div>}
        >
          <div>Main content</div>
        </ResponsiveLayout>
      );
      
      expect(screen.getByText('Main content')).toBeInTheDocument();
      expect(screen.getByText('Sidebar content')).toBeInTheDocument();
    });

    it('toggles sidebar when collapsible', () => {
      render(
        <ResponsiveLayout 
          sidebar 
          collapsible
          sidebarContent={<div>Sidebar content</div>}
        >
          <div>Main content</div>
        </ResponsiveLayout>
      );
      
      const toggleButton = screen.getByLabelText('Đóng sidebar');
      fireEvent.click(toggleButton);
      
      // After clicking, button should change to "Mở sidebar"
      expect(screen.getByLabelText('Mở sidebar')).toBeInTheDocument();
    });
  });
});
