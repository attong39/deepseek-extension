# Variables for Zeta AI Agent Terraform configuration

variable "environment" {
  description = "Environment name (development, staging, production)"
  type        = string
  default     = "development"
  
  validation {
    condition = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be one of: development, staging, production."
  }
}

variable "kubeconfig_path" {
  description = "Path to kubeconfig file"
  type        = string
  default     = "~/.kube/config"
}

variable "kube_context" {
  description = "Kubernetes context to use"
  type        = string
  default     = "default"
}

variable "image_registry" {
  description = "Container image registry"
  type        = string
  default     = "ghcr.io"
}

variable "image_name" {
  description = "Container image name"
  type        = string
  default     = "zeta/zeta-ai-agent"
}

variable "image_tag" {
  description = "Container image tag"
  type        = string
  default     = "latest"
}

variable "app_version" {
  description = "Application version"
  type        = string
  default     = "1.0.0"
}

variable "replicas" {
  description = "Number of pod replicas"
  type        = number
  default     = 1
  
  validation {
    condition = var.replicas >= 1 && var.replicas <= 50
    error_message = "Replicas must be between 1 and 50."
  }
}

variable "cpu_request" {
  description = "CPU request for containers"
  type        = string
  default     = "100m"
}

variable "memory_request" {
  description = "Memory request for containers"
  type        = string
  default     = "256Mi"
}

variable "cpu_limit" {
  description = "CPU limit for containers"
  type        = string
  default     = "500m"
}

variable "memory_limit" {
  description = "Memory limit for containers"
  type        = string
  default     = "1Gi"
}

variable "storage_size" {
  description = "Storage size for vector database"
  type        = string
  default     = "5Gi"
}

variable "storage_class" {
  description = "Storage class for persistent volumes"
  type        = string
  default     = "standard"
}

variable "service_type" {
  description = "Kubernetes service type"
  type        = string
  default     = "ClusterIP"
  
  validation {
    condition = contains(["ClusterIP", "NodePort", "LoadBalancer"], var.service_type)
    error_message = "Service type must be ClusterIP, NodePort, or LoadBalancer."
  }
}

variable "enable_autoscaling" {
  description = "Enable horizontal pod autoscaling"
  type        = bool
  default     = false
}

variable "min_replicas" {
  description = "Minimum number of replicas for autoscaling"
  type        = number
  default     = 1
}

variable "max_replicas" {
  description = "Maximum number of replicas for autoscaling"
  type        = number
  default     = 10
}

variable "target_cpu_utilization" {
  description = "Target CPU utilization percentage for autoscaling"
  type        = number
  default     = 70
}

variable "target_memory_utilization" {
  description = "Target memory utilization percentage for autoscaling"
  type        = number
  default     = 80
}

variable "enable_ingress" {
  description = "Enable ingress for external access"
  type        = bool
  default     = false
}

variable "domain" {
  description = "Domain name for ingress"
  type        = string
  default     = "zeta-ai.example.com"
}

variable "ollama_host" {
  description = "Ollama service host"
  type        = string
  default     = "ollama-service"
}

variable "ollama_port" {
  description = "Ollama service port"
  type        = string
  default     = "11434"
}

variable "ollama_api_key" {
  description = "Ollama API key"
  type        = string
  sensitive   = true
  default     = ""
}

variable "cache_ttl" {
  description = "Cache TTL in seconds"
  type        = string
  default     = "3600"
}

variable "log_level" {
  description = "Application log level"
  type        = string
  default     = "info"
  
  validation {
    condition = contains(["error", "warn", "info", "debug"], var.log_level)
    error_message = "Log level must be one of: error, warn, info, debug."
  }
}

variable "max_context_size" {
  description = "Maximum context size for AI operations"
  type        = string
  default     = "4096"
}

variable "node_selector" {
  description = "Node selector for pod placement"
  type        = map(string)
  default     = {}
}

variable "tolerations" {
  description = "Tolerations for pod placement"
  type = list(object({
    key      = string
    operator = string
    value    = string
    effect   = string
  }))
  default = []
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
