import { Psychology, Send } from '@mui/icons-material';
import {
    Alert,
    Box,
    Button,
    Card,
    CardContent,
    Chip,
    CircularProgress,
    Paper,
    TextField,
    Typography,
} from '@mui/material';
import React, { useState } from 'react';

import type { AssistantResponse } from '../services/apiService';
import { apiService } from '../services/apiService';
import AI from "AI";
import Assistant from "Assistant";
import AssistantPage from "./AssistantPage";
import Context from "../Context/index";
import Error from "Error";
import FormEvent from "FormEvent";
import Local from "Local";
import Metadata from "Metadata";
import Tin from "Tin";

export default function AssistantPage() {
  const [message, setMessage] = useState('');
  const [context, setContext] = useState('');
  const [response, setResponse] = useState<AssistantResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getConfidenceColor = (confidence: number) => {
    if (confidence > 0.8) return 'success';
    if (confidence > 0.5) return 'warning';
    return 'error';
  };

  const getUncertaintyColor = (uncertainty: number) => {
    if (uncertainty < 0.3) return 'success';
    if (uncertainty < 0.6) return 'warning';
    return 'error';
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const result = await apiService.assistantChat(message, context || undefined);
      setResponse(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Có lỗi xảy ra khi gọi AI assistant');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setMessage('');
    setContext('');
    setResponse(null);
    setError(null);
  };

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Psychology />
        AI Assistant (Local)
      </Typography>
      
      <Typography variant="body1" color="text.secondary" gutterBottom>
        Trò chuyện với AI assistant local, bảo mật dữ liệu hoàn toàn
      </Typography>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <TextField
                label="Tin nhắn"
                multiline
                rows={4}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Nhập câu hỏi hoặc yêu cầu của bạn..."
                fullWidth
                required
              />
              
              <TextField
                label="Context (tùy chọn)"
                multiline
                rows={2}
                value={context}
                onChange={(e) => setContext(e.target.value)}
                placeholder="Thêm ngữ cảnh để AI hiểu rõ hơn..."
                fullWidth
              />
              
              <Box sx={{ display: 'flex', gap: 2 }}>
                <Button
                  type="submit"
                  variant="contained"
                  startIcon={loading ? <CircularProgress size={20} /> : <Send />}
                  disabled={loading || !message.trim()}
                >
                  {loading ? 'Đang xử lý...' : 'Gửi'}
                </Button>
                
                <Button
                  type="button"
                  variant="outlined"
                  onClick={handleClear}
                  disabled={loading}
                >
                  Xóa
                </Button>
              </Box>
            </Box>
          </form>
        </CardContent>
      </Card>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {response && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Phản hồi từ AI Assistant
          </Typography>
          
          <Box sx={{ mb: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            <Chip 
              label={`Nguồn: ${response.source}`} 
              variant="outlined" 
              size="small" 
            />
            <Chip 
              label={`Độ tin cậy: ${(response.confidence * 100).toFixed(1)}%`} 
              variant="outlined" 
              size="small"
              color={getConfidenceColor(response.confidence)}
            />
            <Chip 
              label={`Độ không chắc chắn: ${(response.uncertainty * 100).toFixed(1)}%`} 
              variant="outlined" 
              size="small"
              color={getUncertaintyColor(response.uncertainty)}
            />
          </Box>
          
          <Typography variant="body1" sx={{ mb: 2, whiteSpace: 'pre-wrap' }}>
            {response.text}
          </Typography>
          
          {response.metadata && Object.keys(response.metadata).length > 0 && (
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Metadata:
              </Typography>
              <Box component="pre" sx={{ 
                backgroundColor: 'grey.100', 
                p: 1, 
                borderRadius: 1, 
                fontSize: '0.875rem',
                overflow: 'auto'
              }}>
                {JSON.stringify(response.metadata, null, 2)}
              </Box>
            </Box>
          )}
        </Paper>
      )}
    </Box>
  );
}
