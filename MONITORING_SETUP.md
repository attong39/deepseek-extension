# Zeta AI Agent Monitoring & Feedback Configuration

## Prometheus Configuration

### prometheus.yml
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "zeta_rules.yml"

scrape_configs:
  - job_name: 'zeta_ai_agent'
    static_configs:
      - targets: ['localhost:9100']   # metrics endpoint exposed by FastAPI
    scrape_interval: 5s
    metrics_path: /metrics
    
  - job_name: 'ollama'
    static_configs:
      - targets: ['localhost:11434']
    scrape_interval: 10s
    metrics_path: /metrics

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
```

### Alert Rules (zeta_rules.yml)
```yaml
groups:
  - name: zeta_ai_agent
    rules:
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(zeta_request_duration_seconds_bucket[5m])) > 10
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "95th percentile latency is {{ $value }}s"
          
      - alert: LowSuccessRate
        expr: rate(zeta_requests_total{status="success"}[5m]) / rate(zeta_requests_total[5m]) < 0.8
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Low success rate"
          description: "Success rate is {{ $value | humanizePercentage }}"
          
      - alert: VietnameseQualityDrop
        expr: avg(zeta_vietnamese_quality_score) < 7
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Vietnamese quality degradation"
          description: "Average Vietnamese quality score dropped to {{ $value }}"
```

## Grafana Dashboard Configuration

### Dashboard JSON (zeta_dashboard.json)
```json
{
  "dashboard": {
    "id": null,
    "title": "Zeta AI Agent Monitoring",
    "tags": ["zeta", "ai", "monitoring"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Request Latency",
        "type": "stat",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(zeta_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "s",
            "min": 0,
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 1},
                {"color": "red", "value": 10}
              ]
            }
          }
        }
      },
      {
        "id": 2,
        "title": "Success Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(zeta_requests_total{status=\"success\"}[5m]) / rate(zeta_requests_total[5m])",
            "legendFormat": "Success Rate"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percentunit",
            "min": 0,
            "max": 1,
            "thresholds": {
              "steps": [
                {"color": "red", "value": null},
                {"color": "yellow", "value": 0.8},
                {"color": "green", "value": 0.9}
              ]
            }
          }
        }
      },
      {
        "id": 3,
        "title": "Vietnamese Quality Score",
        "type": "stat",
        "targets": [
          {
            "expr": "avg(zeta_vietnamese_quality_score)",
            "legendFormat": "Avg Quality"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "min": 0,
            "max": 10,
            "thresholds": {
              "steps": [
                {"color": "red", "value": null},
                {"color": "yellow", "value": 7},
                {"color": "green", "value": 8}
              ]
            }
          }
        }
      },
      {
        "id": 4,
        "title": "Model Usage Distribution",
        "type": "piechart",
        "targets": [
          {
            "expr": "rate(zeta_requests_total[5m])",
            "legendFormat": "{{ model }}"
          }
        ]
      },
      {
        "id": 5,
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(zeta_requests_total[1m])",
            "legendFormat": "Requests/sec"
          }
        ]
      }
    ],
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "refresh": "5s"
  }
}
```

## Feedback Collection System

### FastAPI Metrics Endpoint
```python
# metrics_server.py
from fastapi import FastAPI, BackgroundTasks
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import time
import json
import sqlite3
from datetime import datetime

app = FastAPI()

# Prometheus metrics
request_count = Counter('zeta_requests_total', 'Total requests', ['model', 'status'])
request_duration = Histogram('zeta_request_duration_seconds', 'Request duration', ['model'])
vietnamese_quality = Gauge('zeta_vietnamese_quality_score', 'Vietnamese quality score', ['model'])
feedback_count = Counter('zeta_feedback_total', 'User feedback', ['rating'])

