// System Monitor Plugin - Safe metadata-only
// Entry point cho plugin system performance monitor

export default {
  // Plugin chỉ export config/metadata, không có executable code
  pluginType: 'system-widget',
  
  // UI configuration cho system monitor widget
  widget: {
    title: 'System Monitor',
    position: 'header',
    size: 'compact'
  },
  
  // System metrics configuration (read-only)
  metrics: {
    cpu: {
      label: 'CPU',
      unit: '%',
      refreshInterval: 5000
    },
    memory: {
      label: 'Memory',
      unit: 'MB',
      refreshInterval: 5000
    },
    disk: {
      label: 'Disk',
      unit: 'GB',
      refreshInterval: 30000
    }
  },
  
  // UI templates (safe HTML/CSS only)
  templates: {
    compactView: `
      <div class="system-monitor-compact">
        <span class="metric">CPU: {{cpu}}%</span>
        <span class="metric">RAM: {{memory}}MB</span>
        <span class="status-indicator {{status}}"></span>
      </div>
    `,
    detailView: `
      <div class="system-monitor-detail">
        <div class="metric-row">
          <span class="label">CPU Usage:</span>
          <span class="value">{{cpu}}%</span>
          <div class="meter"><div class="fill" style="width: {{cpu}}%"></div></div>
        </div>
        <div class="metric-row">
          <span class="label">Memory:</span>
          <span class="value">{{memory}}MB / {{memoryTotal}}MB</span>
          <div class="meter"><div class="fill" style="width: {{memoryPercent}}%"></div></div>
        </div>
        <div class="metric-row">
          <span class="label">Disk:</span>
          <span class="value">{{diskFree}}GB free</span>
        </div>
      </div>
    `
  },
  
  // Safe CSS styles
  styles: `
    .system-monitor-compact {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 4px 8px;
      font-size: 12px;
      color: #666;
    }
    .system-monitor-compact .metric {
      font-family: monospace;
    }
    .status-indicator {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #4caf50;
    }
    .status-indicator.warning { background: #ff9800; }
    .status-indicator.error { background: #f44336; }
    .system-monitor-detail {
      padding: 16px;
      background: #f5f5f5;
      border-radius: 8px;
    }
    .metric-row {
      display: grid;
      grid-template-columns: 80px 80px 1fr;
      align-items: center;
      gap: 8px;
      margin-bottom: 8px;
    }
    .meter {
      height: 6px;
      background: #e0e0e0;
      border-radius: 3px;
      overflow: hidden;
    }
    .meter .fill {
      height: 100%;
      background: linear-gradient(90deg, #4caf50, #ff9800, #f44336);
      transition: width 0.3s ease;
    }
  `
};