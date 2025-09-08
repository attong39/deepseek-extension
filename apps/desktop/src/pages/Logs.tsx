/**
 * Logs Page
 * Real-time log viewing với filtering và export
 */
import {
    Clear as ClearIcon,
    Download as DownloadIcon,
    Refresh as RefreshIcon,
} from '@mui/icons-material';
import {
    Alert,
    Box,
    Button,
    Card,
    CardContent,
    Chip,
    FormControl,
    Grid,
    IconButton,
    InputLabel,
    MenuItem,
    Paper,
    Select,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    TextField,
    Tooltip,
    Typography,
} from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { useSnackbar } from 'notistack';
import React, { useState } from 'react';

import { apiService, queryKeys } from '../services/apiService';
import Actions from "Actions";
import All from "All";
import Auto from "Auto";
import Blob from "Blob";
import CSV from "CSV";
import Clear from "Clear";
import Convert from "Convert";
import DEBUG from "DEBUG";
import Debug from "Debug";
import Download from "Download";
import ERROR from "ERROR";
import Error from "Error";
import Escape from "Escape";
import Export from "Export";
import Exported from "Exported";
import FC from "FC";
import Fetch from "Fetch";
import Filter from "Filter";
import Filters from "Filters";
import Header from "Header";
import INFO from "INFO";
import Info from "Info";
import Level from "Level";
import Levels from "Levels";
import Limit from "Limit";
import Loading from "Loading";
import Logs from "./Logs";
import Max from "Max";
import Message from "Message";
import Metadata from "Metadata";
import No from "No";
import Page from "Page";
import Real from "Real";
import Refresh from "Refresh";
import Reset from "Reset";
import Search from "Search";
import Set from "Set";
import Source from "Source";
import Sources from "Sources";
import System from "System";
import T from "T";
import Timestamp from "Timestamp";
import URL from "URL";
import WARNING from "WARNING";
import Warning from "Warning";

