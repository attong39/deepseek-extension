/**
 * Settings Page
 * Backend connection status + Rules management + Privacy settings
 */
import {
    Add as AddIcon,
    CheckCircle as CheckIcon,
    Delete as DeleteIcon,
    Edit as EditIcon,
    Error as ErrorIcon,
    Refresh as RefreshIcon,
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
    FormControlLabel,
    Grid,
    IconButton,
    Paper,
    Switch,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    TextField,
    Typography,
} from '@mui/material';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useSnackbar } from 'notistack';
import React, { useState } from 'react';

import type { RuleUpsert } from '../services/apiService';
import { apiService, queryKeys } from '../services/apiService';
import AI from "AI";
import API from "../API/index";
import Actions from "Actions";
import Add from "Add";
import App from "../App";
import Are from "Are";
import Auto from "Auto";
import Backend from "Backend";
import Cancel from "Cancel";
import Check from "Check";
import CheckCircle from "CheckCircle";
import Compliance from "Compliance";
import Connection from "Connection";
import Create from "Create";
import Created from "Created";
import Data from "Data";
import Delete from "Delete";
import Describe from "Describe";
import Description from "Description";
import Desktop from "Desktop";
import Disabled from "Disabled";
import Edit from "Edit";
import Electron from "Electron";
import Enable from "Enable";
import Enabled from "Enabled";
import Error from "Error";
import FC from "FC";
import Failed from "Failed";
import FastAPI from "FastAPI";
import Fetch from "Fetch";
import Frontend from "Frontend";
import Header from "Header";
import Information from "Information";
import Jobs from "Jobs";
import Last from "Last";
import Loading from "Loading";
import Local from "Local";
import Logs from "./Logs";
import Management from "Management";
import Name from "Name";
import New from "New";
import No from "No";
import Notice from "Notice";
import Open from "Open";
import Page from "Page";
import Policy from "Policy";
import Privacy from "Privacy";
import Python from "Python";
import Refresh from "Refresh";
import Rule from "Rule";
import Rules from "Rules";
import Runtime from "Runtime";
import Settings from "./Settings";
import Status from "./Status";
import Storage from "Storage";
import Summary from "Summary";
import System from "System";
import Training from "./Training";
import TypeScript from "TypeScript";
import Update from "Update";
import Uploads from "Uploads";
import Version from "Version";
import ZETA from "ZETA";

