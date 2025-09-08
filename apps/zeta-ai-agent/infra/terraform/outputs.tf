# Outputs for Zeta AI Agent Terraform configuration

output "namespace" {
  description = "Kubernetes namespace"
  value       = kubernetes_namespace.zeta_ai.metadata[0].name
}

output "deployment_name" {
  description = "Kubernetes deployment name"
  value       = kubernetes_deployment.zeta_agent.metadata[0].name
}

output "service_name" {
  description = "Kubernetes service name"
  value       = kubernetes_service.zeta_agent.metadata[0].name
}

output "service_ip" {
  description = "Service cluster IP"
  value       = kubernetes_service.zeta_agent.spec[0].cluster_ip
}

output "configmap_name" {
  description = "ConfigMap name"
  value       = kubernetes_config_map.zeta_config.metadata[0].name
}

output "secret_name" {
  description = "Secret name"
  value       = kubernetes_secret.zeta_secrets.metadata[0].name
}

output "pvc_name" {
  description = "Persistent Volume Claim name"
  value       = kubernetes_persistent_volume_claim.vector_storage.metadata[0].name
}

output "ingress_url" {
  description = "Ingress URL (if enabled)"
  value       = var.enable_ingress ? "https://${var.domain}" : "Not enabled"
}

output "environment" {
  description = "Deployment environment"
  value       = var.environment
}

output "application_version" {
  description = "Application version"
  value       = var.app_version
}

output "autoscaling_enabled" {
  description = "Whether autoscaling is enabled"
  value       = var.enable_autoscaling
}

output "replica_count" {
  description = "Current replica count"
  value       = var.replicas
}

output "resource_limits" {
  description = "Container resource limits"
  value = {
    cpu    = var.cpu_limit
    memory = var.memory_limit
  }
}

output "resource_requests" {
  description = "Container resource requests"
  value = {
    cpu    = var.cpu_request
    memory = var.memory_request
  }
}

output "storage_info" {
  description = "Storage configuration"
  value = {
    size  = var.storage_size
    class = var.storage_class
  }
}

output "service_endpoints" {
  description = "Service endpoints"
  value = {
    http    = "http://${kubernetes_service.zeta_agent.spec[0].cluster_ip}:80"
    metrics = "http://${kubernetes_service.zeta_agent.spec[0].cluster_ip}:9090"
  }
}
