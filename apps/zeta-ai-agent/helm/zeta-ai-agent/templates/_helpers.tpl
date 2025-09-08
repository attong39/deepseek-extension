{{/*
Expand the name of the chart.
*/}}
{{- define "zeta-ai-agent.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "zeta-ai-agent.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "zeta-ai-agent.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "zeta-ai-agent.labels" -}}
helm.sh/chart: {{ include "zeta-ai-agent.chart" . }}
{{ include "zeta-ai-agent.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/component: ai-agent
app.kubernetes.io/part-of: zeta-platform
{{- end }}

{{/*
Selector labels
*/}}
{{- define "zeta-ai-agent.selectorLabels" -}}
app.kubernetes.io/name: {{ include "zeta-ai-agent.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "zeta-ai-agent.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "zeta-ai-agent.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create the name of the config map to use
*/}}
{{- define "zeta-ai-agent.configMapName" -}}
{{- if .Values.configMap.enabled }}
{{- printf "%s-config" (include "zeta-ai-agent.fullname" .) }}
{{- else }}
{{- default "default" .Values.configMap.name }}
{{- end }}
{{- end }}

{{/*
Create the name of the secret to use
*/}}
{{- define "zeta-ai-agent.secretName" -}}
{{- if .Values.secret.enabled }}
{{- printf "%s-secret" (include "zeta-ai-agent.fullname" .) }}
{{- else }}
{{- default "default" .Values.secret.name }}
{{- end }}
{{- end }}

{{/*
Create the name of the PVC to use
*/}}
{{- define "zeta-ai-agent.pvcName" -}}
{{- if .Values.persistence.enabled }}
{{- printf "%s-pvc" (include "zeta-ai-agent.fullname" .) }}
{{- else }}
{{- .Values.persistence.existingClaim }}
{{- end }}
{{- end }}

{{/*
Generate the ServiceMonitor name
*/}}
{{- define "zeta-ai-agent.serviceMonitorName" -}}
{{- printf "%s-metrics" (include "zeta-ai-agent.fullname" .) }}
{{- end }}

{{/*
Generate the PrometheusRule name
*/}}
{{- define "zeta-ai-agent.prometheusRuleName" -}}
{{- printf "%s-alerts" (include "zeta-ai-agent.fullname" .) }}
{{- end }}
