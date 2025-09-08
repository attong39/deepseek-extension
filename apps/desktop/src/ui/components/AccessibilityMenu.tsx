import {
    Accessibility as AccessibilityIcon,
    Contrast as ContrastIcon,
    VisibilityOff as ReduceMotionIcon,
    TextFields as TextIcon,
    KeyboardVoice as VoiceIcon,
    ZoomIn as ZoomIcon
} from '@mui/icons-material';
import {
    Alert,
    Box,
    Button,
    Divider,
    FormControlLabel,
    IconButton,
    Popover,
    Switch,
    Typography
} from '@mui/material';
import React from 'react';
import Accessibility from "Accessibility";
import AccessibilityMenu from "./AccessibilityMenu";
import AccessibilityMenuProps from "AccessibilityMenuProps";
import Apply from "Apply";
import Bao from "Bao";
import Basic from "Basic";
import ChangeEvent from "ChangeEvent";
import Contrast from "Contrast";
import Custom from "Custom";
import FC from "FC";
import Focus from "Focus";
import Font from "Font";
import HTMLElement from "HTMLElement";
import HTMLInputElement from "HTMLInputElement";
import High from "High";
import KeyboardVoice from "KeyboardVoice";
import MouseEvent from "MouseEvent";
import Reduce from "Reduce";
import Reset from "Reset";
import Screen from "Screen";
import Settings from "../../pages/Settings";
import Size from "Size";
import TextFields from "TextFields";
import Toggle from "Toggle";
import VisibilityOff from "VisibilityOff";
import Whether from "Whether";
import ZoomIn from "ZoomIn";

export interface AccessibilityMenuProps {
  /** Custom styling */
  sx?: object;
  /** Whether to show as button or icon only */
  variant?: 'button' | 'icon';
}

/**
 * Accessibility menu component với các tùy chọn hỗ trợ người dùng
 * Bao gồm: font size, contrast, motion reduction, screen reader support
 * 
 * @example
 * // Basic accessibility menu
 * <AccessibilityMenu />
 * 
 * @example
 * // Button variant
 * <AccessibilityMenu variant="button" />
 */
