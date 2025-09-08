# Terraform configuration for Zeta AI Agent
# Generated automatically by DevOps Orchestrator

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }

  backend "local" {
    path = "terraform.tfstate"
  }
}

# Provider configuration
provider "kubernetes" {
  config_path = var.kubeconfig_path
  config_context = var.kube_context
}

provider "helm" {
  kubernetes {
    config_path = var.kubeconfig_path
    config_context = var.kube_context
  }
}

# Local values
locals {
  environment = var.environment
  app_name = "zeta-ai-agent"
  namespace = "zeta-ai-${local.environment}"
  
  common_labels = {
    app = local.app_name
    environment = local.environment
    managed_by = "terraform"
    created_by = "devops-orchestrator"
  }
  
  common_tags = merge(var.tags, local.common_labels)
}

# Namespace
resource "kubernetes_namespace" "zeta_ai" {
  metadata {
    name = local.namespace
    labels = local.common_labels
    
    annotations = {
      "description" = "Namespace for Zeta AI Agent - ${local.environment}"
      "created-by" = "terraform"
    }
  }
}

# ConfigMap for application configuration
resource "kubernetes_config_map" "zeta_config" {
  metadata {
    name = "zeta-agent-config"
    namespace = kubernetes_namespace.zeta_ai.metadata[0].name
    labels = local.common_labels
  }

  data = {
    NODE_ENV = local.environment
    OLLAMA_HOST = var.ollama_host
    OLLAMA_PORT = var.ollama_port
    CACHE_TTL = var.cache_ttl
    LOG_LEVEL = var.log_level
    MAX_CONTEXT_SIZE = var.max_context_size
    VECTOR_DB_PATH = "/data/vector"
    METRICS_PORT = "9090"
  }
}

# Secret for sensitive configuration
resource "kubernetes_secret" "zeta_secrets" {
  metadata {
    name = "zeta-secrets"
    namespace = kubernetes_namespace.zeta_ai.metadata[0].name
    labels = local.common_labels
  }

  data = {
    ollama-api-key = var.ollama_api_key
    database-password = random_password.db_password.result
    jwt-secret = random_password.jwt_secret.result
  }

  type = "Opaque"
}

# Random passwords
resource "random_password" "db_password" {
  length = 32
  special = true
}

resource "random_password" "jwt_secret" {
  length = 64
  special = false
}

# Persistent Volume Claim for vector storage
resource "kubernetes_persistent_volume_claim" "vector_storage" {
  metadata {
    name = "zeta-vector-storage"
    namespace = kubernetes_namespace.zeta_ai.metadata[0].name
    labels = local.common_labels
  }

  spec {
    access_modes = ["ReadWriteOnce"]
    resources {
      requests = {
        storage = var.storage_size
      }
    }
    storage_class_name = var.storage_class
  }
}

# Service Account
resource "kubernetes_service_account" "zeta_agent" {
  metadata {
    name = "zeta-agent"
    namespace = kubernetes_namespace.zeta_ai.metadata[0].name
    labels = local.common_labels
  }
}

# Role for service account
resource "kubernetes_role" "zeta_agent" {
  metadata {
    name = "zeta-agent"
    namespace = kubernetes_namespace.zeta_ai.metadata[0].name
    labels = local.common_labels
  }

  rule {
    api_groups = [""]
    resources = ["configmaps", "secrets"]
    verbs = ["get", "list", "watch"]
  }
  
  rule {
    api_groups = [""]
    resources = ["pods"]
    verbs = ["get", "list", "watch"]
  }
}

# Role binding
resource "kubernetes_role_binding" "zeta_agent" {
  metadata {
    name = "zeta-agent"
    namespace = kubernetes_namespace.zeta_ai.metadata[0].name
    labels = local.common_labels
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind = "Role"
    name = kubernetes_role.zeta_agent.metadata[0].name
  }

  subject {
    kind = "ServiceAccount"
    name = kubernetes_service_account.zeta_agent.metadata[0].name
    namespace = kubernetes_namespace.zeta_ai.metadata[0].name
  }
}

