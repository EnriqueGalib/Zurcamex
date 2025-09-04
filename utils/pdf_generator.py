"""
Generador de Documentos PDF - Para Compartir con Clientes
"""

import json
import logging
import os
import re
from datetime import datetime
from pathlib import Path


class PDFGenerator:
    """Generador de documentos PDF profesionales para compartir con clientes"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generate_execution_pdf(self, execution_data, log_file_path=None):
        """Genera un documento PDF completo de la ejecución organizado por fecha y feature"""
        try:
            self.logger.info("Generando documento PDF de ejecución...")

            # Crear directorio de PDFs si no existe
            pdfs_dir = Path("pdfs")
            pdfs_dir.mkdir(exist_ok=True)

            # Obtener información del feature y fecha
            exec_info = execution_data.get("execution_info", {})
            execution_date = exec_info.get(
                "execution_date", datetime.now().strftime("%Y-%m-%d")
            )
            test_name = exec_info.get("test_name", "unknown_test")
            feature_name = exec_info.get("feature_name", test_name)

            # Crear estructura organizada: fecha/feature/resultado
            safe_date = execution_date.replace("-", "_")
            safe_feature_name = self._sanitize_name(feature_name)
            safe_test_name = self._sanitize_name(test_name)

            # Directorio por fecha
            date_dir = pdfs_dir / safe_date
            date_dir.mkdir(exist_ok=True)

            # Directorio por feature dentro de la fecha
            feature_dir = date_dir / safe_feature_name
            feature_dir.mkdir(exist_ok=True)

            # Generar nombre del archivo PDF con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            overall_status = exec_info.get("overall_status", "UNKNOWN")

            if overall_status == "SUCCESS":
                pdf_filename = f"SUCCESS_{safe_test_name}_{timestamp}.html"
                status_dir = feature_dir / "EXITOSOS"
            elif overall_status == "FAILED":
                pdf_filename = f"FAILURE_ANALYSIS_{safe_test_name}_{timestamp}.html"
                status_dir = feature_dir / "FALLIDOS"
            else:
                pdf_filename = f"EXECUTION_REPORT_{safe_test_name}_{timestamp}.html"
                status_dir = feature_dir / "PARCIALES"

            # Crear directorio por resultado
            status_dir.mkdir(exist_ok=True)

            # Ruta final del archivo
            pdf_path = status_dir / pdf_filename

            # Generar contenido del PDF
            pdf_content = self._create_pdf_content(execution_data, log_file_path)

            # Guardar como archivo HTML (optimizado para conversión a PDF)
            with open(pdf_path, "w", encoding="utf-8") as f:
                f.write(pdf_content)

            # Crear archivo de metadatos
            metadata_path = pdf_path.with_suffix(".json")
            metadata = {
                "execution_info": exec_info,
                "generation_timestamp": datetime.now().isoformat(),
                "pdf_path": str(pdf_path),
                "log_file": log_file_path,
                "feature_name": feature_name,
                "test_name": test_name,
                "execution_date": execution_date,
                "overall_status": overall_status,
            }

            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            self.logger.info(f"Documento PDF generado: {pdf_path}")
            self.logger.info(f"Metadatos guardados: {metadata_path}")
            self.logger.info(
                f"Organizado en: {date_dir.name}/{feature_dir.name}/{status_dir.name}"
            )

            return str(pdf_path), str(metadata_path)

        except Exception as e:
            self.logger.error(f"Error generando documento PDF: {str(e)}")
            return None, None

    def _create_pdf_content(self, execution_data, log_file_path=None):
        """Crea el contenido HTML optimizado para PDF"""
        exec_info = execution_data.get("execution_info", {})
        overall_status = exec_info.get("overall_status", "UNKNOWN")

        # Determinar el tipo de documento
        if overall_status == "SUCCESS":
            return self._create_success_pdf_content(execution_data)
        elif overall_status == "FAILED":
            return self._create_failure_pdf_content(execution_data, log_file_path)
        else:
            return self._create_general_pdf_content(execution_data)

    def _create_success_pdf_content(self, execution_data):
        """Crea el contenido PDF para ejecuciones exitosas"""
        exec_info = execution_data.get("execution_info", {})
        summary = execution_data.get("summary", {})
        steps = execution_data.get("steps", [])

        html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Ejecución Exitosa - {exec_info.get('test_name', 'Test')}</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}

        body {{
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
        }}

        .header {{
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 30px;
            text-align: center;
            margin-bottom: 30px;
            border-radius: 10px;
        }}

        .header h1 {{
            font-size: 24px;
            margin: 0 0 10px 0;
        }}

        .header .subtitle {{
            font-size: 16px;
            opacity: 0.9;
        }}

        .status-badge {{
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 14px;
            margin-top: 15px;
            background-color: #4CAF50;
            color: white;
        }}

        .section {{
            margin-bottom: 30px;
            page-break-inside: avoid;
        }}

        .section h2 {{
            color: #4CAF50;
            margin-bottom: 20px;
            font-size: 18px;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }}

        .info-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}

        .info-item {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
        }}

        .info-item strong {{
            color: #4CAF50;
            display: block;
            margin-bottom: 5px;
        }}

        .summary-stats {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-top: 20px;
        }}

        .stat-card {{
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}

        .stat-number {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .stat-label {{
            font-size: 12px;
            opacity: 0.9;
        }}

        .steps-list {{
            list-style: none;
            padding: 0;
        }}

        .step-item {{
            background: #f8f9fa;
            margin-bottom: 15px;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
            page-break-inside: avoid;
        }}

        .step-number {{
            background: #4CAF50;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 15px;
        }}

        .step-title {{
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }}

        .step-details {{
            color: #666;
            margin-bottom: 10px;
        }}

        .step-evidence {{
            background: #e8f5e8;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }}

        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #666;
            border-top: 1px solid #ddd;
            font-size: 12px;
        }}

        .company-logo {{
            text-align: center;
            margin-bottom: 20px;
        }}

        .company-logo h2 {{
            color: #4CAF50;
            margin: 0;
            font-size: 20px;
        }}
    </style>
</head>
<body>
    <div class="company-logo">
        <h2>🏢 ZUCARMEX - Sistema de Automatización de Pruebas</h2>
    </div>

    <div class="header">
        <h1>✅ Reporte de Ejecución Exitosa</h1>
        <div class="subtitle">{exec_info.get('test_name', 'Test')}</div>
        <div class="status-badge">EJECUCIÓN EXITOSA</div>
    </div>

    <div class="section">
        <h2>📋 Información General</h2>
        <div class="info-grid">
            <div class="info-item">
                <strong>🗓️ Fecha de Ejecución</strong>
                {exec_info.get('execution_date', 'N/A')}
            </div>
            <div class="info-item">
                <strong>⏰ Hora de Inicio</strong>
                {exec_info.get('start_time', 'N/A')}
            </div>
            <div class="info-item">
                <strong>⏱️ Duración Total</strong>
                {exec_info.get('total_duration', 'N/A')}
            </div>
            <div class="info-item">
                <strong>🎯 Tipo de Ejecución</strong>
                {exec_info.get('execution_type', 'N/A')}
            </div>
        </div>
    </div>

    <div class="section">
        <h2>📈 Resumen de Resultados</h2>
        <div class="summary-stats">
            <div class="stat-card">
                <div class="stat-number">{summary.get('total_steps', 0)}</div>
                <div class="stat-label">Pasos Ejecutados</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{summary.get('successful_steps', 0)}</div>
                <div class="stat-label">Pasos Exitosos</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{summary.get('failed_steps', 0)}</div>
                <div class="stat-label">Pasos Fallidos</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{summary.get('screenshots_taken', 0)}</div>
                <div class="stat-label">Screenshots</div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>👣 Detalle de Pasos Ejecutados</h2>
        <ol class="steps-list">
"""

        for i, step in enumerate(steps, 1):
            status_emoji = (
                "✅"
                if step.get("status") == "SUCCESS"
                else "❌" if step.get("status") == "FAILED" else "⚠️"
            )
            html_content += f"""
            <li class="step-item">
                <span class="step-number">{i}</span>
                <div class="step-title">{status_emoji} {step.get('name', 'Paso sin nombre')}</div>
                <div class="step-details">
                    <strong>Descripción:</strong> {step.get('description', 'Sin descripción')}<br>
                    <strong>Estado:</strong> {step.get('status', 'UNKNOWN')}<br>
                    <strong>Duración:</strong> {step.get('duration', 'No disponible')}<br>
                    <strong>Timestamp:</strong> {step.get('timestamp', 'No disponible')}
                </div>
"""

            # Agregar evidencias si existen
            evidence = step.get("evidence", [])
            if evidence:
                html_content += (
                    '<div class="step-evidence"><strong>📸 Evidencias:</strong><br>'
                )
                for ev in evidence:
                    html_content += f'• {ev.get("name", "Evidencia")} ({ev.get("timestamp", "Sin timestamp")})<br>'
                html_content += "</div>"

            html_content += "</li>"

        html_content += f"""
        </ol>
    </div>

    <div class="section">
        <h2>🎉 Conclusión</h2>
        <p>Esta ejecución se completó <strong>exitosamente</strong> con {summary.get('successful_steps', 0)} de {summary.get('total_steps', 0)} pasos ejecutados correctamente.</p>

        <h3>📁 Archivos Generados</h3>
        <ul>
            <li><strong>📄 Reporte HTML:</strong> {exec_info.get('evidence_directory', 'N/A')}/reports/</li>
            <li><strong>📸 Screenshots:</strong> {exec_info.get('evidence_directory', 'N/A')}/screenshots/</li>
            <li><strong>📝 Log de Ejecución:</strong> {exec_info.get('log_file', 'N/A')}</li>
        </ul>
    </div>

    <div class="footer">
        <p>Reporte generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Sistema de Automatización de Pruebas - Zucarmex</p>
        <p>Este documento es confidencial y está destinado únicamente para uso interno del cliente.</p>
    </div>
</body>
</html>
"""

        return html_content

    def _create_failure_pdf_content(self, execution_data, log_file_path):
        """Crea el contenido PDF para ejecuciones fallidas"""
        exec_info = execution_data.get("execution_info", {})
        summary = execution_data.get("summary", {})
        steps = execution_data.get("steps", [])

        # Analizar el log si está disponible
        log_analysis = self._analyze_log_file(log_file_path) if log_file_path else {}

        html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análisis de Fallo - {exec_info.get('test_name', 'Test')}</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}

        body {{
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
        }}

        .header {{
            background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
            color: white;
            padding: 30px;
            text-align: center;
            margin-bottom: 30px;
            border-radius: 10px;
        }}

        .header h1 {{
            font-size: 24px;
            margin: 0 0 10px 0;
        }}

        .header .subtitle {{
            font-size: 16px;
            opacity: 0.9;
        }}

        .status-badge {{
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 14px;
            margin-top: 15px;
            background-color: #f44336;
            color: white;
        }}

        .section {{
            margin-bottom: 30px;
            page-break-inside: avoid;
        }}

        .section h2 {{
            color: #f44336;
            margin-bottom: 20px;
            font-size: 18px;
            border-bottom: 2px solid #f44336;
            padding-bottom: 10px;
        }}

        .info-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}

        .info-item {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #f44336;
        }}

        .info-item strong {{
            color: #f44336;
            display: block;
            margin-bottom: 5px;
        }}

        .error-item {{
            background: #ffebee;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #f44336;
            margin-bottom: 15px;
        }}

        .error-title {{
            font-weight: bold;
            color: #f44336;
            margin-bottom: 10px;
        }}

        .recommendations {{
            background: #fff3e0;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #ff9800;
        }}

        .recommendations h3 {{
            color: #ff9800;
            margin-top: 0;
        }}

        .checklist {{
            background: #e8f5e8;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
        }}

        .checklist h3 {{
            color: #4CAF50;
            margin-top: 0;
        }}

        .company-logo {{
            text-align: center;
            margin-bottom: 20px;
        }}

        .company-logo h2 {{
            color: #f44336;
            margin: 0;
            font-size: 20px;
        }}

        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #666;
            border-top: 1px solid #ddd;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="company-logo">
        <h2>🏢 ZUCARMEX - Sistema de Automatización de Pruebas</h2>
    </div>

    <div class="header">
        <h1>❌ Análisis de Fallo</h1>
        <div class="subtitle">{exec_info.get('test_name', 'Test')}</div>
        <div class="status-badge">EJECUCIÓN FALLIDA</div>
    </div>

    <div class="section">
        <h2>🚨 Resumen del Fallo</h2>
        <div class="info-grid">
            <div class="info-item">
                <strong>🗓️ Fecha de Ejecución</strong>
                {exec_info.get('execution_date', 'N/A')}
            </div>
            <div class="info-item">
                <strong>⏰ Hora de Inicio</strong>
                {exec_info.get('start_time', 'N/A')}
            </div>
            <div class="info-item">
                <strong>⏱️ Duración Total</strong>
                {exec_info.get('total_duration', 'N/A')}
            </div>
            <div class="info-item">
                <strong>🎯 Tipo de Ejecución</strong>
                {exec_info.get('execution_type', 'N/A')}
            </div>
        </div>
    </div>

    <div class="section">
        <h2>📊 Estadísticas del Fallo</h2>
        <div class="info-grid">
            <div class="info-item">
                <strong>📈 Total de Pasos</strong>
                {summary.get('total_steps', 0)}
            </div>
            <div class="info-item">
                <strong>✅ Pasos Exitosos</strong>
                {summary.get('successful_steps', 0)}
            </div>
            <div class="info-item">
                <strong>❌ Pasos Fallidos</strong>
                {summary.get('failed_steps', 0)}
            </div>
            <div class="info-item">
                <strong>📸 Screenshots Tomados</strong>
                {summary.get('screenshots_taken', 0)}
            </div>
        </div>
    </div>
