/**
 * Training Panel Component
 * Upload files + training job management
 */
import {
    Add as AddIcon,
    Stop as CancelIcon,
    Pause as PauseIcon,
    PlayArrow as PlayIcon,
    Refresh as RefreshIcon,
    CloudUpload as UploadIcon,
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
    Grid,
    IconButton,
    LinearProgress,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    TextField,
    Typography
} from '@mui/material';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';

import { apiService, queryKeys, TrainingJobCreate } from '../services/apiService';
import Actions from "Actions";
import Add from "Add";
import Area from "Area";
import Audio from "Audio";
import Auto from "Auto";
import Cancel from "Cancel";
import Classification from "Classification";
import CloudUpload from "CloudUpload";
import Component from "Component";
import Create from "Create";
import Documents from "Documents";
import Drag from "Drag";
import Drop from "Drop";
import FC from "FC";
import Fetch from "Fetch";
import File from "File";
import Header from "Header";
import Image from "Image";
import Images from "Images";
import Job from "Job";
import Jobs from "Jobs";
import KB from "KB";
import Math from "Math";
import Model from "Model";
import Name from "Name";
import New from "New";
import No from "No";
import Notice from "Notice";
import Or from "Or";
import Panel from "Panel";
import Pause from "Pause";
import PlayArrow from "PlayArrow";
import Privacy from "Privacy";
import Progress from "Progress";
import Recent from "Recent";
import Refresh from "Refresh";
import Status from "./Status";
import Stop from "Stop";
import Support from "Support";
import Training from "./Training";
import TrainingPanel from "./TrainingPanel";
import Upload from "Upload";
import Uploaded from "Uploaded";
import Uploading from "Uploading";
import Uploads from "Uploads";
import Video from "Video";

