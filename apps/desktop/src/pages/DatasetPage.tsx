import {
    Add,
    Delete,
    Edit,
    Lock,
    LockOpen,
    Storage,
} from '@mui/icons-material';
import {
    Alert,
    Box,
    Button,
    Card,
    CardContent,
    Chip,
    CircularProgress,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    FormControlLabel,
    Grid,
    IconButton,
    Paper,
    Switch,
    TextField,
    Typography,
} from '@mui/material';
import { useEffect, useState } from 'react';

import type { CreateDatasetRequest, Dataset, UpdateDatasetRequest } from '../services/apiService';
import { apiService } from '../services/apiService';
import Access from "Access";
import Create from "Create";
import DatasetPage from "./DatasetPage";
import Error from "Error";
import ID from "ID";
import Locked from "Locked";
import Management from "Management";
import Open from "Open";
import Team from "Team";
import Update from "Update";
import VN from "VN";

export default function DatasetPage() {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingDataset, setEditingDataset] = useState<Dataset | null>(null);
  const [formData, setFormData] = useState<CreateDatasetRequest>({
    name: '',
    description: '',
    team_locked: false,
  });

  const loadDatasets = async () => {
    try {
      setLoading(true);
      const result = await apiService.getDatasets();
      setDatasets(result);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Không thể tải danh sách datasets');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDatasets();
  }, []);

  const handleOpenDialog = (dataset?: Dataset) => {
    if (dataset) {
      setEditingDataset(dataset);
      setFormData({
        name: dataset.name,
        description: dataset.description,
        team_locked: dataset.team_locked,
      });
    } else {
      setEditingDataset(null);
      setFormData({
        name: '',
        description: '',
        team_locked: false,
      });
    }
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setEditingDataset(null);
    setFormData({
      name: '',
      description: '',
      team_locked: false,
    });
  };

  const handleSubmit = async () => {
    try {
      if (editingDataset) {
        // Update existing dataset
        const updateData: UpdateDatasetRequest = {
          name: formData.name,
          description: formData.description,
        };
        if (formData.team_locked !== undefined) {
          updateData.team_locked = formData.team_locked;
        }
        await apiService.updateDataset(editingDataset.id, updateData);
      } else {
        // Create new dataset
        await apiService.createDataset(formData);
      }
      
      handleCloseDialog();
      await loadDatasets();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Không thể lưu dataset');
    }
  };

  const handleDelete = async (dataset: Dataset) => {
    if (!window.confirm(`Bạn có chắc chắn muốn xóa dataset "${dataset.name}"?`)) {
      return;
    }

    try {
      await apiService.deleteDataset(dataset.id);
      await loadDatasets();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Không thể xóa dataset');
    }
  };

  const getRoleColor = (role: string) => {
    switch (role.toLowerCase()) {
      case 'owner': return 'error';
      case 'admin': return 'warning';
      case 'engineer': return 'info';
      case 'trainer_external': return 'success';
      default: return 'default';
    }
  };

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Storage />
          Dataset Management
        </Typography>
        
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpenDialog()}
        >
          Tạo Dataset Mới
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <Grid container spacing={3}>
          {datasets.map((dataset) => (
            <Grid item xs={12} md={6} lg={4} key={dataset.id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Typography variant="h6" component="h2">
                      {dataset.name}
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <IconButton
                        size="small"
                        onClick={() => handleOpenDialog(dataset)}
                        color="primary"
                      >
                        <Edit />
                      </IconButton>
                      <IconButton
                        size="small"
                        onClick={() => handleDelete(dataset)}
                        color="error"
                      >
                        <Delete />
                      </IconButton>
                    </Box>
                  </Box>
                  
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {dataset.description}
                  </Typography>
                  
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
                    <Chip
                      icon={dataset.team_locked ? <Lock /> : <LockOpen />}
                      label={dataset.team_locked ? 'Team Locked' : 'Open Access'}
                      size="small"
                      color={dataset.team_locked ? 'error' : 'success'}
                      variant="outlined"
                    />
                    <Chip
                      label={dataset.creator_role}
                      size="small"
                      color={getRoleColor(dataset.creator_role)}
                      variant="outlined"
                    />
                  </Box>
                  
                  <Paper sx={{ p: 1, backgroundColor: 'grey.50' }}>
                    <Typography variant="caption" display="block">
                      <strong>ID:</strong> {dataset.id}
                    </Typography>
                    <Typography variant="caption" display="block">
                      <strong>Tạo:</strong> {new Date(dataset.created_at).toLocaleString('vi-VN')}
                    </Typography>
                    <Typography variant="caption" display="block">
                      <strong>Cập nhật:</strong> {new Date(dataset.updated_at).toLocaleString('vi-VN')}
                    </Typography>
                  </Paper>
                </CardContent>
              </Card>
            </Grid>
          ))}
          
          {datasets.length === 0 && (
            <Grid item xs={12}>
              <Paper sx={{ p: 4, textAlign: 'center' }}>
                <Storage sx={{ fontSize: 64, color: 'grey.400', mb: 2 }} />
                <Typography variant="h6" color="text.secondary" gutterBottom>
                  Chưa có dataset nào
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Tạo dataset đầu tiên để bắt đầu quản lý dữ liệu training
                </Typography>
              </Paper>
            </Grid>
          )}
        </Grid>
      )}

      {/* Create/Edit Dialog */}
      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingDataset ? 'Chỉnh sửa Dataset' : 'Tạo Dataset Mới'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
            <TextField
              label="Tên Dataset"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              fullWidth
              required
            />
            
            <TextField
              label="Mô tả"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              multiline
              rows={3}
              fullWidth
              required
            />
            
            <FormControlLabel
              control={
                <Switch
                  checked={formData.team_locked ?? false}
                  onChange={(e) => setFormData({ ...formData, team_locked: e.target.checked })}
                />
              }
              label="Team Locked (chỉ team có thể truy cập)"
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Hủy</Button>
          <Button 
            onClick={handleSubmit} 
            variant="contained"
            disabled={!formData.name.trim() || !formData.description.trim()}
          >
            {editingDataset ? 'Cập nhật' : 'Tạo'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
