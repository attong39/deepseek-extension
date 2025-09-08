/**
 * Chat Upload Page
 * Chat interface with file upload and rules integration
 */
import {
    AttachFile as AttachFileIcon,
    AudioFile as AudioIcon,
    Close as CloseIcon,
    Delete as DeleteIcon,
    InsertDriveFile as FileIcon,
    Image as ImageIcon,
    Send as SendIcon,
    Psychology as SmartIcon,
    VideoFile as VideoIcon,
} from '@mui/icons-material';
import {
    Alert,
    Box,
    Button,
    Card,
    CardContent,
    Chip,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Divider,
    FormControl,
    Grid,
    IconButton,
    InputLabel,
    LinearProgress,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    MenuItem,
    Paper,
    Select,
    TextField,
    Typography,
} from '@mui/material';
import { useMutation, useQuery } from '@tanstack/react-query';
import { useSnackbar } from 'notistack';
import React, { useRef, useState } from 'react';

import { apiService, queryKeys } from '../services/apiService';
import All from "All";
import Apply from "Apply";
import Assistant from "Assistant";
import AttachFile from "AttachFile";
import Audio from "Audio";
import AudioFile from "AudioFile";
import Available from "Available";
import Bytes from "Bytes";
import ChangeEvent from "ChangeEvent";
import Chat from "./Chat";
import ChatMessage from "ChatMessage";
import ChatUpload from "./ChatUpload";
import Close from "Close";
import Delete from "Delete";
import Documents from "Documents";
import Error from "Error";
import FC from "FC";
import Fetch from "Fetch";
import File from "File";
import FileReader from "FileReader";
import Files from "Files";
import GB from "GB";
import Generate from "Generate";
import HTMLInputElement from "HTMLInputElement";
import Header from "Header";
import History from "History";
import I from "I";
import Image from "Image";
import Images from "Images";
import Input from "Input";
import InsertDriveFile from "InsertDriveFile";
import KB from "KB";
import MB from "MB";
import Math from "Math";
import Message from "Message";
import No from "No";
import Optional from "Optional";
import PDF from "PDF";
import Page from "Page";
import Panel from "Panel";
import Please from "Please";
import Progress from "Progress";
import Psychology from "Psychology";
import Quick from "Quick";
import Reset from "Reset";
import Rule from "Rule";
import Rules from "Rules";
import Selection from "Selection";
import Send from "Send";
import Simulate from "Simulate";
import Start from "Start";
import Supported from "Supported";
import This from "This";
import Type from "Type";
import Upload from "Upload";
import Uploaded from "Uploaded";
import UploadedFile from "UploadedFile";
import Uploading from "Uploading";
import VideoFile from "VideoFile";
import Videos from "Videos";
import View from "View";
import You from "You";
import Your from "Your";

interface UploadedFile {
  file: File;
  preview?: string;
  uploadProgress: number;
  uploaded: boolean;
  fileId?: string;
}

interface ChatMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  files?: string[];
  rule?: string;
}