const Settings: React.FC = () => {
  const queryClient = useQueryClient();
  const { enqueueSnackbar } = useSnackbar();
  
  const [isRuleDialogOpen, setIsRuleDialogOpen] = useState(false);
  const [editingRule, setEditingRule] = useState<any>(null);
  const [ruleForm, setRuleForm] = useState<RuleUpsert>({
    name: '',
    description: '',
    enabled: true,
    config: {},
  });

  // Fetch health status
  const { data: health, isLoading: healthLoading, error: healthError, refetch: refetchHealth } = useQuery({
    queryKey: queryKeys.health,
    queryFn: () => apiService.getHealth(),
    refetchInterval: 5000,
  });

  // Fetch rules
  const { data: rules = [], isLoading: rulesLoading, refetch: refetchRules } = useQuery({
    queryKey: queryKeys.rules(),
    queryFn: () => apiService.getRules(),
  });

  // Rule mutations
  const createRuleMutation = useMutation({
    mutationFn: (ruleData: RuleUpsert) => apiService.createRule(ruleData),
    onSuccess: () => {
      refetchRules();
      setIsRuleDialogOpen(false);
      resetRuleForm();
      enqueueSnackbar('Rule created successfully', { variant: 'success' });
    },
    onError: (error) => {
      enqueueSnackbar(`Failed to create rule: ${error.message}`, { variant: 'error' });
    },
  });

  const updateRuleMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: RuleUpsert }) => 
      apiService.updateRule(id, data),
    onSuccess: () => {
      refetchRules();
      setIsRuleDialogOpen(false);
      resetRuleForm();
      enqueueSnackbar('Rule updated successfully', { variant: 'success' });
    },
    onError: (error) => {
      enqueueSnackbar(`Failed to update rule: ${error.message}`, { variant: 'error' });
    },
  });

  const deleteRuleMutation = useMutation({
    mutationFn: (ruleId: string) => apiService.deleteRule(ruleId),
    onSuccess: () => {
      refetchRules();
      enqueueSnackbar('Rule deleted successfully', { variant: 'success' });
    },
    onError: (error) => {
      enqueueSnackbar(`Failed to delete rule: ${error.message}`, { variant: 'error' });
    },
  });

  const resetRuleForm = () => {
    setRuleForm({
      name: '',
      description: '',
      enabled: true,
      config: {},
    });
    setEditingRule(null);
  };

  const handleCreateRule = () => {
    setEditingRule(null);
    resetRuleForm();
    setIsRuleDialogOpen(true);
  };

  const handleEditRule = (rule: any) => {
    setEditingRule(rule);
    setRuleForm({
      name: rule.name,
      description: rule.description,
      enabled: rule.enabled,
      config: rule.config,
    });
    setIsRuleDialogOpen(true);
  };

  const handleSaveRule = () => {
    if (!ruleForm.name.trim() || !ruleForm.description.trim()) {
      enqueueSnackbar('Name and description are required', { variant: 'error' });
      return;
    }

    if (editingRule) {
      updateRuleMutation.mutate({ id: editingRule.id, data: ruleForm });
    } else {
      createRuleMutation.mutate(ruleForm);
    }
  };

  const handleDeleteRule = (ruleId: string) => {
    if (window.confirm('Are you sure you want to delete this rule?')) {
      deleteRuleMutation.mutate(ruleId);
    }
  };

  const connectionStatus = healthError ? 'offline' : health?.status === 'healthy' ? 'online' : 'warning';
  const connectionColor = connectionStatus === 'online' ? 'success' : connectionStatus === 'offline' ? 'error' : 'warning';

  return (
    <Box>
      {/* Header */}
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>

      {/* Privacy Notice */}
      <Alert severity="info" sx={{ mb: 3 }}>
        🔒 <strong>Privacy Policy:</strong> ZETA AI không thu thập dữ liệu cá nhân. 
        Tất cả thông tin được xử lý locally và không chia sẻ với bên thứ ba.
      </Alert>

      <Grid container spacing={3}>
        {/* Backend Connection Status */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6">Backend Connection</Typography>
                <Button
                  startIcon={<RefreshIcon />}
                  onClick={() => refetchHealth()}
                  disabled={healthLoading}
                  size="small"
                >
                  Refresh
                </Button>
              </Box>

              <Box display="flex" alignItems="center" gap={1} mb={2}>
                {connectionStatus === 'online' ? (
                  <CheckIcon color="success" />
                ) : (
                  <ErrorIcon color="error" />
                )}
                <Chip
                  label={connectionStatus.toUpperCase()}
                  color={connectionColor}
                  variant="outlined"
                />
              </Box>

              {health && (
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    <strong>API Version:</strong> {health.version}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    <strong>Last Check:</strong> {new Date(health.timestamp).toLocaleString()}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    <strong>Storage:</strong> {health.services.storage}
                  </Typography>
                  
                  <Divider sx={{ my: 1 }} />
                  
                  <Typography variant="body2">
                    <strong>Data Summary:</strong>
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    • Uploads: {health.services.total_uploads}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    • Training Jobs: {health.services.total_jobs}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    • Rules: {health.services.total_rules}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    • Logs: {health.services.total_logs}
                  </Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* System Information */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                System Information
              </Typography>
              <Typography variant="body2" color="text.secondary">
                <strong>Frontend:</strong> React {React.version} + TypeScript
              </Typography>
              <Typography variant="body2" color="text.secondary">
                <strong>Backend:</strong> FastAPI + Python
              </Typography>
              <Typography variant="body2" color="text.secondary">
                <strong>Runtime:</strong> Electron Desktop App
              </Typography>
              <Typography variant="body2" color="text.secondary">
                <strong>Data Storage:</strong> Local processing only
              </Typography>
              
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="h6" gutterBottom>
                Privacy Compliance
              </Typography>
              <Typography variant="body2" color="text.secondary">
                ✅ No external data transmission<br />
                ✅ Local file processing<br />
                ✅ No user tracking<br />
                ✅ Open source code
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Rules Management */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6">Rules Management</Typography>
                <Button
                  startIcon={<AddIcon />}
                  variant="contained"
                  onClick={handleCreateRule}
                >
                  Create Rule
                </Button>
              </Box>

              {rulesLoading ? (
                <Typography>Loading rules...</Typography>
              ) : rules.length === 0 ? (
                <Alert severity="info">
                  No rules configured yet. Create your first rule to get started.
                </Alert>
              ) : (
                <TableContainer component={Paper} variant="outlined">
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Name</TableCell>
                        <TableCell>Description</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Created</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {rules.map((rule) => (
                        <TableRow key={rule.id}>
                          <TableCell>
                            <Typography variant="body2" fontWeight="medium">
                              {rule.name}
                            </Typography>
                          </TableCell>
                          <TableCell>
                            <Typography variant="body2" color="text.secondary">
                              {rule.description}
                            </Typography>
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={rule.enabled ? 'Enabled' : 'Disabled'}
                              color={rule.enabled ? 'success' : 'default'}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            <Typography variant="body2" color="text.secondary">
                              {new Date(rule.created_at).toLocaleDateString()}
                            </Typography>
                          </TableCell>
                          <TableCell>
                            <IconButton
                              size="small"
                              onClick={() => handleEditRule(rule)}
                            >
                              <EditIcon />
                            </IconButton>
                            <IconButton
                              size="small"
                              onClick={() => handleDeleteRule(rule.id)}
                              color="error"
                            >
                              <DeleteIcon />
                            </IconButton>
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

      {/* Rule Dialog */}
      <Dialog 
        open={isRuleDialogOpen} 
        onClose={() => setIsRuleDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          {editingRule ? 'Edit Rule' : 'Create New Rule'}
        </DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Rule Name"
            fullWidth
            variant="outlined"
            value={ruleForm.name}
            onChange={(e) => setRuleForm(prev => ({ ...prev, name: e.target.value }))}
            placeholder="e.g., Auto-save uploads"
          />
          <TextField
            margin="dense"
            label="Description"
            fullWidth
            multiline
            rows={3}
            variant="outlined"
            value={ruleForm.description}
            onChange={(e) => setRuleForm(prev => ({ ...prev, description: e.target.value }))}
            placeholder="Describe what this rule does..."
          />
          <FormControlLabel
            control={
              <Switch
                checked={ruleForm.enabled || false}
                onChange={(e) => setRuleForm(prev => ({ ...prev, enabled: e.target.checked }))}
              />
            }
            label="Enable this rule"
            sx={{ mt: 1 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setIsRuleDialogOpen(false)}>
            Cancel
          </Button>
          <Button 
            onClick={handleSaveRule} 
            variant="contained"
            disabled={createRuleMutation.isPending || updateRuleMutation.isPending}
          >
            {editingRule ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Settings;
