/**
 * Main Dashboard Component
 * Overview của system status và quick actions
 */
import {
    LocalHospital as HealthIcon,
    PlayArrow as PlayIcon,
    Storage as StorageIcon,
    Upload as UploadIcon,
} from '@mui/icons-material';
import {
    Alert,
    Box,
    Button,
    Card,
    CardContent,
    Chip,
    Grid,
    LinearProgress,
    Typography,
} from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import React from 'react';

import { apiService, queryKeys } from '../services/apiService';
import AI from "AI";
import Active from "Active";
import Activity from "Activity";
import All from "All";
import Cards from "Cards";
import Component from "Component";
import Dashboard from "./Dashboard";
import FC from "FC";
import Fetch from "Fetch";
import Files from "Files";
import Header from "Header";
import Health from "Health";
import Jobs from "Jobs";
import KB from "KB";
import LocalHospital from "LocalHospital";
import Main from "../Main";
import Math from "Math";
import More from "More";
import No from "No";
import Notice from "Notice";
import Offline from "Offline";
import Overview from "Overview";
import PlayArrow from "PlayArrow";
import Privacy from "Privacy";
import Quick from "Quick";
import Recent from "Recent";
import Refresh from "Refresh";
import Rules from "Rules";
import Running from "Running";
import Stats from "Stats";
import Status from "./Status";
import Storage from "Storage";
import System from "System";
import Training from "./Training";
import Unknown from "Unknown";
import Upload from "Upload";
import Uploads from "Uploads";
import Version from "Version";
import View from "View";
import ZETA from "ZETA";

const Dashboard: React.FC = () => {
  // Fetch system health
  const { data: health, isLoading: healthLoading, error: healthError } = useQuery({
    queryKey: queryKeys.health,
    queryFn: () => apiService.getHealth(),
    refetchInterval: 30000, // Refresh every 30s
  });

  // Fetch recent training jobs
  const { data: recentJobs = [], isLoading: jobsLoading } = useQuery({
    queryKey: queryKeys.trainingJobs(undefined, 5, 0),
    queryFn: () => apiService.getTrainingJobs(undefined, 5, 0),
    refetchInterval: 5000, // Refresh every 5s
  });

  // Fetch recent uploads
  const { data: recentUploads = [], isLoading: uploadsLoading } = useQuery({
    queryKey: queryKeys.uploads(5, 0),
    queryFn: () => apiService.getUploads(5, 0),
    refetchInterval: 10000,
  });

  const runningJobs = recentJobs.filter(job => job.status === 'running');
  const systemStatus = health?.status === 'healthy' ? 'healthy' : 'warning';

  return (
    <Box sx={{ p: 3 }}>
      {/* Privacy Notice */}
      <Alert severity="info" sx={{ mb: 3 }}>
        🔒 <strong>Privacy Notice:</strong> Ứng dụng này không thu thập dữ liệu cá nhân. 
        Tất cả thông tin chỉ được xử lý locally và trên server của bạn.
      </Alert>

      {/* Header */}
      <Typography variant="h4" gutterBottom>
        ZETA AI Dashboard
      </Typography>

      {/* System Status Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {/* Health Status */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <HealthIcon color={systemStatus === 'healthy' ? 'success' : 'warning'} />
                <Typography variant="h6" sx={{ ml: 1 }}>
                  System Health
                </Typography>
              </Box>
              {healthLoading ? (
                <LinearProgress />
              ) : healthError ? (
                <Chip label="Offline" color="error" />
              ) : (
                <Chip 
                  label={health?.status || 'Unknown'} 
                  color={systemStatus === 'healthy' ? 'success' : 'warning'} 
                />
              )}
              {health && (
                <Typography variant="body2" sx={{ mt: 1 }}>
                  Version: {health.version}
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Storage Stats */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <StorageIcon color="primary" />
                <Typography variant="h6" sx={{ ml: 1 }}>
                  Storage
                </Typography>
              </Box>
              {health && (
                <>
                  <Typography variant="body2">
                    Uploads: {health.services.total_uploads}
                  </Typography>
                  <Typography variant="body2">
                    Training Jobs: {health.services.total_jobs}
                  </Typography>
                  <Typography variant="body2">
                    Rules: {health.services.total_rules}
                  </Typography>
                </>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Running Jobs */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={1}>
                <PlayIcon color="secondary" />
                <Typography variant="h6" sx={{ ml: 1 }}>
                  Active Jobs
                </Typography>
              </Box>
              <Typography variant="h4" color="secondary">
                {runningJobs.length}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Running now
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Quick Upload */}
        <Grid item xs={12} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
              <Box display="flex" alignItems="center" mb={1}>
                <UploadIcon color="info" />
                <Typography variant="h6" sx={{ ml: 1 }}>
                  Quick Upload
                </Typography>
              </Box>
              <Box sx={{ flexGrow: 1, display: 'flex', alignItems: 'center' }}>
                <Button
                  variant="contained"
                  startIcon={<UploadIcon />}
                  fullWidth
                  href="/training"
                >
                  Upload Files
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Recent Activity */}
      <Grid container spacing={3}>
        {/* Recent Training Jobs */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Training Jobs
              </Typography>
              {jobsLoading ? (
                <LinearProgress />
              ) : recentJobs.length === 0 ? (
                <Typography color="textSecondary">No training jobs yet</Typography>
              ) : (
                <Box>
                  {recentJobs.map((job) => (
                    <Box
                      key={job.id}
                      sx={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        py: 1,
                        borderBottom: '1px solid #eee',
                      }}
                    >
                      <Box>
                        <Typography variant="body1">{job.name}</Typography>
                        <Typography variant="body2" color="textSecondary">
                          {new Date(job.created_at).toLocaleString()}
                        </Typography>
                      </Box>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Chip
                          label={job.status}
                          size="small"
                          color={
                            job.status === 'running' ? 'primary' :
                            job.status === 'completed' ? 'success' :
                            job.status === 'failed' ? 'error' : 'default'
                          }
                        />
                        {job.status === 'running' && (
                          <Typography variant="body2">
                            {Math.round(job.progress)}%
                          </Typography>
                        )}
                      </Box>
                    </Box>
                  ))}
                </Box>
              )}
              <Box sx={{ mt: 2 }}>
                <Button variant="outlined" fullWidth href="/training">
                  View All Jobs
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Uploads */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Uploads
              </Typography>
              {uploadsLoading ? (
                <LinearProgress />
              ) : recentUploads.length === 0 ? (
                <Typography color="textSecondary">No uploads yet</Typography>
              ) : (
                <Box>
                  {recentUploads.map((upload) => (
                    <Box
                      key={upload.id}
                      sx={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        py: 1,
                        borderBottom: '1px solid #eee',
                      }}
                    >
                      <Box>
                        <Typography variant="body1">{upload.filename}</Typography>
                        <Typography variant="body2" color="textSecondary">
                          {upload.content_type} • {(upload.size / 1024).toFixed(1)} KB
                        </Typography>
                      </Box>
                      <Typography variant="body2" color="textSecondary">
                        {new Date(upload.upload_time).toLocaleString()}
                      </Typography>
                    </Box>
                  ))}
                </Box>
              )}
              <Box sx={{ mt: 2 }}>
                <Button variant="outlined" fullWidth href="/training">
                  Upload More Files
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
