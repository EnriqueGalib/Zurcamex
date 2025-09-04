"""
Generador de Reportes de Ejecución - Documento de Resumen Final
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path

class ExecutionReportGenerator:
    """Generador de reportes de ejecución con detalles completos"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def generate_execution_report(self, execution_data):
        """Genera un reporte completo de la ejecución"""
        try:
            self.logger.info("Generando reporte de ejecución...")
            
            # Crear directorio de reportes si no existe
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            
            # Obtener información del feature y fecha
            exec_info = execution_data.get('execution_info', {})
            execution_date = exec_info.get('execution_date', datetime.now().strftime("%Y-%m-%d"))
            test_name = exec_info.get('test_name', 'unknown_test')
            
            # Crear nombre de carpeta: fecha + nombre del feature
            safe_test_name = self._sanitize_name(test_name)
            feature_folder = f"{execution_date}_{safe_test_name}"
            
            # Crear directorio específico para el feature
            feature_reports_dir = reports_dir / feature_folder
            feature_reports_dir.mkdir(exist_ok=True)
            
            # Generar nombre del archivo de reporte
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"execution_report_{timestamp}.html"
            report_path = feature_reports_dir / report_filename
            
            # Generar contenido del reporte
            report_content = self._create_report_content(execution_data)
            
            # Guardar reporte HTML
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            # También generar versión JSON para procesamiento automático
            json_report_path = feature_reports_dir / f"execution_report_{timestamp}.json"
            with open(json_report_path, 'w', encoding='utf-8') as f:
                json.dump(execution_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Reporte generado: {report_path}")
            self.logger.info(f"Reporte JSON generado: {json_report_path}")
            self.logger.info(f"Carpeta de reportes: {feature_reports_dir}")
            
            return str(report_path), str(json_report_path)
            
        except Exception as e:
            self.logger.error(f"Error generando reporte de ejecución: {str(e)}")
            return None, None
    
    def _create_report_content(self, execution_data):
        """Crea el contenido HTML del reporte"""
        
        # Template HTML con estilos modernos
        html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Ejecución - {{ execution_data.execution_info.test_name }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .status-badge {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 1.1em;
            margin-top: 15px;
        }
        
        .status-success {
            background-color: #4CAF50;
            color: white;
        }
        
        .status-failed {
            background-color: #f44336;
            color: white;
        }
        
        .status-partial {
            background-color: #ff9800;
            color: white;
        }
        
        .section {
            background: white;
            margin-bottom: 30px;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .section h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .info-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .info-item strong {
            color: #667eea;
            display: block;
            margin-bottom: 5px;
        }
        
        .steps-list {
            list-style: none;
        }
        
        .step-item {
            background: #f8f9fa;
            margin-bottom: 15px;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
            position: relative;
        }
        
        .step-item.failed {
            border-left-color: #f44336;
            background: #ffebee;
        }
        
        .step-item.partial {
            border-left-color: #ff9800;
            background: #fff3e0;
        }
        
        .step-number {
            position: absolute;
            top: -10px;
            left: 20px;
            background: #667eea;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }
        
        .step-item.failed .step-number {
            background: #f44336;
        }
        
        .step-item.partial .step-number {
            background: #ff9800;
        }
        
        .step-title {
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }
        
        .step-details {
            color: #666;
            margin-bottom: 10px;
        }
        
        .step-evidence {
            background: #e3f2fd;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }
        
        .evidence-link {
            color: #1976d2;
            text-decoration: none;
            font-weight: bold;
        }
        
        .evidence-link:hover {
            text-decoration: underline;
        }
        
        .summary-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #666;
            border-top: 1px solid #ddd;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .info-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Reporte de Ejecución</h1>
            <div class="subtitle">{{ execution_data.execution_info.test_name }}</div>
            <div class="status-badge status-{{ execution_data.execution_info.overall_status.lower() }}">
                {{ execution_data.execution_info.overall_status }}
            </div>
        </div>
        
        <div class="section">
            <h2>📋 Información General</h2>
            <div class="info-grid">
                <div class="info-item">
                    <strong>🗓️ Fecha de Ejecución</strong>
                    {{ execution_data.execution_info.execution_date }}
                </div>
                <div class="info-item">
                    <strong>⏰ Hora de Inicio</strong>
                    {{ execution_data.execution_info.start_time }}
                </div>
                <div class="info-item">
                    <strong>⏱️ Duración Total</strong>
                    {{ execution_data.execution_info.total_duration }}
                </div>
                <div class="info-item">
                    <strong>🎯 Tipo de Ejecución</strong>
                    {{ execution_data.execution_info.execution_type }}
                </div>
                <div class="info-item">
                    <strong>📁 Directorio de Evidencias</strong>
                    {{ execution_data.execution_info.evidence_directory }}
                </div>
                <div class="info-item">
                    <strong>📝 Log de Ejecución</strong>
                    {{ execution_data.execution_info.log_file }}
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📈 Resumen de Resultados</h2>
            <div class="summary-stats">
                <div class="stat-card">
                    <div class="stat-number">{{ execution_data.summary.total_steps }}</div>
                    <div class="stat-label">Pasos Ejecutados</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ execution_data.summary.successful_steps }}</div>
                    <div class="stat-label">Pasos Exitosos</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ execution_data.summary.failed_steps }}</div>
                    <div class="stat-label">Pasos Fallidos</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ execution_data.summary.screenshots_taken }}</div>
                    <div class="stat-label">Screenshots</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>👣 Detalle de Pasos</h2>
            <ol class="steps-list">
                {% for step in execution_data.steps %}
                <li class="step-item {{ step.status.lower() }}">
                    <div class="step-number">{{ loop.index }}</div>
                    <div class="step-title">{{ step.name }}</div>
                    <div class="step-details">
                        <strong>Descripción:</strong> {{ step.description }}<br>
                        <strong>Estado:</strong> {{ step.status }}<br>
                        <strong>Duración:</strong> {{ step.duration }}<br>
                        <strong>Timestamp:</strong> {{ step.timestamp }}
                    </div>
                    {% if step.evidence %}
                    <div class="step-evidence">
                        <strong>📸 Evidencias:</strong><br>
                        {% for evidence in step.evidence %}
                        <a href="{{ evidence.path }}" class="evidence-link" target="_blank">
                            {{ evidence.name }} ({{ evidence.timestamp }})
                        </a><br>
                        {% endfor %}
                    </div>
                    {% endif %}
                </li>
                {% endfor %}
            </ol>
        </div>
        
        {% if execution_data.features %}
        <div class="section">
            <h2>🔧 Features Ejecutados</h2>
            <div class="info-grid">
                {% for feature in execution_data.features %}
                <div class="info-item">
                    <strong>{{ feature.name }}</strong><br>
                    Scenarios: {{ feature.scenarios_count }}<br>
                    Estado: {{ feature.status }}<br>
                    Duración: {{ feature.duration }}
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
        
        <div class="footer">
            <p>Reporte generado automáticamente el {{ execution_data.execution_info.report_generated_at }}</p>
            <p>Sistema de Automatización de Pruebas - Zucarmex</p>
        </div>
    </div>
