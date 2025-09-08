"""
Prometheus Dashboard Configuration for Enhanced Zeta Core
"""
import yaml
import f
import open
import output_dir
import print
import str


PROMETHEUS_CONFIG = {
    "global": {
        "scrape_interval": "15s",
        "evaluation_interval": "15s"
    },
    "scrape_configs": [
        {
            "job_name": "zeta-core-enhanced",
            "static_configs": [
                {
                    "targets": ["localhost:8000"]
                }
            ],
            "metrics_path": "/metrics",
            "scrape_interval": "5s"
        }
    ],
    "rule_files": [
        "zeta_alerts.yml"
    ]
}


GRAFANA_DASHBOARD = {
    "dashboard": {
        "id": None,
        "title": "Enhanced Zeta Core Monitoring",
        "tags": ["zeta", "core", "enhanced"],
        "timezone": "browser",
        "panels": [
            {
                "id": 1,
                "title": "Zero-Trust Decisions",
                "type": "stat",
                "targets": [
                    {
                        "expr": "sum(rate(zeta_zt_decisions_total[5m])) by (allow)",
                        "legendFormat": "{{allow}}"
                    }
                ],
                "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
            },
            {
                "id": 2,
                "title": "Risk Score Distribution",
                "type": "histogram",
                "targets": [
                    {
                        "expr": "histogram_quantile(0.95, rate(zeta_zt_risk_scores_bucket[5m]))",
                        "legendFormat": "95th percentile"
                    },
                    {
                        "expr": "histogram_quantile(0.50, rate(zeta_zt_risk_scores_bucket[5m]))",
                        "legendFormat": "50th percentile"
                    }
                ],
                "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}
            },
            {
                "id": 3,
                "title": "Agent Executions",
                "type": "graph",
                "targets": [
                    {
                        "expr": "sum(rate(zeta_agent_executions_total[5m])) by (agent_type)",
                        "legendFormat": "{{agent_type}}"
                    }
                ],
                "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8}
            },
            {
                "id": 4,
                "title": "Knowledge Graph Queries",
                "type": "graph",
                "targets": [
                    {
                        "expr": "sum(rate(zeta_kg_queries_total[5m])) by (query_type)",
                        "legendFormat": "{{query_type}}"
                    }
                ],
                "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8}
            },
            {
                "id": 5,
                "title": "Active Sessions",
                "type": "stat",
                "targets": [
                    {
                        "expr": "zeta_zt_active_sessions",
                        "legendFormat": "Active Sessions"
                    }
                ],
                "gridPos": {"h": 4, "w": 6, "x": 0, "y": 16}
            },
            {
                "id": 6,
                "title": "Active Agent Teams",
                "type": "stat",
                "targets": [
                    {
                        "expr": "zeta_active_agent_teams",
                        "legendFormat": "Active Teams"
                    }
                ],
                "gridPos": {"h": 4, "w": 6, "x": 6, "y": 16}
            },
            {
                "id": 7,
                "title": "Knowledge Graph Size",
                "type": "stat",
                "targets": [
                    {
                        "expr": "zeta_kg_nodes_total",
                        "legendFormat": "Nodes"
                    },
                    {
                        "expr": "zeta_kg_edges_total",
                        "legendFormat": "Edges"
                    }
                ],
                "gridPos": {"h": 4, "w": 6, "x": 12, "y": 16}
            },
            {
                "id": 8,
                "title": "API Request Rate",
                "type": "graph",
                "targets": [
                    {
                        "expr": "sum(rate(zeta_api_requests_total[5m])) by (endpoint)",
                        "legendFormat": "{{endpoint}}"
                    }
                ],
                "gridPos": {"h": 8, "w": 24, "x": 0, "y": 20}
            }
        ],
        "time": {
            "from": "now-1h",
            "to": "now"
        },
        "refresh": "5s"
    }
}