const TrainingPanel: React.FC = () => {
  const queryClient = useQueryClient();
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [newJobName, setNewJobName] = useState('');
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);

  // Fetch training jobs
  const { data: trainingJobs = [], isLoading: jobsLoading, refetch: refetchJobs } = useQuery({
    queryKey: queryKeys.trainingJobs(),
    queryFn: () => apiService.getTrainingJobs(),
    refetchInterval: 3000, // Auto-refresh every 3s
  });

  // Fetch uploads
  const { data: uploads = [], refetch: refetchUploads } = useQuery({
    queryKey: queryKeys.uploads(),
    queryFn: () => apiService.getUploads(),
  });

  // File upload mutation
  const uploadMutation = useMutation({
    mutationFn: ({ file, description }: { file: File; description?: string }) =>
      apiService.uploadFile(file, description),
    onSuccess: () => {
      setUploadStatus('Upload successful!');
      refetchUploads();
      setTimeout(() => setUploadStatus(null), 3000);
    },
    onError: (error) => {
      setUploadStatus(`Upload failed: ${error.message}`);
      setTimeout(() => setUploadStatus(null), 5000);
    },
  });

  // Training job mutations
  const createJobMutation = useMutation({
    mutationFn: (jobData: TrainingJobCreate) => apiService.createTrainingJob(jobData),
    onSuccess: () => {
      setIsCreateDialogOpen(false);
      setNewJobName('');
      refetchJobs();
    },
  });

  const startJobMutation = useMutation({
    mutationFn: (jobId: string) => apiService.startTrainingJob(jobId),
    onSuccess: () => refetchJobs(),
  });

  const pauseJobMutation = useMutation({
    mutationFn: (jobId: string) => apiService.pauseTrainingJob(jobId),
    onSuccess: () => refetchJobs(),
  });

  const cancelJobMutation = useMutation({
    mutationFn: (jobId: string) => apiService.cancelTrainingJob(jobId),
    onSuccess: () => refetchJobs(),
  });

  // File drop handler
  const onDrop = useCallback((acceptedFiles: File[]) => {
    acceptedFiles.forEach((file) => {
      uploadMutation.mutate({ file });
    });
  }, [uploadMutation]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.bmp'],
      'audio/*': ['.mp3', '.wav', '.ogg', '.m4a'],
      'video/*': ['.mp4', '.avi', '.mov', '.mkv'],
      'text/*': ['.txt', '.csv', '.json'],
      'application/pdf': ['.pdf'],
    },
    multiple: true,
  });

  const handleCreateJob = () => {
    if (newJobName.trim()) {
      createJobMutation.mutate({
        name: newJobName.trim(),
        config: { auto_start: false },
      });
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'primary';
      case 'completed': return 'success';
      case 'failed': return 'error';
      case 'cancelled': return 'warning';
      case 'paused': return 'info';
      default: return 'default';
    }
  };

  const canStart = (status: string) => ['created', 'paused'].includes(status);
  const canPause = (status: string) => status === 'running';
  const canCancel = (status: string) => ['created', 'running', 'paused'].includes(status);

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Training & Upload</Typography>
        <Box gap={1} display="flex">
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={() => {
              refetchJobs();
              refetchUploads();
            }}
          >
            Refresh
          </Button>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setIsCreateDialogOpen(true)}
          >
            New Training Job
          </Button>
        </Box>
      </Box>

      {/* Upload Status */}
      {uploadStatus && (
        <Alert 
          severity={uploadStatus.includes('failed') ? 'error' : 'success'} 
          sx={{ mb: 3 }}
        >
          {uploadStatus}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* File Upload Area */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                File Upload
              </Typography>
              
              <Box
                {...getRootProps()}
                sx={{
                  border: '2px dashed #ccc',
                  borderRadius: 2,
                  p: 4,
                  textAlign: 'center',
                  cursor: 'pointer',
                  backgroundColor: isDragActive ? 'action.hover' : 'background.paper',
                  '&:hover': { backgroundColor: 'action.hover' },
                }}
              >
                <input {...getInputProps()} />
                <UploadIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  {isDragActive ? 'Drop files here' : 'Drag & drop files here'}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Support: Images, Audio, Video, Documents
                </Typography>
                <Button variant="outlined" startIcon={<UploadIcon />}>
                  Or click to select files
                </Button>
              </Box>

              {uploadMutation.isPending && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="body2" gutterBottom>
                    Uploading...
                  </Typography>
                  <LinearProgress />
                </Box>
              )}

              {/* Recent Uploads */}
              <Typography variant="h6" sx={{ mt: 3, mb: 2 }}>
                Recent Uploads ({uploads.length})
              </Typography>
              <Box sx={{ maxHeight: 200, overflow: 'auto' }}>
                {uploads.slice(0, 5).map((upload) => (
                  <Box
                    key={upload.id}
                    sx={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      p: 1,
                      borderBottom: '1px solid #eee',
                    }}
                  >
                    <Box>
                      <Typography variant="body2">{upload.filename}</Typography>
                      <Typography variant="caption" color="text.secondary">
                        {upload.content_type} • {(upload.size / 1024).toFixed(1)} KB
                      </Typography>
                    </Box>
                    <Typography variant="caption" color="text.secondary">
                      {new Date(upload.upload_time).toLocaleString()}
                    </Typography>
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Training Jobs */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Training Jobs ({trainingJobs.length})
              </Typography>

              {jobsLoading ? (
                <LinearProgress />
              ) : trainingJobs.length === 0 ? (
                <Typography color="text.secondary" textAlign="center" py={4}>
                  No training jobs yet. Create one to get started!
                </Typography>
              ) : (
                <TableContainer component={Paper} variant="outlined">
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Name</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Progress</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {trainingJobs.map((job) => (
                        <TableRow key={job.id}>
                          <TableCell>
                            <Typography variant="body2">{job.name}</Typography>
                            <Typography variant="caption" color="text.secondary">
                              {new Date(job.created_at).toLocaleString()}
                            </Typography>
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={job.status}
                              size="small"
                              color={getStatusColor(job.status)}
                            />
                          </TableCell>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              {job.status === 'running' && (
                                <LinearProgress
                                  variant="determinate"
                                  value={job.progress}
                                  sx={{ width: 60 }}
                                />
                              )}
                              <Typography variant="body2">
                                {Math.round(job.progress)}%
                              </Typography>
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Box gap={0.5} display="flex">
                              <IconButton
                                size="small"
                                disabled={!canStart(job.status) || startJobMutation.isPending}
                                onClick={() => startJobMutation.mutate(job.id)}
                              >
                                <PlayIcon />
                              </IconButton>
                              <IconButton
                                size="small"
                                disabled={!canPause(job.status) || pauseJobMutation.isPending}
                                onClick={() => pauseJobMutation.mutate(job.id)}
                              >
                                <PauseIcon />
                              </IconButton>
                              <IconButton
                                size="small"
                                disabled={!canCancel(job.status) || cancelJobMutation.isPending}
                                onClick={() => cancelJobMutation.mutate(job.id)}
                              >
                                <CancelIcon />
                              </IconButton>
                            </Box>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Create Job Dialog */}
      <Dialog open={isCreateDialogOpen} onClose={() => setIsCreateDialogOpen(false)}>
        <DialogTitle>Create New Training Job</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Job Name"
            fullWidth
            variant="outlined"
            value={newJobName}
            onChange={(e) => setNewJobName(e.target.value)}
            placeholder="e.g., Image Classification Model"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setIsCreateDialogOpen(false)}>Cancel</Button>
          <Button 
            onClick={handleCreateJob} 
            variant="contained"
            disabled={!newJobName.trim() || createJobMutation.isPending}
          >
            Create Job
          </Button>
        </DialogActions>
      </Dialog>

      {/* Privacy Notice */}
      <Alert severity="info" sx={{ mt: 3 }}>
        🔒 <strong>Privacy:</strong> Uploaded files được xử lý locally, không chia sẻ với third parties.
      </Alert>
    </Box>
  );
};

export default TrainingPanel;
