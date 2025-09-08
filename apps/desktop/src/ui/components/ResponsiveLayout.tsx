import { useMediaQuery } from '@mui/material';
import { useTheme as useMuiTheme } from '@mui/material/styles';
import React from 'react';
import Auto from "Auto";
import Basic from "Basic";
import Children from "Children";
import Custom from "Custom";
import Enter from "Enter";
import FC from "FC";
import Main from "../../Main";
import MainContent from "MainContent";
import Mobile from "Mobile";
import NavigationMenu from "NavigationMenu";
import ReactNode from "ReactNode";
import Responsive from "Responsive";
import ResponsiveLayout from "./ResponsiveLayout";
import ResponsiveLayoutProps from "ResponsiveLayoutProps";
import Sidebar from "../../components/nav/Sidebar";
import Whether from "Whether";
import With from "With";

export interface ResponsiveLayoutProps {
  /** Children to render */
  children: React.ReactNode;
  /** Whether to use sidebar layout on larger screens */
  sidebar?: boolean;
  /** Sidebar content (only used if sidebar=true) */
  sidebarContent?: React.ReactNode;
  /** Sidebar width in pixels */
  sidebarWidth?: number;
  /** Whether sidebar is collapsible */
  collapsible?: boolean;
  /** Whether sidebar starts collapsed */
  defaultCollapsed?: boolean;
  /** Custom breakpoint for sidebar collapse */
  collapseBreakpoint?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
}

/**
 * Responsive layout component với sidebar và breakpoint handling
 * Tự động adapt layout dựa trên screen size và theme
 * 
 * @example
 * // Basic responsive container
 * <ResponsiveLayout>
 *   <MainContent />
 * </ResponsiveLayout>
 * 
 * @example
 * // With sidebar
 * <ResponsiveLayout 
 *   sidebar
 *   sidebarContent={<NavigationMenu />}
 *   collapsible
 * >
 *   <MainContent />
 * </ResponsiveLayout>
 */
export const ResponsiveLayout: React.FC<ResponsiveLayoutProps> = ({
  children,
  sidebar = false,
  sidebarContent,
  sidebarWidth = 280,
  collapsible = false,
  defaultCollapsed = false,
  collapseBreakpoint = 'md'
}) => {
  const muiTheme = useMuiTheme();
  const [collapsed, setCollapsed] = React.useState(defaultCollapsed);
  
  // Responsive breakpoints
  const isMobile = useMediaQuery(muiTheme.breakpoints.down('sm'));
  const shouldCollapse = useMediaQuery(muiTheme.breakpoints.down(collapseBreakpoint));
  
  // Auto-collapse on small screens
  React.useEffect(() => {
    if (shouldCollapse && !collapsed) {
      setCollapsed(true);
    }
  }, [shouldCollapse, collapsed]);

  const toggleSidebar = () => {
    if (collapsible) {
      setCollapsed(!collapsed);
    }
  };

  const effectiveSidebarWidth = collapsed ? 60 : sidebarWidth;
  let sidebarWidth_final: string | number;
  if (isMobile) {
    sidebarWidth_final = collapsed ? 0 : '100%';
  } else {
    sidebarWidth_final = effectiveSidebarWidth;
  }

  if (!sidebar) {
    return (
      <div
        style={{
          width: '100%',
          height: '100%',
          backgroundColor: `var(--theme-bg-primary)`,
          color: `var(--theme-text-primary)`,
          transition: 'background-color 0.3s ease, color 0.3s ease'
        }}
      >
        {children}
      </div>
    );
  }

  return (
    <div
      style={{
        display: 'flex',
        width: '100%',
        height: '100%',
        backgroundColor: `var(--theme-bg-primary)`,
        color: `var(--theme-text-primary)`,
        transition: 'background-color 0.3s ease, color 0.3s ease'
      }}
    >
      {/* Sidebar */}
      <div
        style={{
          width: sidebarWidth_final,
          height: '100%',
          backgroundColor: `var(--theme-bg-secondary)`,
          borderRight: `1px solid var(--theme-border-primary)`,
          transition: 'width 0.3s ease, background-color 0.3s ease',
          overflow: 'hidden',
          position: isMobile ? 'fixed' : 'relative',
          zIndex: isMobile ? 1000 : 'auto',
          boxShadow: isMobile && !collapsed ? muiTheme.shadows[8] : 'none'
        }}
      >
        {collapsible && (
          <div
            style={{
              padding: '8px',
              borderBottom: `1px solid var(--theme-border-primary)`,
              textAlign: 'right'
            }}
          >
            <button
              onClick={toggleSidebar}
              style={{
                background: 'none',
                border: 'none',
                color: `var(--theme-text-primary)`,
                cursor: 'pointer',
                fontSize: '18px',
                padding: '4px 8px'
              }}
              aria-label={collapsed ? 'Mở sidebar' : 'Đóng sidebar'}
            >
              {collapsed ? '→' : '←'}
            </button>
          </div>
        )}
        <div
          style={{
            height: collapsible ? 'calc(100% - 41px)' : '100%',
            overflow: 'auto'
          }}
        >
          {sidebarContent}
        </div>
      </div>

      {/* Mobile backdrop */}
      {isMobile && !collapsed && (
        <button
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            zIndex: 999,
            border: 'none',
            cursor: 'pointer'
          }}
          onClick={toggleSidebar}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              toggleSidebar();
            }
          }}
          aria-label="Đóng sidebar"
          type="button"
        />
      )}

      {/* Main content */}
      <div
        style={{
          flex: 1,
          height: '100%',
          overflow: 'auto',
          width: isMobile ? '100%' : `calc(100% - ${effectiveSidebarWidth}px)`,
          transition: 'width 0.3s ease, margin 0.3s ease'
        }}
      >
        {children}
      </div>
    </div>
  );
};

export default ResponsiveLayout;
