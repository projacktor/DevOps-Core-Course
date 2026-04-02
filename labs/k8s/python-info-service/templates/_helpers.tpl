{{/* Expand chart name */}}
{{- define "python-info-service.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/* Build fully qualified app name */}}
{{- define "python-info-service.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}

{{/* Chart name and version */}}
{{- define "python-info-service.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/* Labels used by all resources */}}
{{- define "python-info-service.labels" -}}
helm.sh/chart: {{ include "python-info-service.chart" . }}
{{ include "python-info-service.selectorLabels" . }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{/* Minimal selector labels */}}
{{- define "python-info-service.selectorLabels" -}}
app.kubernetes.io/name: {{ include "python-info-service.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app: {{ include "python-info-service.name" . }}
{{- end -}}
