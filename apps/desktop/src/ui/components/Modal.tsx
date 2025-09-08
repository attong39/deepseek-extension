import { Close as CloseIcon } from '@mui/icons-material';
import {
    Box,
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Fade,
    IconButton,
    Slide,
    SxProps,
    Theme,
    Typography
} from '@mui/material';
import { TransitionProps } from '@mui/material/transitions';
import React from 'react';
import Animation from "Animation";
import Basic from "Basic";
import Close from "Close";
import Custom from "Custom";
import FC from "FC";
import FadeTransition from "FadeTransition";
import FormContent from "FormContent";
import Handler from "Handler";
import MUI from "MUI";
import Modal from "./Modal";
import ModalProps from "ModalProps";
import Prevent from "Prevent";
import Primary from "Primary";
import ReactElement from "ReactElement";
import ReactNode from "ReactNode";
import Secondary from "Secondary";
import SlideTransition from "SlideTransition";
import TransitionComponent from "TransitionComponent";
import Whether from "Whether";
import Wrapper from "Wrapper";

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

export interface ModalProps {
  /** Whether modal is open */
  open: boolean;
  /** Handler for closing modal */
  onClose: () => void;
  /** Modal title */
  title?: string;
  /** Modal content */
  children: React.ReactNode;
  /** Primary action button config */
  primaryAction?: {
    label: string;
    onClick: () => void;
    disabled?: boolean;
    loading?: boolean;
    color?: 'primary' | 'secondary' | 'error' | 'warning' | 'info' | 'success';
  };
  /** Secondary action button config */
  secondaryAction?: {
    label: string;
    onClick: () => void;
    disabled?: boolean;
  };
  /** Whether to show close button */
  showCloseButton?: boolean;
  /** Modal size */
  maxWidth?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | false;
  /** Whether modal is fullscreen */
  fullScreen?: boolean;
  /** Whether modal takes full width */
  fullWidth?: boolean;
  /** Animation transition type */
  transition?: 'slide' | 'fade' | 'none';
  /** Custom styling */
  sx?: SxProps<Theme>;
  /** Whether to disable backdrop click to close */
  disableBackdropClick?: boolean;
  /** Whether to disable escape key to close */
  disableEscapeKeyDown?: boolean;
}

/**
 * Modal component với animation, actions và responsive design
 * Wrapper xung quanh MUI Dialog với presets phổ biến
 * 
 * @example
 * // Basic modal
 * <Modal open={open} onClose={handleClose} title="Xác nhận">
 *   <Typography>Bạn có chắc chắn muốn xóa?</Typography>
 * </Modal>
 * 
 * @example
 * // Modal with actions
 * <Modal
 *   open={open}
 *   onClose={handleClose}
 *   title="Tạo mới"
 *   primaryAction={{ label: "Tạo", onClick: handleCreate, loading: isCreating }}
 *   secondaryAction={{ label: "Hủy", onClick: handleClose }}
 * >
 *   <FormContent />
 * </Modal>
 */
export const Modal: React.FC<ModalProps> = ({
  open,
  onClose,
  title,
  children,
  primaryAction,
  secondaryAction,
  showCloseButton = true,
  maxWidth = 'sm',
  fullScreen = false,
  fullWidth = true,
  transition = 'slide',
  sx,
  disableBackdropClick = false,
  disableEscapeKeyDown = false
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

  const handleClose = (_event: object, reason?: string) => {
    // Prevent closing on backdrop click if disabled
    if (disableBackdropClick && reason === 'backdropClick') {
      return;
    }
    
    // Prevent closing on escape key if disabled
    if (disableEscapeKeyDown && reason === 'escapeKeyDown') {
      return;
    }
    
    onClose();
  };

  return (
    <Dialog
      open={open}
      onClose={handleClose}
      maxWidth={maxWidth}
      fullScreen={fullScreen}
      fullWidth={fullWidth}
      TransitionComponent={getTransitionComponent()}
      sx={sx}
    >
      {title && (
        <DialogTitle>
          <Box display="flex" alignItems="center" justifyContent="space-between">
            <Typography variant="h6" component="span">
              {title}
            </Typography>
            {showCloseButton && (
              <IconButton
                edge="end"
                color="inherit"
                onClick={onClose}
                aria-label="Đóng"
                size="small"
              >
                <CloseIcon />
              </IconButton>
            )}
          </Box>
        </DialogTitle>
      )}
      
      <DialogContent>
        {children}
      </DialogContent>
      
      {(primaryAction || secondaryAction) && (
        <DialogActions>
          {secondaryAction && (
            <Button
              onClick={secondaryAction.onClick}
              disabled={secondaryAction.disabled}
              color="inherit"
            >
              {secondaryAction.label}
            </Button>
          )}
          {primaryAction && (
            <Button
              onClick={primaryAction.onClick}
              disabled={primaryAction.disabled || primaryAction.loading}
              color={primaryAction.color || 'primary'}
              variant="contained"
            >
              {primaryAction.loading ? 'Đang xử lý...' : primaryAction.label}
            </Button>
          )}
        </DialogActions>
      )}
    </Dialog>
  );
};

export default Modal;