</body>
</html>
        """
        
        # Renderizar template manualmente (sin jinja2)
        return self._render_template(html_template, execution_data)
    
    def _render_template(self, template, data):
        """Renderiza el template HTML manualmente"""
        try:
            # Reemplazar variables del template
            html = template
            
            # Reemplazar variables de execution_info
            exec_info = data.get('execution_info', {})
            for key, value in exec_info.items():
                html = html.replace(f"{{{{ execution_data.execution_info.{key} }}}}", str(value))
            
            # Reemplazar variables de summary
            summary = data.get('summary', {})
            for key, value in summary.items():
                html = html.replace(f"{{{{ execution_data.summary.{key} }}}}", str(value))
            
            # Reemplazar sección de steps
            steps_html = ""
            steps = data.get('steps', [])
            for i, step in enumerate(steps, 1):
                step_html = f"""
                <li class="step-item {step.get('status', 'UNKNOWN').lower()}">
                    <div class="step-number">{i}</div>
                    <div class="step-title">{step.get('name', 'Paso sin nombre')}</div>
                    <div class="step-details">
                        <strong>Descripción:</strong> {step.get('description', 'Sin descripción')}<br>
                        <strong>Estado:</strong> {step.get('status', 'UNKNOWN')}<br>
                        <strong>Duración:</strong> {step.get('duration', 'No disponible')}<br>
                        <strong>Timestamp:</strong> {step.get('timestamp', 'No disponible')}
                    </div>
                """
                
                # Agregar evidencias si existen
                evidence = step.get('evidence', [])
                if evidence:
                    step_html += '<div class="step-evidence"><strong>📸 Evidencias:</strong><br>'
                    for ev in evidence:
                        step_html += f'<a href="{ev.get("path", "#")}" class="evidence-link" target="_blank">{ev.get("name", "Evidencia")} ({ev.get("timestamp", "Sin timestamp")})</a><br>'
                    step_html += '</div>'
                
                step_html += '</li>'
                steps_html += step_html
            
            html = html.replace("{% for step in execution_data.steps %}\n                <li class=\"step-item {{ step.status.lower() }}\">\n                    <div class=\"step-number\">{{ loop.index }}</div>\n                    <div class=\"step-title\">{{ step.name }}</div>\n                    <div class=\"step-details\">\n                        <strong>Descripción:</strong> {{ step.description }}<br>\n                        <strong>Estado:</strong> {{ step.status }}<br>\n                        <strong>Duración:</strong> {{ step.duration }}<br>\n                        <strong>Timestamp:</strong> {{ step.timestamp }}\n                    </div>\n                    {% if step.evidence %}\n                    <div class=\"step-evidence\">\n                        <strong>📸 Evidencias:</strong><br>\n                        {% for evidence in step.evidence %}\n                        <a href=\"{{ evidence.path }}\" class=\"evidence-link\" target=\"_blank\">\n                            {{ evidence.name }} ({{ evidence.timestamp }})\n                        </a><br>\n                        {% endfor %}\n                    </div>\n                    {% endif %}\n                </li>\n                {% endfor %}", steps_html)
            
            # Reemplazar sección de features
            features_html = ""
            features = data.get('features', [])
            for feature in features:
                features_html += f"""
                <div class="info-item">
                    <strong>{feature.get('name', 'Feature sin nombre')}</strong><br>
                    Scenarios: {feature.get('scenarios_count', 0)}<br>
                    Estado: {feature.get('status', 'UNKNOWN')}<br>
                    Duración: {feature.get('duration', 'No disponible')}
                </div>
                """
            
            html = html.replace("{% for feature in execution_data.features %}\n                <div class=\"info-item\">\n                    <strong>{{ feature.name }}</strong><br>\n                    Scenarios: {{ feature.scenarios_count }}<br>\n                    Estado: {{ feature.status }}<br>\n                    Duración: {{ feature.duration }}\n                </div>\n                {% endfor %}", features_html)
            
            # Remover sección de features si no hay features
            if not features:
                html = html.replace("{% if execution_data.features %}\n        <div class=\"section\">\n            <h2>🔧 Features Ejecutados</h2>\n            <div class=\"info-grid\">\n                {% for feature in execution_data.features %}\n                <div class=\"info-item\">\n                    <strong>{{ feature.name }}</strong><br>\n                    Scenarios: {{ feature.scenarios_count }}<br>\n                    Estado: {{ feature.status }}<br>\n                    Duración: {{ feature.duration }}\n                </div>\n                {% endfor %}\n            </div>\n        </div>\n        {% endif %}", "")
            
            return html
            
        except Exception as e:
            self.logger.error(f"Error renderizando template: {str(e)}")
            return template  # Devolver template original si hay error
    
    def _sanitize_name(self, name):
        """Sanitiza el nombre para usar en nombres de archivos y carpetas"""
        import re
        # Remover caracteres especiales y espacios
        sanitized = re.sub(r'[^\w\s-]', '', str(name)).strip()
        # Reemplazar espacios y guiones múltiples con un solo guión
        sanitized = re.sub(r'[-\s]+', '_', sanitized)
        # Limitar longitud
        return sanitized[:50] if len(sanitized) > 50 else sanitized
    
    def collect_execution_data(self, context, scenario=None, feature=None):
        """Recolecta datos de la ejecución para el reporte"""
        try:
            execution_data = {
                "execution_info": {
                    "test_name": self._get_test_name(scenario, feature),
                    "execution_date": datetime.now().strftime("%Y-%m-%d"),
                    "start_time": getattr(context, 'start_time', datetime.now().strftime("%H:%M:%S")),
                    "total_duration": self._calculate_duration(context),
                    "execution_type": self._get_execution_type(scenario, feature),
                    "evidence_directory": getattr(context, 'evidence_dir', 'No disponible'),
                    "log_file": getattr(context, 'log_file', 'No disponible'),
                    "overall_status": self._get_overall_status(context),
                    "report_generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                "summary": {
                    "total_steps": len(getattr(context, 'executed_steps', [])),
                    "successful_steps": len([s for s in getattr(context, 'executed_steps', []) if s.get('status') == 'SUCCESS']),
                    "failed_steps": len([s for s in getattr(context, 'executed_steps', []) if s.get('status') == 'FAILED']),
                    "screenshots_taken": self._count_screenshots(context)
                },
                "steps": self._collect_steps_data(context),
                "features": self._collect_features_data(context, feature)
            }
            
            return execution_data
            
        except Exception as e:
            self.logger.error(f"Error recolectando datos de ejecución: {str(e)}")
            return self._create_fallback_data()
    
    def _get_test_name(self, scenario, feature):
        """Obtiene el nombre de la prueba"""
        if scenario:
            return f"{scenario.name}"
        elif feature:
            return f"{feature.name}"
        else:
            return "Ejecución de Pruebas"
    
    def _calculate_duration(self, context):
        """Calcula la duración total de la ejecución"""
        if hasattr(context, 'start_time') and hasattr(context, 'end_time'):
            try:
                start = datetime.strptime(context.start_time, "%H:%M:%S")
                end = datetime.strptime(context.end_time, "%H:%M:%S")
                duration = end - start
                return str(duration)
            except:
                pass
        return "No disponible"
    
    def _get_execution_type(self, scenario, feature):
        """Determina el tipo de ejecución"""
        if scenario and feature:
            return f"Scenario: {scenario.name} del Feature: {feature.name}"
        elif feature:
            return f"Feature completo: {feature.name}"
        else:
            return "Todos los features"
    
    def _get_overall_status(self, context):
        """Determina el estado general de la ejecución"""
        if hasattr(context, 'executed_steps'):
            failed_steps = len([s for s in context.executed_steps if s.get('status') == 'FAILED'])
            if failed_steps == 0:
                return "SUCCESS"
            elif failed_steps < len(context.executed_steps):
                return "PARTIAL"
            else:
                return "FAILED"
        return "UNKNOWN"
    
    def _count_screenshots(self, context):
        """Cuenta el número de screenshots tomados"""
        if hasattr(context, 'screenshots_taken'):
            return context.screenshots_taken
        return 0
    
    def _collect_steps_data(self, context):
        """Recolecta datos de los pasos ejecutados"""
        steps = []
        if hasattr(context, 'executed_steps'):
            for i, step in enumerate(context.executed_steps, 1):
                step_data = {
                    "number": i,
                    "name": step.get('name', f'Paso {i}'),
                    "description": step.get('description', 'Sin descripción'),
                    "status": step.get('status', 'UNKNOWN'),
                    "duration": step.get('duration', 'No disponible'),
                    "timestamp": step.get('timestamp', datetime.now().strftime("%H:%M:%S")),
                    "evidence": step.get('evidence', [])
                }
                steps.append(step_data)
        return steps
    
    def _collect_features_data(self, context, feature):
        """Recolecta datos de los features ejecutados"""
        features = []
        if feature:
            feature_data = {
                "name": feature.name,
                "scenarios_count": 1,  # Por ahora asumimos 1 scenario
                "status": getattr(context, 'overall_status', 'UNKNOWN'),
                "duration": self._calculate_duration(context)
            }
            features.append(feature_data)
        return features
    
    def _create_fallback_data(self):
        """Crea datos de fallback si hay errores"""
        return {
            "execution_info": {
                "test_name": "Ejecución de Pruebas",
                "execution_date": datetime.now().strftime("%Y-%m-%d"),
                "start_time": datetime.now().strftime("%H:%M:%S"),
                "total_duration": "No disponible",
                "execution_type": "Desconocido",
                "evidence_directory": "No disponible",
                "log_file": "No disponible",
                "overall_status": "UNKNOWN",
                "report_generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "summary": {
                "total_steps": 0,
                "successful_steps": 0,
                "failed_steps": 0,
                "screenshots_taken": 0
            },
            "steps": [],
            "features": []
        }
