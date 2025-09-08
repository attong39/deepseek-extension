{{/*
Expand the name of the chart.
*/}}
{{- define "zeta-agent.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "zeta-agent.fullname" -}}
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
{{- define "zeta-agent.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "zeta-agent.labels" -}}
helm.sh/chart: {{ include "zeta-agent.chart" . }}
{{ include "zeta-agent.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- with .Values.commonLabels }}
{{ toYaml . }}
{{- end }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "zeta-agent.selectorLabels" -}}
app.kubernetes.io/name: {{ include "zeta-agent.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "zeta-agent.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "zeta-agent.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create the name of the secret to use
*/}}
{{- define "zeta-agent.secretName" -}}
{{- printf "%s-secrets" (include "zeta-agent.fullname" .) }}
{{- end }}

{{/*
Create the name of the configmap to use
*/}}
{{- define "zeta-agent.configMapName" -}}
{{- printf "%s-config" (include "zeta-agent.fullname" .) }}
{{- end }}

{{/*
Create the name of the PVC to use
*/}}
{{- define "zeta-agent.pvcName" -}}
{{- printf "%s-storage" (include "zeta-agent.fullname" .) }}
{{- end }}

{{/*
Return the proper image name
*/}}
{{- define "zeta-agent.image" -}}
{{- $registryName := .Values.image.registry -}}
{{- $repositoryName := .Values.image.repository -}}
{{- $tag := .Values.image.tag | toString -}}
{{- if .Values.global.imageRegistry }}
    {{- printf "%s/%s:%s" .Values.global.imageRegistry $repositoryName $tag -}}
{{- else -}}
    {{- printf "%s/%s:%s" $registryName $repositoryName $tag -}}
{{- end -}}
{{- end }}

{{/*
Return the proper Docker Image Registry Secret Names
*/}}
{{- define "zeta-agent.imagePullSecrets" -}}
{{- if .Values.global.imagePullSecrets }}
imagePullSecrets:
{{- range .Values.global.imagePullSecrets }}
  - name: {{ . }}
{{- end }}
{{- else if .Values.image.pullSecrets }}
imagePullSecrets:
{{- range .Values.image.pullSecrets }}
  - name: {{ . }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Return the target Kubernetes version
*/}}
{{- define "zeta-agent.capabilities.kubeVersion" -}}
{{- if .Values.global }}
    {{- if .Values.global.kubeVersion }}
    {{- .Values.global.kubeVersion -}}
    {{- else }}
    {{- default .Capabilities.KubeVersion.Version .Values.kubeVersion -}}
    {{- end -}}
{{- else }}
{{- default .Capabilities.KubeVersion.Version .Values.kubeVersion -}}
{{- end -}}
{{- end -}}

{{/*
Return the appropriate apiVersion for deployment.
*/}}
{{- define "zeta-agent.deployment.apiVersion" -}}
{{- if semverCompare "<1.14-0" (include "zeta-agent.capabilities.kubeVersion" .) -}}
{{- print "extensions/v1beta1" -}}
{{- else -}}
{{- print "apps/v1" -}}
{{- end -}}
{{- end -}}

{{/*
Return the appropriate apiVersion for ingress.
*/}}
{{- define "zeta-agent.ingress.apiVersion" -}}
{{- if semverCompare "<1.14-0" (include "zeta-agent.capabilities.kubeVersion" .) -}}
{{- print "extensions/v1beta1" -}}
{{- else if semverCompare "<1.19-0" (include "zeta-agent.capabilities.kubeVersion" .) -}}
{{- print "networking.k8s.io/v1beta1" -}}
{{- else -}}
{{- print "networking.k8s.io/v1" -}}
{{- end -}}
{{- end -}}

{{/*
Return the appropriate apiVersion for networkPolicy.
*/}}
{{- define "zeta-agent.networkPolicy.apiVersion" -}}
{{- if semverCompare "<1.7-0" (include "zeta-agent.capabilities.kubeVersion" .) -}}
{{- print "extensions/v1beta1" -}}
{{- else -}}
{{- print "networking.k8s.io/v1" -}}
{{- end -}}
{{- end -}}

{{/*
Compile all warnings into a single message, and call fail.
*/}}
{{- define "zeta-agent.validateValues" -}}
{{- $messages := list -}}
{{- $messages := append $messages (include "zeta-agent.validateValues.persistence" .) -}}
{{- $messages := append $messages (include "zeta-agent.validateValues.ingress" .) -}}
{{- $messages := without $messages "" -}}
{{- $message := join "\n" $messages -}}
{{- if $message -}}
{{- printf "\nVALUES VALIDATION:\n%s" $message | fail -}}
{{- end -}}
{{- end -}}

{{/*
Validate values of Zeta Agent - Persistence
*/}}
{{- define "zeta-agent.validateValues.persistence" -}}
{{- if and .Values.persistence.enabled (not .Values.persistence.size) -}}
zeta-agent: persistence.size
    You must provide a size when persistence is enabled
{{- end -}}
{{- end -}}

{{/*
Validate values of Zeta Agent - Ingress
*/}}
{{- define "zeta-agent.validateValues.ingress" -}}
{{- if and .Values.ingress.enabled (not .Values.ingress.hosts) -}}
zeta-agent: ingress.hosts
    You must provide hosts when ingress is enabled
{{- end -}}
{{- end -}}

{{/*
Generate certificates for webhook
*/}}
{{- define "zeta-agent.gen-certs" -}}
{{- $altNames := list ( printf "%s.%s" (include "zeta-agent.fullname" .) .Release.Namespace ) ( printf "%s.%s.svc" (include "zeta-agent.fullname" .) .Release.Namespace ) -}}
{{- $ca := genCA "zeta-agent-ca" 365 -}}
{{- $cert := genSignedCert ( include "zeta-agent.fullname" . ) nil $altNames 365 $ca -}}
tls.crt: {{ $cert.Cert | b64enc }}
tls.key: {{ $cert.Key | b64enc }}
ca.crt: {{ $ca.Cert | b64enc }}
{{- end -}}