ALERT_RULES = {
    "groups": [
        {
            "name": "zeta_core_alerts",
            "rules": [
                {
                    "alert": "HighRiskScoreDetected",
                    "expr": "histogram_quantile(0.95, rate(zeta_zt_risk_scores_bucket[5m])) > 0.8",
                    "for": "2m",
                    "labels": {
                        "severity": "warning"
                    },
                    "annotations": {
                        "summary": "High risk scores detected",
                        "description": "95th percentile of risk scores is above 0.8 for 2 minutes"
                    }
                },
                {
                    "alert": "AgentExecutionFailures",
                    "expr": "sum(rate(zeta_agent_executions_total{status=\"failed\"}[5m])) > 0.1",
                    "for": "1m",
                    "labels": {
                        "severity": "critical"
                    },
                    "annotations": {
                        "summary": "High agent execution failure rate",
                        "description": "Agent execution failure rate is above 10% for 1 minute"
                    }
                },
                {
                    "alert": "ZeroTrustDenialSpike",
                    "expr": "sum(rate(zeta_zt_decisions_total{allow=\"false\"}[5m])) > 0.5",
                    "for": "30s",
                    "labels": {
                        "severity": "warning"
                    },
                    "annotations": {
                        "summary": "High Zero-Trust denial rate",
                        "description": "Zero-Trust is denying more than 50% of requests"
                    }
                },
                {
                    "alert": "KnowledgeGraphQueryFailures",
                    "expr": "sum(rate(zeta_kg_queries_total{status=\"failed\"}[5m])) > 0.05",
                    "for": "1m",
                    "labels": {
                        "severity": "warning"
                    },
                    "annotations": {
                        "summary": "Knowledge graph query failures",
                        "description": "Knowledge graph query failure rate is above 5%"
                    }
                }
            ]
        }
    ]
}


def save_prometheus_config(output_dir: str = "."):
    """Save Prometheus configuration files"""
    import os
    
    # Save main Prometheus config
    with open(os.path.join(output_dir, "prometheus.yml"), "w") as f:
        yaml.dump(PROMETHEUS_CONFIG, f, default_flow_style=False)
    
    # Save alert rules
    with open(os.path.join(output_dir, "zeta_alerts.yml"), "w") as f:
        yaml.dump(ALERT_RULES, f, default_flow_style=False)
    
    # Save Grafana dashboard
    with open(os.path.join(output_dir, "grafana_dashboard.json"), "w") as f:
        import json
        json.dump(GRAFANA_DASHBOARD, f, indent=2)
    
    print(f"✅ Prometheus configuration saved to {output_dir}/")
    print("   - prometheus.yml: Main Prometheus configuration")
    print("   - zeta_alerts.yml: Alert rules")
    print("   - grafana_dashboard.json: Grafana dashboard definition")


def create_docker_compose_monitoring():
    """Create docker-compose for monitoring stack"""
    docker_compose = {
        "version": "3.8",
        "services": {
            "prometheus": {
                "image": "prom/prometheus:latest",
                "container_name": "zeta-prometheus",
                "ports": ["9090:9090"],
                "volumes": [
                    "./prometheus.yml:/etc/prometheus/prometheus.yml",
                    "./zeta_alerts.yml:/etc/prometheus/zeta_alerts.yml"
                ],
                "command": [
                    "--config.file=/etc/prometheus/prometheus.yml",
                    "--storage.tsdb.path=/prometheus",
                    "--web.console.libraries=/etc/prometheus/console_libraries",
                    "--web.console.templates=/etc/prometheus/consoles",
                    "--storage.tsdb.retention.time=200h",
                    "--web.enable-lifecycle"
                ]
            },
            "grafana": {
                "image": "grafana/grafana:latest",
                "container_name": "zeta-grafana",
                "ports": ["3000:3000"],
                "environment": [
                    "GF_SECURITY_ADMIN_PASSWORD=admin"
                ],
                "volumes": [
                    "grafana-storage:/var/lib/grafana"
                ]
            }
        },
        "volumes": {
            "grafana-storage": {}
        }
    }
    
    with open("docker-compose.monitoring.yml", "w") as f:
        yaml.dump(docker_compose, f, default_flow_style=False)
    
    print("✅ Created docker-compose.monitoring.yml")


if __name__ == "__main__":
    # Save all configuration files
    save_prometheus_config()
    create_docker_compose_monitoring()
    
    print("\n🚀 To start monitoring:")
    print("1. docker-compose -f docker-compose.monitoring.yml up -d")
    print("2. Access Grafana at http://localhost:3000 (admin/admin)")
    print("3. Add Prometheus data source: http://prometheus:9090")
    print("4. Import the dashboard from grafana_dashboard.json")