"""

        # Agregar análisis del log si está disponible
        if log_analysis:
            html_content += f"""
    <div class="section">
        <h2>🔍 Análisis del Log</h2>
        <div class="info-item">
            <strong>📄 Archivo de Log</strong>
            {log_analysis.get('file_path', 'N/A')}
        </div>

        <h3>🚨 Errores Encontrados</h3>
"""

            errors = log_analysis.get("errors", [])
            if errors:
                for i, error in enumerate(errors, 1):
                    html_content += f"""
        <div class="error-item">
            <div class="error-title">Error {i}: {error.get('type', 'Error Desconocido')}</div>
            <strong>🕐 Timestamp:</strong> {error.get('timestamp', 'N/A')}<br>
            <strong>📍 Ubicación:</strong> Línea {error.get('line_number', 'N/A')}<br>
            <strong>📝 Mensaje:</strong> {error.get('message', 'N/A')}
        </div>
"""
            else:
                html_content += (
                    "<p>No se encontraron errores específicos en el log.</p>"
                )

            # Agregar patrones detectados
            patterns = log_analysis.get("patterns", {})
            if patterns:
                html_content += "<h3>🔍 Patrones Detectados</h3><ul>"
                for pattern, count in patterns.items():
                    html_content += (
                        f"<li><strong>{pattern}:</strong> {count} ocurrencias</li>"
                    )
                html_content += "</ul>"

            html_content += "</div>"

        # Agregar análisis de pasos
        failed_steps = [step for step in steps if step.get("status") == "FAILED"]
        successful_steps = [step for step in steps if step.get("status") == "SUCCESS"]

        html_content += """
    <div class="section">
        <h2>👣 Análisis de Pasos</h2>
