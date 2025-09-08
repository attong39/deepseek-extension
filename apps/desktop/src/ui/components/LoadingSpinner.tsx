import { Box, CircularProgress, SxProps, Theme, Typography } from '@mui/material';
import React from 'react';
import Basic from "Basic";
import Color from "Color";
import Custom from "Custom";
import FC from "FC";
import Fullscreen from "Fullscreen";
import Loading from "Loading";
import LoadingSpinner from "./LoadingSpinner";
import LoadingSpinnerProps from "LoadingSpinnerProps";
import Size from "Size";
import Whether from "Whether";
import With from "With";

export interface LoadingSpinnerProps {
  /** Loading message to display */
  message?: string;
  /** Size of the spinner */
  size?: number | string;
  /** Whether to show the component inline or centered */
  variant?: 'inline' | 'fullscreen' | 'centered';
  /** Custom styling */
  sx?: SxProps<Theme>;
  /** Color of the spinner */
  color?: 'primary' | 'secondary' | 'inherit';
  /** Whether to show backdrop for fullscreen variant */
  backdrop?: boolean;
}

/**
 * Loading spinner component với nhiều variants cho các use cases khác nhau
 * 
 * @example
 * // Basic spinner
 * <LoadingSpinner />
 * 
 * @example
 * // With message
 * <LoadingSpinner message="Đang xử lý..." />
 * 
 * @example
 * // Fullscreen with backdrop
 * <LoadingSpinner variant="fullscreen" message="Đang tải dữ liệu..." backdrop />
 */
export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  message,
  size = 40,
  variant = 'inline',
  sx,
  color = 'primary',
  backdrop = false
}) => {
  const getContainerStyles = (): SxProps<Theme> => {
    switch (variant) {
      case 'fullscreen':
        return {
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexDirection: 'column',
          gap: 2,
          zIndex: 9999,
          backgroundColor: backdrop ? 'rgba(0, 0, 0, 0.5)' : 'transparent',
          ...sx
        };
      case 'centered':
        return {
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexDirection: 'column',
          gap: 2,
          minHeight: '200px',
          ...sx
        };
      default:
        return {
          display: 'flex',
          alignItems: 'center',
          gap: 2,
          ...sx
        };
    }
  };

  return (
    <Box sx={getContainerStyles()}>
      <CircularProgress size={size} color={color} />
      {message && (
        <Typography
          variant={variant === 'fullscreen' ? 'h6' : 'body2'}
          color="text.secondary"
          textAlign="center"
        >
          {message}
        </Typography>
      )}
    </Box>
  );
};

export default LoadingSpinner;
