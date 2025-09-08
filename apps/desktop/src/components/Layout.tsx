import {
    Psychology as AssistantIcon,
    Chat as ChatIcon,
    Dashboard as DashboardIcon,
    Storage as DatasetIcon,
    Logout as LogoutIcon,
    Article as LogsIcon,
    Menu as MenuIcon,
    Settings as SettingsIcon,
} from '@mui/icons-material';
import {
    AppBar,
    Box,
    Button,
    Chip,
    Drawer,
    IconButton,
    List,
    ListItem,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    Toolbar,
    Typography,
} from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

import { apiService, queryKeys } from '../services/apiService';
import AccessibilityMenu from '../ui/components/AccessibilityMenu';
import ThemeToggle from '../ui/components/ThemeToggle';
import AI from "AI";
import API from "../API/index";
import Accessibility from "Accessibility";
import App from "../App";
import Article from "Article";
import Assistant from "Assistant";
import Bar from "Bar";
import Better from "Better";
import Chat from "../pages/Chat";
import Check from "Check";
import Close from "Close";
import Dashboard from "./Dashboard/index";
import Datasets from "Datasets";
import Desktop from "Desktop";
import FC from "FC";
import Health from "Health";
import Layout from "./Layout";
import LayoutProps from "LayoutProps";
import Local from "Local";
import Logout from "Logout";
import Logs from "../pages/Logs";
import Main from "../Main";
import Menu from "Menu";
import Mobile from "Mobile";
import ModalProps from "ModalProps";
import MuiDrawer from "MuiDrawer";
import Offline from "Offline";
import Psychology from "Psychology";
import ReactNode from "ReactNode";
import Settings from "./Settings/index";
import Sidebar from "./nav/Sidebar";
import Storage from "Storage";
import Theme from "Theme";
import Toggle from "Toggle";
import Unknown from "Unknown";
import Upload from "Upload";
import ZETA from "ZETA";

const drawerWidth = 240;

interface LayoutProps {
  children: React.ReactNode;
  onLogout?: () => void;
}

const Layout: React.FC<LayoutProps> = ({ children, onLogout }) => {
  const [mobileOpen, setMobileOpen] = React.useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  // Health check for connection status
  const { data: health, isError } = useQuery({
    queryKey: queryKeys.health,
    queryFn: () => apiService.getHealth(),
    refetchInterval: 30000, // Check every 30s
  });

  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
    { text: 'AI Assistant', icon: <AssistantIcon />, path: '/assistant' },
    { text: 'Datasets', icon: <DatasetIcon />, path: '/datasets' },
    { text: 'Chat & Upload', icon: <ChatIcon />, path: '/chat' },
    { text: 'Logs', icon: <LogsIcon />, path: '/logs' },
    { text: 'Settings', icon: <SettingsIcon />, path: '/settings' },
  ];

  const handleLogout = () => {
    apiService.clearToken();
    if (onLogout) {
      onLogout();
    }
  };

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleNavigation = (path: string) => {
    navigate(path);
    setMobileOpen(false); // Close mobile drawer
  };

  const drawer = (
    <Box>
      <Toolbar>
        <Typography variant="h6" noWrap component="div">
          ZETA AI
        </Typography>
      </Toolbar>
      <List>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => handleNavigation(item.path)}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  const connectionStatus = isError ? 'Offline' : health?.status || 'Unknown';
  let statusColor: 'error' | 'success' | 'warning' = 'warning';
  if (isError) {
    statusColor = 'error';
  } else if (health?.status === 'healthy') {
    statusColor = 'success';
  }

  return (
    <Box sx={{ display: 'flex' }}>
      {/* App Bar */}
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            ZETA AI Desktop (Local)
          </Typography>
          
          {/* Theme Toggle */}
          <Box sx={{ mr: 1 }}>
            <ThemeToggle size="sm" />
          </Box>
          
          {/* Accessibility Menu */}
          <Box sx={{ mr: 2 }}>
            <AccessibilityMenu />
          </Box>
          
          <Button
            color="inherit"
            startIcon={<LogoutIcon />}
            onClick={handleLogout}
            sx={{ mr: 2 }}
          >
            Đăng xuất
          </Button>
          <Chip
            label={`API: ${connectionStatus}`}
            color={statusColor}
            size="small"
            variant="outlined"
            sx={{ color: 'white', borderColor: 'rgba(255,255,255,0.5)' }}
          />
        </Toolbar>
      </AppBar>

      {/* Sidebar */}
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
        aria-label="main navigation"
      >
        {/* Mobile drawer */}
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        {/* Desktop drawer */}
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      {/* Main content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          mt: '64px', // AppBar height
        }}
      >
        {children}
      </Box>
    </Box>
  );
};

export default Layout;