export const AccessibilityMenu: React.FC<AccessibilityMenuProps> = ({
  sx,
  variant = 'icon'
}) => {
  const [anchorEl, setAnchorEl] = React.useState<HTMLElement | null>(null);
  const [settings, setSettings] = React.useState({
    fontSize: 'normal',
    highContrast: false,
    reduceMotion: false,
    screenReader: false,
    keyboardNavigation: true
  });

  const open = Boolean(anchorEl);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleSettingChange = (setting: keyof typeof settings) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const newSettings = { ...settings, [setting]: event.target.checked };
    setSettings(newSettings);
    
    // Apply accessibility settings to document
    applyAccessibilitySettings(newSettings);
  };

  const handleFontSizeChange = (size: string) => {
    const newSettings = { ...settings, fontSize: size };
    setSettings(newSettings);
    applyAccessibilitySettings(newSettings);
  };

  const applyAccessibilitySettings = (newSettings: typeof settings) => {
    const root = document.documentElement;
    
    // Font size
    switch (newSettings.fontSize) {
      case 'small':
        root.style.setProperty('--accessibility-font-scale', '0.9');
        break;
      case 'large':
        root.style.setProperty('--accessibility-font-scale', '1.2');
        break;
      case 'extra-large':
        root.style.setProperty('--accessibility-font-scale', '1.4');
        break;
      default:
        root.style.setProperty('--accessibility-font-scale', '1');
    }
    
    // High contrast
    if (newSettings.highContrast) {
      root.classList.add('high-contrast');
    } else {
      root.classList.remove('high-contrast');
    }
    
    // Reduce motion
    if (newSettings.reduceMotion) {
      root.style.setProperty('--accessibility-motion', 'none');
      root.classList.add('reduce-motion');
    } else {
      root.style.setProperty('--accessibility-motion', 'normal');
      root.classList.remove('reduce-motion');
    }
    
    // Screen reader announcements
    if (newSettings.screenReader) {
      announceToScreenReader('Cài đặt accessibility đã được cập nhật');
    }
  };

  const announceToScreenReader = (message: string) => {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.style.position = 'absolute';
    announcement.style.left = '-10000px';
    announcement.style.width = '1px';
    announcement.style.height = '1px';
    announcement.style.overflow = 'hidden';
    announcement.textContent = message;
    
    document.body.appendChild(announcement);
    setTimeout(() => document.body.removeChild(announcement), 1000);
  };

  const resetSettings = () => {
    const defaultSettings = {
      fontSize: 'normal',
      highContrast: false,
      reduceMotion: false,
      screenReader: false,
      keyboardNavigation: true
    };
    setSettings(defaultSettings);
    applyAccessibilitySettings(defaultSettings);
    announceToScreenReader('Đã reset cài đặt accessibility về mặc định');
  };

  return (
    <>
      {variant === 'button' ? (
        <Button
          startIcon={<AccessibilityIcon />}
          onClick={handleClick}
          aria-label="Mở menu accessibility"
          sx={sx}
        >
          Accessibility
        </Button>
      ) : (
        <IconButton
          onClick={handleClick}
          aria-label="Mở menu accessibility"
          sx={sx}
        >
          <AccessibilityIcon />
        </IconButton>
      )}

      <Popover
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
      >
        <Box sx={{ p: 2, minWidth: 280, maxWidth: 350 }}>
          <Typography variant="h6" gutterBottom>
            <AccessibilityIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
            Accessibility Settings
          </Typography>
          
          <Alert severity="info" sx={{ mb: 2, fontSize: '0.875rem' }}>
            Các cài đặt này giúp cải thiện trải nghiệm cho người dùng có nhu cầu đặc biệt
          </Alert>

          {/* Font Size */}
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle2" gutterBottom>
              <TextIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
              Kích thước font
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              {[
                { value: 'small', label: 'Nhỏ' },
                { value: 'normal', label: 'Bình thường' },
                { value: 'large', label: 'Lớn' },
                { value: 'extra-large', label: 'Rất lớn' }
              ].map((option) => (
                <Button
                  key={option.value}
                  size="small"
                  variant={settings.fontSize === option.value ? 'contained' : 'outlined'}
                  onClick={() => handleFontSizeChange(option.value)}
                >
                  {option.label}
                </Button>
              ))}
            </Box>
          </Box>

          <Divider sx={{ my: 2 }} />

          {/* Toggle Settings */}
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
            <FormControlLabel
              control={
                <Switch
                  checked={settings.highContrast}
                  onChange={handleSettingChange('highContrast')}
                />
              }
              label={
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <ContrastIcon sx={{ mr: 1 }} />
                  Chế độ tương phản cao
                </Box>
              }
            />

            <FormControlLabel
              control={
                <Switch
                  checked={settings.reduceMotion}
                  onChange={handleSettingChange('reduceMotion')}
                />
              }
              label={
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <ReduceMotionIcon sx={{ mr: 1 }} />
                  Giảm animation
                </Box>
              }
            />

            <FormControlLabel
              control={
                <Switch
                  checked={settings.screenReader}
                  onChange={handleSettingChange('screenReader')}
                />
              }
              label={
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <VoiceIcon sx={{ mr: 1 }} />
                  Hỗ trợ screen reader
                </Box>
              }
            />

            <FormControlLabel
              control={
                <Switch
                  checked={settings.keyboardNavigation}
                  onChange={handleSettingChange('keyboardNavigation')}
                />
              }
              label={
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <ZoomIcon sx={{ mr: 1 }} />
                  Focus indicators rõ ràng
                </Box>
              }
            />
          </Box>

          <Divider sx={{ my: 2 }} />

          <Button
            fullWidth
            variant="outlined"
            onClick={resetSettings}
            size="small"
          >
            Reset về mặc định
          </Button>
        </Box>
      </Popover>
    </>
  );
};

export default AccessibilityMenu;