const Logs: React.FC = () => {
  const { enqueueSnackbar } = useSnackbar();
  
  const [filters, setFilters] = useState({
    level: '',
    source: '',
    limit: 100,
    skip: 0,
  });
  const [searchText, setSearchText] = useState('');

  // Fetch logs with current filters
  const { data: logs = [], isLoading, refetch } = useQuery({
    queryKey: queryKeys.logs(filters.level || undefined, filters.source || undefined, filters.limit, filters.skip),
    queryFn: () => apiService.getLogs(
      filters.level || undefined,
      filters.source || undefined,
      filters.limit,
      filters.skip
    ),
    refetchInterval: 5000, // Auto-refresh every 5s
  });

  // Filter logs by search text on frontend
  const filteredLogs = logs.filter(log => 
    searchText === '' || 
    log.message.toLowerCase().includes(searchText.toLowerCase()) ||
    log.source.toLowerCase().includes(searchText.toLowerCase())
  );

  const handleFilterChange = (field: string, value: any) => {
    setFilters(prev => ({
      ...prev,
      [field]: value,
      skip: 0, // Reset pagination when filtering
    }));
  };

  const handleClearFilters = () => {
    setFilters({
      level: '',
      source: '',
      limit: 100,
      skip: 0,
    });
    setSearchText('');
  };

  const handleExportLogs = async () => {
    try {
      // Fetch all logs for export (no limit)
      const allLogs = await apiService.getLogs(
        filters.level || undefined,
        filters.source || undefined,
        1000, // Max export limit
        0
      );

      // Convert to CSV
      const csvHeaders = ['Timestamp', 'Level', 'Source', 'Message', 'Metadata'];
      const csvRows = allLogs.map(log => [
        new Date(log.timestamp).toISOString(),
        log.level,
        log.source,
        `"${log.message.replace(/"/g, '""')}"`, // Escape quotes
        `"${JSON.stringify(log.metadata).replace(/"/g, '""')}"`,
      ]);

      const csvContent = [
        csvHeaders.join(','),
        ...csvRows.map(row => row.join(','))
      ].join('\n');

      // Download CSV file
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      const url = URL.createObjectURL(blob);
      link.setAttribute('href', url);
      link.setAttribute('download', `zeta_logs_${new Date().toISOString().split('T')[0]}.csv`);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      enqueueSnackbar(`Exported ${allLogs.length} log entries`, { variant: 'success' });
    } catch (error) {
      enqueueSnackbar(`Export failed: ${(error as Error).message}`, { variant: 'error' });
    }
  };

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'ERROR': return 'error';
      case 'WARNING': return 'warning';
      case 'INFO': return 'info';
      case 'DEBUG': return 'default';
      default: return 'default';
    }
  };

  const uniqueSources = [...new Set(logs.map(log => log.source))];

  return (
    <Box>
      {/* Header */}
      <Typography variant="h4" gutterBottom>
        System Logs
      </Typography>

      {/* Filters */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Filters & Search
          </Typography>
          
          <Grid container spacing={2} alignItems="center">
            {/* Search */}
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Search logs"
                value={searchText}
                onChange={(e) => setSearchText(e.target.value)}
                placeholder="Search messages, sources..."
                size="small"
              />
            </Grid>

            {/* Level Filter */}
            <Grid item xs={12} md={2}>
              <FormControl fullWidth size="small">
                <InputLabel>Level</InputLabel>
                <Select
                  value={filters.level}
                  label="Level"
                  onChange={(e) => handleFilterChange('level', e.target.value)}
                >
                  <MenuItem value="">All Levels</MenuItem>
                  <MenuItem value="DEBUG">Debug</MenuItem>
                  <MenuItem value="INFO">Info</MenuItem>
                  <MenuItem value="WARNING">Warning</MenuItem>
                  <MenuItem value="ERROR">Error</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            {/* Source Filter */}
            <Grid item xs={12} md={2}>
              <FormControl fullWidth size="small">
                <InputLabel>Source</InputLabel>
                <Select
                  value={filters.source}
                  label="Source"
                  onChange={(e) => handleFilterChange('source', e.target.value)}
                >
                  <MenuItem value="">All Sources</MenuItem>
                  {uniqueSources.map(source => (
                    <MenuItem key={source} value={source}>{source}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            {/* Limit */}
            <Grid item xs={12} md={2}>
              <FormControl fullWidth size="small">
                <InputLabel>Limit</InputLabel>
                <Select
                  value={filters.limit}
                  label="Limit"
                  onChange={(e) => handleFilterChange('limit', e.target.value)}
                >
                  <MenuItem value={50}>50 logs</MenuItem>
                  <MenuItem value={100}>100 logs</MenuItem>
                  <MenuItem value={200}>200 logs</MenuItem>
                  <MenuItem value={500}>500 logs</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            {/* Actions */}
            <Grid item xs={12} md={2}>
              <Box display="flex" gap={1}>
                <Tooltip title="Refresh logs">
                  <IconButton onClick={() => refetch()} disabled={isLoading}>
                    <RefreshIcon />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Clear filters">
                  <IconButton onClick={handleClearFilters}>
                    <ClearIcon />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Export to CSV">
                  <IconButton onClick={handleExportLogs}>
                    <DownloadIcon />
                  </IconButton>
                </Tooltip>
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Logs Table */}
      <Card>
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
            <Typography variant="h6">
              Logs ({filteredLogs.length} entries)
            </Typography>
            <Button
              startIcon={<DownloadIcon />}
              onClick={handleExportLogs}
              variant="outlined"
              size="small"
            >
              Export CSV
            </Button>
          </Box>

          {isLoading && <Typography>Loading logs...</Typography>}
          
          {!isLoading && filteredLogs.length === 0 && (
            <Alert severity="info">
              No logs found matching current filters.
            </Alert>
          )}
          
          {!isLoading && filteredLogs.length > 0 && (
            <TableContainer component={Paper} variant="outlined" sx={{ maxHeight: 600 }}>
              <Table stickyHeader size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Timestamp</TableCell>
                    <TableCell>Level</TableCell>
                    <TableCell>Source</TableCell>
                    <TableCell>Message</TableCell>
                    <TableCell>Metadata</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {filteredLogs.map((log) => (
                    <TableRow key={log.id} hover>
                      <TableCell>
                        <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                          {new Date(log.timestamp).toLocaleString()}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={log.level}
                          size="small"
                          color={getLevelColor(log.level)}
                          variant="outlined"
                        />
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" color="text.secondary">
                          {log.source}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" sx={{ maxWidth: 400, wordBreak: 'break-word' }}>
                          {log.message}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        {Object.keys(log.metadata).length > 0 ? (
                          <Tooltip title={JSON.stringify(log.metadata, null, 2)}>
                            <Chip 
                              label={`${Object.keys(log.metadata).length} items`}
                              size="small"
                              variant="outlined"
                            />
                          </Tooltip>
                        ) : (
                          <Typography variant="body2" color="text.secondary">-</Typography>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}

          {/* Auto-refresh indicator */}
          <Box mt={2} display="flex" justifyContent="center">
            <Alert severity="info" sx={{ width: 'fit-content' }}>
              🔄 Auto-refreshing every 5 seconds
            </Alert>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Logs;