# Deployment
resource "kubernetes_deployment" "zeta_agent" {
  metadata {
    name = "zeta-agent"
    namespace = kubernetes_namespace.zeta_ai.metadata[0].name
    labels = local.common_labels
    
    annotations = {
      "deployment.kubernetes.io/revision" = "1"
      "description" = "Zeta AI Agent deployment"
    }
  }

  spec {
    replicas = var.replicas
    
    selector {
      match_labels = {
        app = local.app_name
        environment = local.environment
      }
    }

    template {
      metadata {
        labels = merge(local.common_labels, {
          version = var.app_version
        })
        
        annotations = {
          "prometheus.io/scrape" = "true"
          "prometheus.io/port" = "9090"
          "prometheus.io/path" = "/metrics"
        }
      }

      spec {
        service_account_name = kubernetes_service_account.zeta_agent.metadata[0].name
        
        security_context {
          fs_group = 1001
          run_as_non_root = true
          run_as_user = 1001
        }

        container {
          name = "zeta-agent"
          image = "${var.image_registry}/${var.image_name}:${var.image_tag}"
          image_pull_policy = "Always"

          port {
            container_port = 3000
            name = "http"
            protocol = "TCP"
          }
          
          port {
            container_port = 9090
            name = "metrics"
            protocol = "TCP"
          }

          env_from {
            config_map_ref {
              name = kubernetes_config_map.zeta_config.metadata[0].name
            }
          }

          env {
            name = "OLLAMA_API_KEY"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.zeta_secrets.metadata[0].name
                key = "ollama-api-key"
              }
            }
          }

          resources {
            requests = {
              cpu = var.cpu_request
              memory = var.memory_request
            }
            limits = {
              cpu = var.cpu_limit
              memory = var.memory_limit
            }
          }

          liveness_probe {
            http_get {
              path = "/health"
              port = 3000
            }
            initial_delay_seconds = 30
            period_seconds = 10
            timeout_seconds = 5
            failure_threshold = 3
          }

          readiness_probe {
            http_get {
              path = "/ready"
              port = 3000
            }
            initial_delay_seconds = 5
            period_seconds = 5
            timeout_seconds = 3
            failure_threshold = 3
          }

          volume_mount {
            name = "vector-storage"
            mount_path = "/data/vector"
          }
          
          volume_mount {
            name = "temp-storage"
            mount_path = "/tmp"
          }
        }

        volume {
          name = "vector-storage"
          persistent_volume_claim {
            claim_name = kubernetes_persistent_volume_claim.vector_storage.metadata[0].name
          }
        }
        
        volume {
          name = "temp-storage"
          empty_dir {}
        }

        node_selector = var.node_selector
        
        dynamic "toleration" {
          for_each = var.tolerations
          content {
            key = toleration.value.key
            operator = toleration.value.operator
            value = toleration.value.value
            effect = toleration.value.effect
          }
        }

        affinity {
          pod_anti_affinity {
            preferred_during_scheduling_ignored_during_execution {
              weight = 100
              pod_affinity_term {
                label_selector {
                  match_expressions {
                    key = "app"
                    operator = "In"
                    values = [local.app_name]
                  }
                }
                topology_key = "kubernetes.io/hostname"
              }
            }
          }
        }
      }
    }

    strategy {
      type = "RollingUpdate"
      rolling_update {
        max_surge = "25%"
        max_unavailable = "25%"
      }
    }
  }
}

# Service
resource "kubernetes_service" "zeta_agent" {
  metadata {
    name = "zeta-agent"
    namespace = kubernetes_namespace.zeta_ai.metadata[0].name
    labels = local.common_labels
  }

  spec {
    selector = {
      app = local.app_name
      environment = local.environment
    }

    port {
      name = "http"
      port = 80
      target_port = 3000
      protocol = "TCP"
    }
    
    port {
      name = "metrics"
      port = 9090
      target_port = 9090
      protocol = "TCP"
    }

    type = var.service_type
  }
}

# Horizontal Pod Autoscaler
resource "kubernetes_horizontal_pod_autoscaler_v2" "zeta_agent" {
  count = var.enable_autoscaling ? 1 : 0
  
  metadata {
    name = "zeta-agent-hpa"
    namespace = kubernetes_namespace.zeta_ai.metadata[0].name
    labels = local.common_labels
  }

  spec {
    scale_target_ref {
      api_version = "apps/v1"
      kind = "Deployment"
      name = kubernetes_deployment.zeta_agent.metadata[0].name
    }

    min_replicas = var.min_replicas
    max_replicas = var.max_replicas

    metric {
      type = "Resource"
      resource {
        name = "cpu"
        target {
          type = "Utilization"
          average_utilization = var.target_cpu_utilization
        }
      }
    }

    metric {
      type = "Resource"
      resource {
        name = "memory"
        target {
          type = "Utilization"
          average_utilization = var.target_memory_utilization
        }
      }
    }
  }
}

# Ingress (if enabled)
resource "kubernetes_ingress_v1" "zeta_agent" {
  count = var.enable_ingress ? 1 : 0
  
  metadata {
    name = "zeta-agent-ingress"
    namespace = kubernetes_namespace.zeta_ai.metadata[0].name
    labels = local.common_labels
    
    annotations = {
      "kubernetes.io/ingress.class" = "nginx"
      "cert-manager.io/cluster-issuer" = "letsencrypt-prod"
      "nginx.ingress.kubernetes.io/ssl-redirect" = "true"
      "nginx.ingress.kubernetes.io/rate-limit" = "100"
    }
  }

  spec {
    tls {
      hosts = [var.domain]
      secret_name = "zeta-agent-tls"
    }

    rule {
      host = var.domain
      http {
        path {
          path = "/"
          path_type = "Prefix"
          backend {
            service {
              name = kubernetes_service.zeta_agent.metadata[0].name
              port {
                number = 80
              }
            }
          }
        }
      }
    }
  }
}