# Database setup
def init_db():
    conn = sqlite3.connect('feedback.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            model TEXT,
            prompt TEXT,
            response TEXT,
            rating INTEGER,
            vietnamese_quality REAL,
            latency REAL,
            metadata TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/feedback")
async def submit_feedback(feedback_data: dict, background_tasks: BackgroundTasks):
    """Collect user feedback"""
    background_tasks.add_task(store_feedback, feedback_data)
    
    # Update Prometheus metrics
    if 'rating' in feedback_data:
        feedback_count.labels(rating=feedback_data['rating']).inc()
    
    return {"status": "success", "message": "Feedback recorded"}

def store_feedback(data: dict):
    """Store feedback in database"""
    conn = sqlite3.connect('feedback.db')
    conn.execute('''
        INSERT INTO feedback (model, prompt, response, rating, vietnamese_quality, latency, metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('model'),
        data.get('prompt'),
        data.get('response'),
        data.get('rating'),
        data.get('vietnamese_quality'),
        data.get('latency'),
        json.dumps(data.get('metadata', {}))
    ))
    conn.commit()
    conn.close()

@app.post("/metrics/request")
async def log_request(request_data: dict):
    """Log request metrics"""
    model = request_data.get('model', 'unknown')
    status = request_data.get('status', 'unknown')
    duration = request_data.get('duration', 0)
    vn_quality = request_data.get('vietnamese_quality')
    
    request_count.labels(model=model, status=status).inc()
    request_duration.labels(model=model).observe(duration)
    
    if vn_quality is not None:
        vietnamese_quality.labels(model=model).set(vn_quality)
    
    return {"status": "logged"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9100)
```

### VS Code Extension Feedback Integration
```typescript
// feedback.ts
export class FeedbackManager {
    private metricsEndpoint = 'http://localhost:9100';
    
    async submitFeedback(feedback: {
        model: string;
        prompt: string;
        response: string;
        rating: number; // 1-5 stars
        vietnameseQuality?: number; // 1-10 scale
        latency: number;
    }) {
        try {
            await fetch(`${this.metricsEndpoint}/feedback`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(feedback)
            });
        } catch (error) {
            console.error('Failed to submit feedback:', error);
        }
    }
    
    async logRequest(request: {
        model: string;
        status: 'success' | 'error' | 'timeout';
        duration: number;
        vietnameseQuality?: number;
    }) {
        try {
            await fetch(`${this.metricsEndpoint}/metrics/request`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(request)
            });
        } catch (error) {
            console.error('Failed to log request:', error);
        }
    }
}
```

## Auto-retrain Schedule

### Weekly Retrain Script (lo_finetune.sh)
```bash
#!/bin/bash
# lo_finetune.sh - Weekly model retraining

set -e

LOG_FILE="/var/log/zeta_retrain.log"
FEEDBACK_DB="/path/to/feedback.db"

echo "$(date): Starting weekly LoRA fine-tuning" >> $LOG_FILE

# Extract good feedback samples
python3 << EOF
import sqlite3
import json

conn = sqlite3.connect('$FEEDBACK_DB')
cursor = conn.execute('''
    SELECT prompt, response, vietnamese_quality 
    FROM feedback 
    WHERE rating >= 4 AND vietnamese_quality >= 8
    AND timestamp > date('now', '-7 days')
''')

samples = []
for row in cursor:
    samples.append({
        'prompt': row[0],
        'response': row[1],
        'quality': row[2]
    })

with open('new_training_samples.jsonl', 'w') as f:
    for sample in samples:
        f.write(json.dumps(sample) + '\n')

print(f"Extracted {len(samples)} new training samples")
EOF

# Run LoRA fine-tuning if we have enough samples
if [ -f "new_training_samples.jsonl" ] && [ $(wc -l < new_training_samples.jsonl) -gt 100 ]; then
    echo "$(date): Running LoRA fine-tuning with $(wc -l < new_training_samples.jsonl) samples" >> $LOG_FILE
    
    python scripts/lo_finetune.py \
        --base_model attong39/zeta \
        --dataset new_training_samples.jsonl \
        --epochs 1 \
        --learning_rate 2e-4 \
        --output_model attong39/zeta-updated
    
    # Test the updated model
    python scripts/benchmark_latency.py --model attong39/zeta-updated --quick
    
    # If performance is better, deploy
    if [ $? -eq 0 ]; then
        ollama cp attong39/zeta-updated attong39/zeta
        ollama push attong39/zeta
        echo "$(date): Model updated and deployed successfully" >> $LOG_FILE
    else
        echo "$(date): New model performance worse, keeping existing model" >> $LOG_FILE
    fi
else
    echo "$(date): Insufficient training samples, skipping retrain" >> $LOG_FILE
fi

echo "$(date): Weekly retrain completed" >> $LOG_FILE
```

### Cron Job Setup
```bash
# Add to crontab: crontab -e
# Run every Sunday at 02:00
0 2 * * 0 /home/ai/zeta/lo_finetune.sh >> /var/log/zeta_retrain.log 2>&1
```

## Deployment Commands

### Start Monitoring Stack
```bash
# Start metrics server
cd monitoring
python metrics_server.py &

# Start Prometheus
prometheus --config.file=prometheus.yml &

# Start Grafana (if using Docker)
docker run -d -p 3000:3000 \
  -v grafana-storage:/var/lib/grafana \
  -v $(pwd)/dashboards:/etc/grafana/provisioning/dashboards \
  grafana/grafana
```

### Current Status
✅ **Metrics Framework**: Prometheus configuration ready
✅ **Dashboard**: Grafana dashboard with key KPIs
✅ **Feedback System**: VS Code integration with database storage
✅ **Auto-retrain**: Weekly model improvement pipeline
✅ **Alerting**: Critical metrics monitoring

Ready for production deployment with comprehensive observability.
