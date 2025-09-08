// Training Monitor Plugin - Safe metadata-only
// Entry point cho plugin training progress monitor

export default {
  // Plugin chỉ export config/metadata, không có executable code
  pluginType: 'ui-widget',
  
  // UI configuration cho training progress widget
  widget: {
    title: 'Training Progress',
    position: 'sidebar',
    size: 'small'
  },
  
  // WebSocket event handlers configuration
  websocketEvents: {
    'training-progress': {
      handler: 'displayProgress',
      ui: 'progress-bar'
    },
    'training-complete': {
      handler: 'showCompletion',
      ui: 'notification'
    }
  },
  
  // UI templates (safe HTML/CSS only)
  templates: {
    progressBar: `
      <div class="training-progress">
        <div class="progress-label">{{title}}</div>
        <div class="progress-bar">
          <div class="progress-fill" style="width: {{progress}}%"></div>
        </div>
        <div class="progress-text">{{progress}}% - {{status}}</div>
      </div>
    `,
    notification: `
      <div class="training-notification">
        <span class="icon">✅</span>
        <span class="message">{{message}}</span>
      </div>
    `
  },
  
  // Safe CSS styles
  styles: `
    .training-progress {
      padding: 12px;
      border: 1px solid #e0e0e0;
      border-radius: 8px;
      background: #f9f9f9;
    }
    .progress-bar {
      height: 8px;
      background: #e0e0e0;
      border-radius: 4px;
      overflow: hidden;
      margin: 8px 0;
    }
    .progress-fill {
      height: 100%;
      background: linear-gradient(90deg, #4caf50, #8bc34a);
      transition: width 0.3s ease;
    }
    .progress-label {
      font-weight: 600;
      font-size: 14px;
      color: #333;
    }
    .progress-text {
      font-size: 12px;
      color: #666;
      text-align: center;
    }
    .training-notification {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 12px;
      background: #e8f5e8;
      border: 1px solid #4caf50;
      border-radius: 6px;
      color: #2e7d32;
    }
  `
};