"""
Gestor de Evidencias - Sistema de Organización y Limpieza Automática
"""

import os
import json
import shutil
import logging
from datetime import datetime, timedelta
from pathlib import Path
import zipfile

class EvidenceManager:
    """Gestor de evidencias con organización automática y limpieza"""
    
    def __init__(self, config_file="config.json"):
        """Inicializa el gestor de evidencias"""
        self.config = self._load_config(config_file)
        self.logger = logging.getLogger(__name__)
        
        # Configuración por defecto
        self.retention_days = self.config.get('evidence_management', {}).get('retention_days', 30)
        self.archive_after_days = self.config.get('evidence_management', {}).get('archive_after_days', 90)
        self.cleanup_temp_files = self.config.get('evidence_management', {}).get('cleanup_temp_files', True)
        self.generate_daily_summaries = self.config.get('evidence_management', {}).get('generate_daily_summaries', True)
        self.max_screenshots_per_execution = self.config.get('evidence_management', {}).get('max_screenshots_per_execution', 20)
        self.compress_old_evidence = self.config.get('evidence_management', {}).get('compress_old_evidence', True)
        
        self.logger.info(f"EvidenceManager inicializado - Retención: {self.retention_days} días, Archivado: {self.archive_after_days} días")
    
    def _load_config(self, config_file):
        """Carga la configuración desde el archivo JSON"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.warning(f"No se pudo cargar {config_file}, usando configuración por defecto: {str(e)}")
            return {}
    
    def create_evidence_structure(self, feature_name, scenario_name, execution_result="UNKNOWN"):
        """Crea la estructura de evidencias para una ejecución"""
        try:
            # Crear estructura de carpetas
            today = datetime.now().strftime("%Y-%m-%d")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Determinar el tipo de resultado y subcarpeta
            result_info = self._get_result_info(execution_result)
            result_subfolder = result_info["subfolder"]
            result_prefix = result_info["prefix"]
            
            # Crear estructura de carpetas con subcarpetas por resultado
            base_dir = Path("evidences") / today / feature_name / result_subfolder
            execution_dir = base_dir / f"{result_prefix}_{timestamp}"
            screenshots_dir = execution_dir / "screenshots"
            
            # Crear directorios
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            
            self.logger.info(f"Estructura de evidencias creada: {execution_dir}")
            self.logger.info(f"Subcarpeta por resultado: {result_subfolder}")
            return str(execution_dir), str(screenshots_dir)
            
        except Exception as e:
            self.logger.error(f"Error creando estructura de evidencias: {str(e)}")
            # Fallback a estructura simple
            return self._create_simple_structure(feature_name, scenario_name)
    
    def _get_result_info(self, result):
        """Obtiene información completa del resultado incluyendo subcarpeta"""
        result_upper = str(result).upper()
        if "SUCCESS" in result_upper or "PASS" in result_upper:
            return {
                "subfolder": "✅_EXITOSOS",
                "prefix": "SUCCESS",
                "emoji": "✅",
                "status": "EXITOSO"
            }
        elif "FAIL" in result_upper or "ERROR" in result_upper:
            return {
                "subfolder": "❌_FALLIDOS", 
                "prefix": "FAILED",
                "emoji": "❌",
                "status": "FALLIDO"
            }
        elif "PARTIAL" in result_upper or "WARNING" in result_upper:
            return {
                "subfolder": "⚠️_PARCIALES",
                "prefix": "PARTIAL", 
                "emoji": "⚠️",
                "status": "PARCIAL"
            }
        else:
            return {
                "subfolder": "❓_DESCONOCIDOS",
                "prefix": "UNKNOWN",
                "emoji": "❓", 
                "status": "DESCONOCIDO"
            }
    
    def _get_result_prefix(self, result):
        """Obtiene el prefijo basado en el resultado (método legacy)"""
        result_info = self._get_result_info(result)
        return f"{result_info['emoji']}_{result_info['prefix']}"
    
    def _create_simple_structure(self, feature_name, scenario_name):
        """Crea estructura simple como fallback"""
        evidence_dir = os.path.join("evidences", feature_name, scenario_name)
        os.makedirs(evidence_dir, exist_ok=True)
        return evidence_dir, evidence_dir
    
    def save_execution_metadata(self, execution_dir, metadata):
        """Guarda metadatos de la ejecución"""
        try:
            metadata_file = os.path.join(execution_dir, "execution_summary.json")
            
            # Agregar timestamp de creación
            metadata['created_at'] = datetime.now().isoformat()
            metadata['execution_dir'] = execution_dir
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Metadatos guardados: {metadata_file}")
            
        except Exception as e:
            self.logger.error(f"Error guardando metadatos: {str(e)}")
    
    def save_performance_metrics(self, execution_dir, metrics):
        """Guarda métricas de rendimiento"""
        try:
            metrics_file = os.path.join(execution_dir, "performance_metrics.json")
            
            # Agregar timestamp
            metrics['timestamp'] = datetime.now().isoformat()
            
            with open(metrics_file, 'w', encoding='utf-8') as f:
                json.dump(metrics, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Métricas guardadas: {metrics_file}")
            
        except Exception as e:
            self.logger.error(f"Error guardando métricas: {str(e)}")
    
    def save_error_details(self, execution_dir, error_info):
        """Guarda detalles de errores"""
        try:
            error_file = os.path.join(execution_dir, "error_details.json")
            
            # Agregar timestamp
            error_info['timestamp'] = datetime.now().isoformat()
            
            with open(error_file, 'w', encoding='utf-8') as f:
                json.dump(error_info, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Detalles de error guardados: {error_file}")
            
        except Exception as e:
            self.logger.error(f"Error guardando detalles de error: {str(e)}")
    
    def cleanup_old_evidence(self):
        """Limpia evidencias antiguas según la configuración"""
        try:
            self.logger.info("Iniciando limpieza de evidencias antiguas...")
            
            evidences_dir = Path("evidences")
            if not evidences_dir.exists():
                self.logger.info("No existe directorio de evidencias")
                return
            
            cutoff_date = datetime.now() - timedelta(days=self.retention_days)
            archive_date = datetime.now() - timedelta(days=self.archive_after_days)
            
            cleaned_count = 0
            archived_count = 0
            
            # Procesar carpetas por fecha
            for date_dir in evidences_dir.iterdir():
                if not date_dir.is_dir():
                    continue
                
                try:
                    # Parsear fecha del directorio
                    dir_date = datetime.strptime(date_dir.name, "%Y-%m-%d")
                    
                    if dir_date < archive_date:
                        # Archivar evidencias muy antiguas
                        self._archive_evidence(date_dir)
                        archived_count += 1
                        self.logger.info(f"Archivado: {date_dir.name}")
                        
                    elif dir_date < cutoff_date:
                        # Limpiar evidencias antiguas
                        if self.cleanup_temp_files:
                            self._cleanup_evidence_directory(date_dir)
                        cleaned_count += 1
                        self.logger.info(f"Limpiado: {date_dir.name}")
                        
                except ValueError:
                    # No es un directorio de fecha válido, saltar
                    continue
            
            self.logger.info(f"Limpieza completada - Limpiados: {cleaned_count}, Archivados: {archived_count}")
            
        except Exception as e:
            self.logger.error(f"Error en limpieza de evidencias: {str(e)}")
    
    def _archive_evidence(self, evidence_dir):
        """Archiva evidencias antiguas"""
        try:
            archive_dir = Path("evidences") / "archive" / evidence_dir.name
            archive_dir.mkdir(parents=True, exist_ok=True)
            
            if self.compress_old_evidence:
                # Comprimir en ZIP
                zip_file = archive_dir / f"{evidence_dir.name}.zip"
                with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(evidence_dir):
                        for file in files:
                            file_path = Path(root) / file
                            arcname = file_path.relative_to(evidence_dir.parent)
                            zipf.write(file_path, arcname)
                
                # Eliminar directorio original
                shutil.rmtree(evidence_dir)
                self.logger.info(f"Evidencias archivadas y comprimidas: {zip_file}")
            else:
                # Mover sin comprimir
                shutil.move(str(evidence_dir), str(archive_dir))
                self.logger.info(f"Evidencias archivadas: {archive_dir}")
                
        except Exception as e:
            self.logger.error(f"Error archivando evidencias {evidence_dir}: {str(e)}")
    
    def _cleanup_evidence_directory(self, evidence_dir):
        """Limpia un directorio de evidencias"""
        try:
            # Limpiar archivos temporales
            for root, dirs, files in os.walk(evidence_dir):
                for file in files:
                    if file.endswith('.tmp') or file.startswith('temp_'):
                        os.remove(os.path.join(root, file))
            
            # Limitar número de screenshots por ejecución
            for feature_dir in evidence_dir.iterdir():
                if feature_dir.is_dir():
                    for execution_dir in feature_dir.iterdir():
                        if execution_dir.is_dir():
                            screenshots_dir = execution_dir / "screenshots"
                            if screenshots_dir.exists():
                                self._limit_screenshots(screenshots_dir)
            
        except Exception as e:
            self.logger.error(f"Error limpiando directorio {evidence_dir}: {str(e)}")
    
    def _limit_screenshots(self, screenshots_dir):
        """Limita el número de screenshots por ejecución"""
        try:
            screenshots = list(screenshots_dir.glob("*.png"))
            if len(screenshots) > self.max_screenshots_per_execution:
                # Ordenar por fecha de modificación
                screenshots.sort(key=lambda x: x.stat().st_mtime)
                
                # Eliminar los más antiguos
                to_remove = screenshots[:-self.max_screenshots_per_execution]
                for screenshot in to_remove:
                    screenshot.unlink()
                
                self.logger.info(f"Eliminados {len(to_remove)} screenshots antiguos de {screenshots_dir}")
                
        except Exception as e:
            self.logger.error(f"Error limitando screenshots en {screenshots_dir}: {str(e)}")
    
    def generate_daily_summary(self, date=None):
        """Genera resumen diario de evidencias"""
        try:
            if date is None:
                date = datetime.now().strftime("%Y-%m-%d")
            
            date_dir = Path("evidences") / date
            if not date_dir.exists():
                self.logger.info(f"No hay evidencias para {date}")
                return
            
            summary = {
                "date": date,
                "generated_at": datetime.now().isoformat(),
                "features": {},
                "total_executions": 0,
                "successful_executions": 0,
                "failed_executions": 0,
                "partial_executions": 0
            }
            
            # Procesar cada feature
            for feature_dir in date_dir.iterdir():
                if not feature_dir.is_dir():
                    continue
                
                feature_name = feature_dir.name
                feature_summary = {
                    "executions": 0,
                    "successful": 0,
                    "failed": 0,
                    "partial": 0,
                    "execution_details": []
                }
                
                # Procesar cada ejecución
                for execution_dir in feature_dir.iterdir():
                    if not execution_dir.is_dir():
                        continue
                    
                    execution_name = execution_dir.name
                    feature_summary["executions"] += 1
                    summary["total_executions"] += 1
                    
                    # Determinar resultado
                    if "SUCCESS" in execution_name:
                        feature_summary["successful"] += 1
                        summary["successful_executions"] += 1
                    elif "FAILED" in execution_name:
                        feature_summary["failed"] += 1
                        summary["failed_executions"] += 1
                    elif "PARTIAL" in execution_name:
                        feature_summary["partial"] += 1
                        summary["partial_executions"] += 1
                    
                    # Agregar detalles de la ejecución
                    feature_summary["execution_details"].append({
                        "name": execution_name,
                        "timestamp": execution_name.split("_")[-1] if "_" in execution_name else "unknown",
                        "screenshots_count": len(list((execution_dir / "screenshots").glob("*.png")) if (execution_dir / "screenshots").exists() else [])
                    })
                
                summary["features"][feature_name] = feature_summary
            
            # Guardar resumen
            summary_file = date_dir / "daily_summary.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Resumen diario generado: {summary_file}")
            return summary
            
        except Exception as e:
            self.logger.error(f"Error generando resumen diario: {str(e)}")
            return None
    
    def get_evidence_statistics(self):
        """Obtiene estadísticas de evidencias"""
        try:
            evidences_dir = Path("evidences")
            if not evidences_dir.exists():
                return {"error": "No existe directorio de evidencias"}
            
            stats = {
                "total_days": 0,
                "total_features": 0,
                "total_executions": 0,
                "successful_executions": 0,
                "failed_executions": 0,
                "partial_executions": 0,
                "total_size_mb": 0,
                "oldest_evidence": None,
                "newest_evidence": None
            }
            
            dates = []
            
            # Procesar cada fecha
            for date_dir in evidences_dir.iterdir():
                if not date_dir.is_dir() or date_dir.name == "archive":
                    continue
                
                try:
                    dir_date = datetime.strptime(date_dir.name, "%Y-%m-%d")
                    dates.append(dir_date)
                    stats["total_days"] += 1
                    
                    # Procesar features
                    for feature_dir in date_dir.iterdir():
                        if not feature_dir.is_dir():
                            continue
                        
                        stats["total_features"] += 1
                        
                        # Procesar ejecuciones
                        for execution_dir in feature_dir.iterdir():
                            if not execution_dir.is_dir():
                                continue
                            
                            stats["total_executions"] += 1
                            
                            # Contar por tipo
                            if "SUCCESS" in execution_dir.name:
                                stats["successful_executions"] += 1
                            elif "FAILED" in execution_dir.name:
                                stats["failed_executions"] += 1
                            elif "PARTIAL" in execution_dir.name:
                                stats["partial_executions"] += 1
                            
                            # Calcular tamaño
                            for root, dirs, files in os.walk(execution_dir):
                                for file in files:
                                    file_path = Path(root) / file
                                    stats["total_size_mb"] += file_path.stat().st_size / (1024 * 1024)
                
                except ValueError:
                    continue
            
            # Fechas
            if dates:
                stats["oldest_evidence"] = min(dates).strftime("%Y-%m-%d")
                stats["newest_evidence"] = max(dates).strftime("%Y-%m-%d")
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error obteniendo estadísticas: {str(e)}")
            return {"error": str(e)}