"""

        if failed_steps:
            html_content += f"<h3>❌ Pasos Fallidos ({len(failed_steps)})</h3>"
            for i, step in enumerate(failed_steps, 1):
                html_content += f"""
        <div class="error-item">
            <div class="error-title">{i}. {step.get('name', 'Paso sin nombre')}</div>
            <strong>📄 Descripción:</strong> {step.get('description', 'Sin descripción')}<br>
            <strong>⏱️ Duración:</strong> {step.get('duration', 'No disponible')}<br>
            <strong>🕐 Timestamp:</strong> {step.get('timestamp', 'No disponible')}
"""

                # Agregar evidencias si existen
                evidence = step.get("evidence", [])
                if evidence:
                    html_content += '<div style="margin-top: 10px;"><strong>📸 Evidencias del Fallo:</strong><br>'
                    for ev in evidence:
                        html_content += f'• {ev.get("name", "Evidencia")} ({ev.get("timestamp", "Sin timestamp")})<br>'
                    html_content += "</div>"

                html_content += "</div>"

        if successful_steps:
            html_content += f"<h3>✅ Pasos Exitosos ({len(successful_steps)})</h3><ul>"
            for i, step in enumerate(successful_steps, 1):
                html_content += f"<li><strong>{i}.</strong> {step.get('name', 'Paso sin nombre')} - {step.get('timestamp', 'N/A')}</li>"
            html_content += "</ul>"

        html_content += "</div>"

        # Agregar recomendaciones
        html_content += f"""
    <div class="section">
        <h2>💡 Recomendaciones para Solución</h2>

        <div class="recommendations">
            <h3>🔧 Acciones Inmediatas</h3>
            <ol>
                <li><strong>📸 Revisar Screenshots:</strong> Examinar las capturas de pantalla del momento del fallo</li>
                <li><strong>📝 Analizar Log:</strong> Revisar el archivo de log completo para más detalles</li>
                <li><strong>🔄 Reproducir:</strong> Intentar reproducir el fallo en un entorno controlado</li>
            </ol>
        </div>

        <div class="recommendations">
            <h3>🛠️ Posibles Causas</h3>
            <ul>
                <li><strong>Errores de Selenium:</strong> Verificar que los elementos estén disponibles</li>
                <li><strong>Timeouts:</strong> Revisar tiempos de espera y condiciones de red</li>
                <li><strong>Elementos no encontrados:</strong> Verificar selectores y estado de la página</li>
                <li><strong>Problemas de red:</strong> Verificar conectividad y velocidad</li>
                <li><strong>Cambios en la UI:</strong> Revisar si la interfaz ha cambiado</li>
                <li><strong>Datos de prueba:</strong> Verificar que los datos de entrada sean válidos</li>
            </ul>
        </div>

        <div class="checklist">
            <h3>📋 Checklist de Verificación</h3>
            <ul>
                <li>□ ¿Los elementos de la página están visibles?</li>
                <li>□ ¿Los selectores siguen siendo válidos?</li>
                <li>□ ¿La aplicación está funcionando correctamente?</li>
                <li>□ ¿Los datos de prueba son correctos?</li>
                <li>□ ¿Hay problemas de red o conectividad?</li>
            </ul>
        </div>
    </div>

    <div class="section">
        <h2>📁 Archivos de Referencia</h2>
        <ul>
            <li><strong>📄 Log Completo:</strong> {exec_info.get('log_file', 'N/A')}</li>
            <li><strong>📸 Screenshots:</strong> {exec_info.get('evidence_directory', 'N/A')}/screenshots/</li>
            <li><strong>📊 Reporte JSON:</strong> {exec_info.get('evidence_directory', 'N/A')}/reports/</li>
        </ul>
    </div>

    <div class="footer">
        <p>Análisis generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Sistema de Automatización de Pruebas - Zucarmex</p>
        <p>Este documento es confidencial y está destinado únicamente para uso interno del cliente.</p>
    </div>
