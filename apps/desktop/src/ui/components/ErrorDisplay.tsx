import {
    Close as CloseIcon,
    ExpandLess as ExpandLessIcon,
    ExpandMore as ExpandMoreIcon,
    Refresh as RefreshIcon
} from '@mui/icons-material';
import {
    Alert,
    AlertTitle,
    Box,
    Button,
    Collapse,
    IconButton,
    SxProps,
    Theme,
    Typography
} from '@mui/material';
import React from 'react';
import Basic from "Basic";
import Close from "Close";
import Current from "Current";
import Custom from "Custom";
import Error from "Error";
import ErrorBoundaryState from "ErrorBoundaryState";
import ErrorDisplay from "./ErrorDisplay";
import ErrorDisplayProps from "ErrorDisplayProps";
import ExpandLess from "ExpandLess";
import ExpandMore from "ExpandMore";
import FC from "FC";
import Network from "Network";
import Optional from "Optional";
import Refresh from "Refresh";
import Retry from "Retry";
import Severity from "Severity";
import Thu from "Thu";
import Whether from "Whether";
import With from "With";
import Xem from "Xem";

export type ErrorBoundaryState = 'error' | 'loading' | 'retry' | 'success';

export interface ErrorDisplayProps {
  /** Error message to display */
  message: string;
  /** Optional error details */
  details?: string;
  /** Severity level */
  severity?: 'error' | 'warning' | 'info';
  /** Whether to show retry button */
  showRetry?: boolean;
  /** Whether to show close button */
  showClose?: boolean;
  /** Whether to show expand/collapse for details */
  collapsible?: boolean;
  /** Retry handler */
  onRetry?: () => void;
  /** Close handler */
  onClose?: () => void;
  /** Custom styling */
  sx?: SxProps<Theme>;
  /** Current state for loading during retry */
  state?: ErrorBoundaryState;
}

/**
 * Error display component với retry, collapse và các options khác
 * Dùng cho error boundaries, form validation errors, và general error states
 * 
 * @example
 * // Basic error
 * <ErrorDisplay message="Đã có lỗi xảy ra" />
 * 
 * @example
 * // With retry and details
 * <ErrorDisplay 
 *   message="Không thể tải dữ liệu"
 *   details="Network timeout after 30 seconds"
 *   showRetry
 *   onRetry={handleRetry}
 *   collapsible
 * />
 */
export const ErrorDisplay: React.FC<ErrorDisplayProps> = ({
  message,
  details,
  severity = 'error',
  showRetry = false,
  showClose = false,
  collapsible = false,
  onRetry,
  onClose,
  sx,
  state = 'error'
}) => {
  const [expanded, setExpanded] = React.useState(false);

  const handleRetry = () => {
    if (onRetry) {
      onRetry();
    }
  };

  const handleToggleExpand = () => {
    setExpanded(!expanded);
  };

  const actionButtons = (
    <Box display="flex" gap={1} alignItems="center">
      {showRetry && (
        <Button
          size="small"
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={handleRetry}
          disabled={state === 'loading' || state === 'retry'}
        >
          {state === 'loading' || state === 'retry' ? 'Đang thử lại...' : 'Thử lại'}
        </Button>
      )}
      {collapsible && details && (
        <IconButton
          size="small"
          onClick={handleToggleExpand}
          aria-label={expanded ? 'Thu gọn' : 'Xem chi tiết'}
        >
          {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
        </IconButton>
      )}
      {showClose && (
        <IconButton
          size="small"
          onClick={onClose}
          aria-label="Đóng"
        >
          <CloseIcon />
        </IconButton>
      )}
    </Box>
  );

  return (
    <Box sx={sx}>
      <Alert
        severity={severity}
        action={actionButtons}
        sx={{ alignItems: 'flex-start' }}
      >
        <AlertTitle>{message}</AlertTitle>
        {details && !collapsible && (
          <Typography variant="body2" component="div">
            {details}
          </Typography>
        )}
      </Alert>
      
      {collapsible && details && (
        <Collapse in={expanded}>
          <Alert severity="info" sx={{ mt: 1, border: 'none', backgroundColor: 'grey.50' }}>
            <Typography variant="body2" component="pre" sx={{ fontFamily: 'monospace', whiteSpace: 'pre-wrap' }}>
              {details}
            </Typography>
          </Alert>
        </Collapse>
      )}
    </Box>
  );
};

export default ErrorDisplay;
