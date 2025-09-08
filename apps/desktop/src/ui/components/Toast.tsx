import {
    Alert,
    AlertColor,
    Fade,
    Slide,
    Snackbar,
    SxProps,
    Theme
} from '@mui/material';
import { TransitionProps } from '@mui/material/transitions';
import React from 'react';
import Action from "Action";
import Animation from "Animation";
import Custom from "Custom";
import Duration from "Duration";
import Error from "Error";
import Event from "Event";
import FC from "FC";
import FadeTransition from "FadeTransition";
import Handler from "Handler";
import Position from "Position";
import ReactElement from "ReactElement";
import SlideTransition from "SlideTransition";
import Success from "Success";
import SyntheticEvent from "SyntheticEvent";
import Toast from "./Toast";
import ToastProps from "ToastProps";
import TransitionComponent from "TransitionComponent";
import Whether from "Whether";

// Animation transitions
const SlideTransition = React.forwardRef<
  unknown,
  TransitionProps & { children: React.ReactElement<any, any> }
>((props, ref) => <Slide direction="up" ref={ref} {...props} />);

const FadeTransition = React.forwardRef<
  unknown,
  TransitionProps & { children: React.ReactElement<any, any> }
>((props, ref) => <Fade ref={ref} {...props} />);

SlideTransition.displayName = 'SlideTransition';
FadeTransition.displayName = 'FadeTransition';

export interface ToastProps {
  /** Whether toast is open */
  open: boolean;
  /** Toast message */
  message: string;
  /** Toast severity */
  severity?: AlertColor;
  /** Duration in milliseconds (0 = manual close only) */
  duration?: number;
  /** Handler for closing toast */
  onClose: () => void;
  /** Position of toast */
  anchorOrigin?: {
    vertical: 'top' | 'bottom';
    horizontal: 'left' | 'center' | 'right';
  };
  /** Animation transition */
  transition?: 'slide' | 'fade';
  /** Whether to show close button */
  showCloseButton?: boolean;
  /** Custom styling */
  sx?: SxProps<Theme>;
  /** Action button config */
  action?: {
    label: string;
    onClick: () => void;
  };
}

/**
 * Toast notification component với animation và positioning
 * Dùng cho success messages, errors, warnings, và info notifications
 * 
 * @example
 * // Success toast
 * <Toast
 *   open={showSuccess}
 *   message="Đã lưu thành công!"
 *   severity="success"
 *   onClose={() => setShowSuccess(false)}
 * />
 * 
 * @example
 * // Error toast with action
 * <Toast
 *   open={showError}
 *   message="Không thể kết nối server"
 *   severity="error"
 *   duration={0}
 *   action={{ label: "Thử lại", onClick: handleRetry }}
 *   onClose={() => setShowError(false)}
 * />
 */
export const Toast: React.FC<ToastProps> = ({
  open,
  message,
  severity = 'info',
  duration = 6000,
  onClose,
  anchorOrigin = { vertical: 'bottom', horizontal: 'left' },
  transition = 'slide',
  showCloseButton = true,
  sx,
  action
}) => {
  const getTransitionComponent = () => {
    switch (transition) {
      case 'slide':
        return SlideTransition;
      case 'fade':
        return FadeTransition;
      default:
        return undefined;
    }
  };

  const handleClose = (_event?: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === 'clickaway') {
      return;
    }
    onClose();
  };

  return (
    <Snackbar
      open={open}
      autoHideDuration={duration > 0 ? duration : undefined}
      onClose={handleClose}
      anchorOrigin={anchorOrigin}
      TransitionComponent={getTransitionComponent()}
      sx={sx}
    >
      <Alert
        onClose={showCloseButton ? handleClose : undefined}
        severity={severity}
        action={action && (
          <button
            onClick={action.onClick}
            style={{
              background: 'none',
              border: 'none',
              color: 'inherit',
              textDecoration: 'underline',
              cursor: 'pointer',
              fontSize: 'inherit'
            }}
          >
            {action.label}
          </button>
        )}
        sx={{ width: '100%' }}
      >
        {message}
      </Alert>
    </Snackbar>
  );
};

export default Toast;