const ChatUpload: React.FC = () => {
  const { enqueueSnackbar } = useSnackbar();
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const [message, setMessage] = useState('');
  const [selectedRule, setSelectedRule] = useState('');
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [isRuleDialogOpen, setIsRuleDialogOpen] = useState(false);

  // Fetch available rules
  const { data: rules = [] } = useQuery({
    queryKey: queryKeys.rules(),
    queryFn: () => apiService.getRules(),
  });

  // File upload mutation
  const uploadMutation = useMutation({
    mutationFn: (file: File) => apiService.uploadFile(file),
    onSuccess: (result, file) => {
      setFiles(prev => prev.map(f => 
        f.file === file 
          ? { ...f, uploaded: true, uploadProgress: 100, fileId: result.id || 'unknown' }
          : f
      ));
      enqueueSnackbar(`File "${file.name}" uploaded successfully`, { variant: 'success' });
    },
    onError: (error, file) => {
      enqueueSnackbar(`Upload failed for "${file.name}": ${(error as Error).message}`, { variant: 'error' });
      setFiles(prev => prev.filter(f => f.file !== file));
    },
  });

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(event.target.files || []);
    
    const newFiles: UploadedFile[] = selectedFiles.map(file => {
      const uploadedFile: UploadedFile = {
        file,
        uploadProgress: 0,
        uploaded: false,
      };

      // Generate preview for images
      if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const result = e.target?.result as string;
          setFiles(prev => prev.map(f => 
            f.file === file 
              ? { ...f, preview: result }
              : f
          ));
        };
        reader.readAsDataURL(file);
      }

      return uploadedFile;
    });

    setFiles(prev => [...prev, ...newFiles]);

    // Start uploading files
    newFiles.forEach(fileWrapper => {
      uploadMutation.mutate(fileWrapper.file);
    });
  };

  const handleRemoveFile = (fileToRemove: UploadedFile) => {
    setFiles(prev => prev.filter(f => f.file !== fileToRemove.file));
  };

  const handleSendMessage = () => {
    if (!message.trim() && files.length === 0) {
      enqueueSnackbar('Please enter a message or upload files', { variant: 'warning' });
      return;
    }

    const uploadedFileIds = files.filter(f => f.uploaded).map(f => f.fileId!);
    
    const newMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: message,
      timestamp: new Date(),
      files: uploadedFileIds.length > 0 ? uploadedFileIds : undefined,
      rule: selectedRule || undefined,
    };

    setChatHistory(prev => [...prev, newMessage]);

    // Simulate assistant response
    setTimeout(() => {
      const filesText = uploadedFileIds.length > 0 ? ` with ${uploadedFileIds.length} file(s)` : '';
      const ruleText = selectedRule ? ` using rule "${selectedRule}"` : '';
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: `I received your message${filesText}${ruleText}. This is a simulated response.`,
        timestamp: new Date(),
      };
      setChatHistory(prev => [...prev, assistantMessage]);
    }, 1000);

    // Reset form
    setMessage('');
    setFiles([]);
    setSelectedRule('');
  };

  const getFileIcon = (fileType: string) => {
    if (fileType.startsWith('image/')) return <ImageIcon />;
    if (fileType.startsWith('video/')) return <VideoIcon />;
    if (fileType.startsWith('audio/')) return <AudioIcon />;
    return <FileIcon />;
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <Box>
      {/* Header */}
      <Typography variant="h4" gutterBottom>
        Chat & Upload
      </Typography>

      <Grid container spacing={3}>
        {/* Chat History */}
        <Grid item xs={12} md={8}>
          <Card sx={{ height: 500, display: 'flex', flexDirection: 'column' }}>
            <CardContent sx={{ flexGrow: 1, overflow: 'auto' }}>
              <Typography variant="h6" gutterBottom>
                Chat History
              </Typography>
              
              {chatHistory.length === 0 ? (
                <Alert severity="info">
                  Start a conversation by typing a message or uploading files below.
                </Alert>
              ) : (
                <Box>
                  {chatHistory.map((msg) => (
                    <Paper
                      key={msg.id}
                      sx={{
                        p: 2,
                        mb: 2,
                        ml: msg.type === 'user' ? 4 : 0,
                        mr: msg.type === 'assistant' ? 4 : 0,
                        bgcolor: msg.type === 'user' ? 'primary.light' : 'grey.100',
                        color: msg.type === 'user' ? 'white' : 'text.primary',
                      }}
                    >
                      <Typography variant="body2" sx={{ mb: 1 }}>
                        <strong>{msg.type === 'user' ? 'You' : 'Assistant'}</strong>
                        <Typography component="span" sx={{ ml: 2, fontSize: '0.8em', opacity: 0.7 }}>
                          {msg.timestamp.toLocaleTimeString()}
                        </Typography>
                      </Typography>
                      
                      <Typography variant="body1" sx={{ mb: 1 }}>
                        {msg.content}
                      </Typography>
                      
                      {msg.files && msg.files.length > 0 && (
                        <Box sx={{ mt: 1 }}>
                          {msg.files.map((fileId) => (
                            <Chip
                              key={fileId}
                              label={`File: ${fileId}`}
                              size="small"
                              sx={{ mr: 1, mb: 0.5 }}
                            />
                          ))}
                        </Box>
                      )}
                      
                      {msg.rule && (
                        <Chip
                          icon={<SmartIcon />}
                          label={`Rule: ${msg.rule}`}
                          size="small"
                          color="secondary"
                          sx={{ mt: 1 }}
                        />
                      )}
                    </Paper>
                  ))}
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Input Panel */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Send Message
              </Typography>

              {/* Rule Selection */}
              <FormControl fullWidth sx={{ mb: 2 }} size="small">
                <InputLabel>Apply Rule (Optional)</InputLabel>
                <Select
                  value={selectedRule}
                  label="Apply Rule (Optional)"
                  onChange={(e) => setSelectedRule(e.target.value)}
                >
                  <MenuItem value="">No Rule</MenuItem>
                  {rules.map((rule) => (
                    <MenuItem key={rule.id} value={rule.name}>
                      {rule.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              {/* Message Input */}
              <TextField
                fullWidth
                multiline
                rows={4}
                label="Your message"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                sx={{ mb: 2 }}
                placeholder="Type your message here..."
              />

              {/* File Upload */}
              <Box sx={{ mb: 2 }}>
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileSelect}
                  multiple
                  style={{ display: 'none' }}
                  accept="image/*,video/*,audio/*,.pdf,.doc,.docx,.txt"
                />
                <Button
                  variant="outlined"
                  startIcon={<AttachFileIcon />}
                  onClick={() => fileInputRef.current?.click()}
                  fullWidth
                  sx={{ mb: 1 }}
                >
                  Upload Files
                </Button>
                
                <Typography variant="caption" color="text.secondary">
                  Supported: Images, Videos, Audio, PDF, Documents
                </Typography>
              </Box>

              {/* File List */}
              {files.length > 0 && (
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Uploaded Files ({files.length})
                  </Typography>
                  <List dense>
                    {files.map((fileWrapper) => (
                      <ListItem
                        key={`${fileWrapper.file.name}-${fileWrapper.file.size}`}
                        secondaryAction={
                          <IconButton 
                            edge="end" 
                            size="small"
                            onClick={() => handleRemoveFile(fileWrapper)}
                          >
                            {fileWrapper.uploaded ? <DeleteIcon /> : <CloseIcon />}
                          </IconButton>
                        }
                      >
                        <ListItemIcon>
                          {getFileIcon(fileWrapper.file.type)}
                        </ListItemIcon>
                        <ListItemText
                          primary={fileWrapper.file.name}
                          secondary={`${formatFileSize(fileWrapper.file.size)} • ${fileWrapper.uploaded ? 'Uploaded' : 'Uploading...'}`}
                        />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}

              {/* Upload Progress */}
              {files.some(f => !f.uploaded) && (
                <Box sx={{ mb: 2 }}>
                  <Typography variant="caption">Uploading files...</Typography>
                  <LinearProgress />
                </Box>
              )}

              {/* Send Button */}
              <Button
                variant="contained"
                fullWidth
                startIcon={<SendIcon />}
                onClick={handleSendMessage}
                disabled={uploadMutation.isPending || files.some(f => !f.uploaded)}
              >
                Send Message
              </Button>
            </CardContent>
          </Card>

          {/* Quick Rules */}
          <Card sx={{ mt: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quick Rules
              </Typography>
              
              {rules.slice(0, 3).map((rule) => (
                <Box key={rule.id} sx={{ mb: 1 }}>
                  <Button
                    variant="outlined"
                    size="small"
                    fullWidth
                    onClick={() => setSelectedRule(rule.name)}
                    sx={{ justifyContent: 'flex-start', textAlign: 'left' }}
                  >
                    <SmartIcon sx={{ mr: 1, fontSize: 16 }} />
                    {rule.name}
                  </Button>
                </Box>
              ))}
              
              <Divider sx={{ my: 1 }} />
              
              <Button
                variant="text"
                size="small"
                fullWidth
                onClick={() => setIsRuleDialogOpen(true)}
              >
                View All Rules
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Rules Dialog */}
      <Dialog 
        open={isRuleDialogOpen} 
        onClose={() => setIsRuleDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Available Rules
          <IconButton
            aria-label="close"
            onClick={() => setIsRuleDialogOpen(false)}
            sx={{ position: 'absolute', right: 8, top: 8 }}
          >
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent>
          <List>
            {rules.map((rule) => (
              <ListItem
                key={rule.id}
                component="div"
                onClick={() => {
                  setSelectedRule(rule.name);
                  setIsRuleDialogOpen(false);
                }}
                sx={{ cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }}
              >
                <ListItemIcon>
                  <SmartIcon />
                </ListItemIcon>
                <ListItemText
                  primary={rule.name}
                  secondary={rule.description}
                />
              </ListItem>
            ))}
          </List>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setIsRuleDialogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ChatUpload;