</body>
</html>
"""

        return html_content

    def _create_general_pdf_content(self, execution_data):
        """Crea el contenido PDF para ejecuciones generales"""
        # Similar a success pero con colores neutros
        return self._create_success_pdf_content(execution_data)

    def _analyze_log_file(self, log_file_path):
        """Analiza el archivo de log para extraer información de errores"""
        try:
            if not log_file_path or not os.path.exists(log_file_path):
                return {}

            log_analysis = {
                "file_path": log_file_path,
                "file_size": os.path.getsize(log_file_path),
                "last_modified": datetime.fromtimestamp(
                    os.path.getmtime(log_file_path)
                ).strftime("%Y-%m-%d %H:%M:%S"),
                "errors": [],
                "patterns": {},
            }

            with open(log_file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Patrones de error comunes
            error_patterns = [
                (r"ERROR", "Error General"),
                (r"FAILED", "Paso Fallido"),
                (r"Exception", "Excepción"),
                (r"TimeoutException", "Timeout"),
                (r"NoSuchElementException", "Elemento No Encontrado"),
                (r"WebDriverException", "Error de WebDriver"),
                (r"AssertionError", "Error de Aserción"),
                (r"AttributeError", "Error de Atributo"),
                (r"KeyError", "Error de Clave"),
                (r"ValueError", "Error de Valor"),
            ]

            # Contar patrones
            for pattern, name in error_patterns:
                count = sum(
                    1 for line in lines if re.search(pattern, line, re.IGNORECASE)
                )
                if count > 0:
                    log_analysis["patterns"][name] = count

            # Extraer errores específicos
            for i, line in enumerate(lines):
                line = line.strip()
                if any(
                    re.search(pattern, line, re.IGNORECASE)
                    for pattern, _ in error_patterns
                ):
                    error_info = {
                        "line_number": i + 1,
                        "timestamp": self._extract_timestamp(line),
                        "type": self._classify_error(line),
                        "message": line,
                    }
                    log_analysis["errors"].append(error_info)

            return log_analysis

        except Exception as e:
            self.logger.error(f"Error analizando log: {str(e)}")
            return {}

    def _extract_timestamp(self, line):
        """Extrae timestamp de una línea de log"""
        timestamp_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
        match = re.search(timestamp_pattern, line)
        return match.group(1) if match else "N/A"

    def _classify_error(self, line):
        """Clasifica el tipo de error basado en el contenido"""
        if "NoSuchElementException" in line:
            return "Elemento No Encontrado"
        elif "TimeoutException" in line:
            return "Timeout"
        elif "WebDriverException" in line:
            return "Error de WebDriver"
        elif "AssertionError" in line:
            return "Error de Aserción"
        elif "Exception" in line:
            return "Excepción General"
        elif "ERROR" in line:
            return "Error de Log"
        else:
            return "Error Desconocido"

    def _sanitize_name(self, name):
        """Sanitiza el nombre para usar en nombres de archivos y carpetas"""
        # Remover caracteres especiales y espacios
        sanitized = re.sub(r"[^\w\s-]", "", str(name)).strip()
        # Reemplazar espacios y guiones múltiples con un solo guión
        sanitized = re.sub(r"[-\s]+", "_", sanitized)
        # Limitar longitud
        return sanitized[:50] if len(sanitized) > 50 else sanitized
