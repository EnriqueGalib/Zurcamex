"""
Gestor de Limpieza - Eliminación de Evidencias y Logs Antiguos
"""

import os
import shutil
import logging
from datetime import datetime, timedelta
from pathlib import Path
import json

class CleanupManager:
    """Gestor de limpieza de evidencias y logs antiguos que no están en la nueva estructura"""
    
    def __init__(self, config=None):
        self.logger = logging.getLogger(__name__)
        self.config = config or {}
        
        # Configuración por defecto
        self.cleanup_old_evidence = self.config.get('cleanup_old_evidence', True)
        self.cleanup_old_logs = self.config.get('cleanup_old_logs', True)
        self.cleanup_old_reports = self.config.get('cleanup_old_reports', True)
        self.cleanup_old_docs = self.config.get('cleanup_old_docs', True)
        
        # Días de retención
        self.evidence_retention_days = self.config.get('evidence_retention_days', 30)
        self.logs_retention_days = self.config.get('logs_retention_days', 30)
        self.reports_retention_days = self.config.get('reports_retention_days', 30)
        self.docs_retention_days = self.config.get('docs_retention_days', 30)
    
    def cleanup_old_files(self):
        """Limpia archivos antiguos que no están en la nueva estructura"""
        try:
            self.logger.info("Iniciando limpieza de archivos antiguos...")
            
            cleanup_summary = {
                'evidences_cleaned': 0,
                'logs_cleaned': 0,
                'reports_cleaned': 0,
                'docs_cleaned': 0,
                'total_size_freed': 0,
                'errors': []
            }
            
            # Limpiar evidencias antiguas
            if self.cleanup_old_evidence:
                evidences_cleaned, size_freed = self._cleanup_old_evidences()
                cleanup_summary['evidences_cleaned'] = evidences_cleaned
                cleanup_summary['total_size_freed'] += size_freed
            
            # Limpiar logs antiguos
            if self.cleanup_old_logs:
                logs_cleaned, size_freed = self._cleanup_old_logs()
                cleanup_summary['logs_cleaned'] = logs_cleaned
                cleanup_summary['total_size_freed'] += size_freed
            
            # Limpiar reportes antiguos
            if self.cleanup_old_reports:
                reports_cleaned, size_freed = self._cleanup_old_reports()
                cleanup_summary['reports_cleaned'] = reports_cleaned
                cleanup_summary['total_size_freed'] += size_freed
            
            # Limpiar documentación antigua
            if self.cleanup_old_docs:
                docs_cleaned, size_freed = self._cleanup_old_docs()
                cleanup_summary['docs_cleaned'] = docs_cleaned
                cleanup_summary['total_size_freed'] += size_freed
            
            # Generar reporte de limpieza
            self._generate_cleanup_report(cleanup_summary)
            
            self.logger.info(f"Limpieza completada: {cleanup_summary}")
            return cleanup_summary
            
        except Exception as e:
            self.logger.error(f"Error en limpieza de archivos antiguos: {str(e)}")
            return None
    
    def _cleanup_old_evidences(self):
        """Limpia evidencias antiguas que no están en la nueva estructura"""
        try:
            evidences_dir = Path("evidences")
            if not evidences_dir.exists():
                return 0, 0
            
            cleaned_count = 0
            total_size_freed = 0
            
            # Limpiar estructura antigua (sin fecha)
            for feature_dir in evidences_dir.iterdir():
                if not feature_dir.is_dir():
                    continue
                
                # Si no es una carpeta de fecha (YYYY-MM-DD), es estructura antigua
                if not self._is_date_folder(feature_dir.name):
                    self.logger.info(f"Eliminando estructura antigua de evidencias: {feature_dir}")
                    
                    # Calcular tamaño antes de eliminar
                    size = self._get_directory_size(feature_dir)
                    total_size_freed += size
                    
                    # Eliminar directorio
                    shutil.rmtree(feature_dir)
                    cleaned_count += 1
            
            # Limpiar evidencias por fecha (más antiguas que retention_days)
            cutoff_date = datetime.now() - timedelta(days=self.evidence_retention_days)
            
            for date_dir in evidences_dir.iterdir():
                if not date_dir.is_dir() or not self._is_date_folder(date_dir.name):
                    continue
                
                try:
                    folder_date = datetime.strptime(date_dir.name, "%Y-%m-%d")
                    if folder_date < cutoff_date:
                        self.logger.info(f"Eliminando evidencias antiguas: {date_dir}")
                        
                        # Calcular tamaño antes de eliminar
                        size = self._get_directory_size(date_dir)
                        total_size_freed += size
                        
                        # Eliminar directorio
                        shutil.rmtree(date_dir)
                        cleaned_count += 1
                        
                except ValueError:
                    # Si no se puede parsear la fecha, mantener el directorio
                    continue
            
            self.logger.info(f"Evidencias limpiadas: {cleaned_count} directorios, {total_size_freed} bytes liberados")
            return cleaned_count, total_size_freed
            
        except Exception as e:
            self.logger.error(f"Error limpiando evidencias antiguas: {str(e)}")
            return 0, 0
    
    def _cleanup_old_logs(self):
        """Limpia logs antiguos que no están en la nueva estructura"""
        try:
            logs_dir = Path("logs")
            if not logs_dir.exists():
                return 0, 0
            
            cleaned_count = 0
            total_size_freed = 0
            
            # Limpiar estructura antigua (sin fecha)
            for feature_dir in logs_dir.iterdir():
                if not feature_dir.is_dir():
                    continue
                
                # Si no es una carpeta de fecha (YYYY-MM-DD), es estructura antigua
                if not self._is_date_folder(feature_dir.name):
                    self.logger.info(f"Eliminando estructura antigua de logs: {feature_dir}")
                    
                    # Calcular tamaño antes de eliminar
                    size = self._get_directory_size(feature_dir)
                    total_size_freed += size
                    
                    # Eliminar directorio
                    shutil.rmtree(feature_dir)
                    cleaned_count += 1
            
            # Limpiar logs por fecha (más antiguos que retention_days)
            cutoff_date = datetime.now() - timedelta(days=self.logs_retention_days)
            
            for date_dir in logs_dir.iterdir():
                if not date_dir.is_dir() or not self._is_date_folder(date_dir.name):
                    continue
                
                try:
                    folder_date = datetime.strptime(date_dir.name, "%Y-%m-%d")
                    if folder_date < cutoff_date:
                        self.logger.info(f"Eliminando logs antiguos: {date_dir}")
                        
                        # Calcular tamaño antes de eliminar
                        size = self._get_directory_size(date_dir)
                        total_size_freed += size
                        
                        # Eliminar directorio
                        shutil.rmtree(date_dir)
                        cleaned_count += 1
                        
                except ValueError:
                    # Si no se puede parsear la fecha, mantener el directorio
                    continue
            
            self.logger.info(f"Logs limpiados: {cleaned_count} directorios, {total_size_freed} bytes liberados")
            return cleaned_count, total_size_freed
            
        except Exception as e:
            self.logger.error(f"Error limpiando logs antiguos: {str(e)}")
            return 0, 0
    
    def _cleanup_old_reports(self):
        """Limpia reportes antiguos que no están en la nueva estructura"""
        try:
            reports_dir = Path("reports")
            if not reports_dir.exists():
                return 0, 0
            
            cleaned_count = 0
            total_size_freed = 0
            
            # Limpiar reportes antiguos (archivos sueltos sin carpeta de feature)
            for item in reports_dir.iterdir():
                if item.is_file():
                    # Si es un archivo suelto, es estructura antigua
                    self.logger.info(f"Eliminando reporte antiguo: {item}")
                    
                    # Calcular tamaño antes de eliminar
                    size = item.stat().st_size
                    total_size_freed += size
                    
                    # Eliminar archivo
                    item.unlink()
                    cleaned_count += 1
            
            # Limpiar carpetas de reportes por fecha (más antiguas que retention_days)
            cutoff_date = datetime.now() - timedelta(days=self.reports_retention_days)
            
            for feature_dir in reports_dir.iterdir():
                if not feature_dir.is_dir():
                    continue
                
                # Extraer fecha del nombre de la carpeta (formato: YYYY-MM-DD_feature_name)
                folder_name = feature_dir.name
                if '_' in folder_name:
                    date_part = folder_name.split('_')[0]
                    try:
                        folder_date = datetime.strptime(date_part, "%Y-%m-%d")
                        if folder_date < cutoff_date:
                            self.logger.info(f"Eliminando reportes antiguos: {feature_dir}")
                            
                            # Calcular tamaño antes de eliminar
                            size = self._get_directory_size(feature_dir)
                            total_size_freed += size
                            
                            # Eliminar directorio
                            shutil.rmtree(feature_dir)
                            cleaned_count += 1
                            
                    except ValueError:
                        # Si no se puede parsear la fecha, mantener el directorio
                        continue
            
            self.logger.info(f"Reportes limpiados: {cleaned_count} elementos, {total_size_freed} bytes liberados")
            return cleaned_count, total_size_freed
            
        except Exception as e:
            self.logger.error(f"Error limpiando reportes antiguos: {str(e)}")
            return 0, 0
    
    def _cleanup_old_docs(self):
        """Limpia documentación antigua que no está en la nueva estructura"""
        try:
            docs_dir = Path("docs")
            if not docs_dir.exists():
                return 0, 0
            
            cleaned_count = 0
            total_size_freed = 0
            
            # Limpiar archivos de documentación antiguos (que no estén en las carpetas organizadas)
            organized_folders = ['✅_EXITOSOS', '❌_FALLIDOS', '⚠️_PARCIALES', '❓_DESCONOCIDOS']
            
            for item in docs_dir.iterdir():
                if item.is_file() and item.suffix == '.md':
                    # Si es un archivo .md suelto, es estructura antigua
                    self.logger.info(f"Eliminando documentación antigua: {item}")
                    
                    # Calcular tamaño antes de eliminar
                    size = item.stat().st_size
                    total_size_freed += size
                    
                    # Eliminar archivo
                    item.unlink()
                    cleaned_count += 1
                elif item.is_dir() and item.name not in organized_folders:
                    # Si es una carpeta que no está en la estructura organizada, es antigua
                    self.logger.info(f"Eliminando carpeta de documentación antigua: {item}")
                    
                    # Calcular tamaño antes de eliminar
                    size = self._get_directory_size(item)
                    total_size_freed += size
                    
                    # Eliminar directorio
                    shutil.rmtree(item)
                    cleaned_count += 1
            
            self.logger.info(f"Documentación limpiada: {cleaned_count} elementos, {total_size_freed} bytes liberados")
            return cleaned_count, total_size_freed
            
        except Exception as e:
            self.logger.error(f"Error limpiando documentación antigua: {str(e)}")
            return 0, 0
    
    def _is_date_folder(self, folder_name):
        """Verifica si el nombre de la carpeta es una fecha en formato YYYY-MM-DD"""
        try:
            datetime.strptime(folder_name, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def _get_directory_size(self, directory):
        """Calcula el tamaño total de un directorio"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except (OSError, FileNotFoundError):
                        continue
        except Exception as e:
            self.logger.warning(f"Error calculando tamaño de {directory}: {str(e)}")
        
        return total_size
    
    def _generate_cleanup_report(self, cleanup_summary):
        """Genera un reporte de la limpieza realizada"""
        try:
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            cleanup_report_path = reports_dir / f"cleanup_report_{timestamp}.json"
            
            cleanup_summary['cleanup_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cleanup_summary['total_size_freed_mb'] = round(cleanup_summary['total_size_freed'] / (1024 * 1024), 2)
            
            with open(cleanup_report_path, 'w', encoding='utf-8') as f:
                json.dump(cleanup_summary, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Reporte de limpieza generado: {cleanup_report_path}")
            
        except Exception as e:
            self.logger.error(f"Error generando reporte de limpieza: {str(e)}")
    
    def get_cleanup_stats(self):
        """Obtiene estadísticas de limpieza sin ejecutar la limpieza"""
        try:
            stats = {
                'evidences': self._get_old_evidences_count(),
                'logs': self._get_old_logs_count(),
                'reports': self._get_old_reports_count(),
                'docs': self._get_old_docs_count()
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error obteniendo estadísticas de limpieza: {str(e)}")
            return None
    
    def _get_old_evidences_count(self):
        """Cuenta evidencias antiguas sin eliminarlas"""
        try:
            evidences_dir = Path("evidences")
            if not evidences_dir.exists():
                return 0
            
            count = 0
            cutoff_date = datetime.now() - timedelta(days=self.evidence_retention_days)
            
            for item in evidences_dir.iterdir():
                if not item.is_dir():
                    continue
                
                if not self._is_date_folder(item.name):
                    count += 1
                else:
                    try:
                        folder_date = datetime.strptime(item.name, "%Y-%m-%d")
                        if folder_date < cutoff_date:
                            count += 1
                    except ValueError:
                        continue
            
            return count
            
        except Exception as e:
            self.logger.error(f"Error contando evidencias antiguas: {str(e)}")
            return 0
    
    def _get_old_logs_count(self):
        """Cuenta logs antiguos sin eliminarlos"""
        try:
            logs_dir = Path("logs")
            if not logs_dir.exists():
                return 0
            
            count = 0
            cutoff_date = datetime.now() - timedelta(days=self.logs_retention_days)
            
            for item in logs_dir.iterdir():
                if not item.is_dir():
                    continue
                
                if not self._is_date_folder(item.name):
                    count += 1
                else:
                    try:
                        folder_date = datetime.strptime(item.name, "%Y-%m-%d")
                        if folder_date < cutoff_date:
                            count += 1
                    except ValueError:
                        continue
            
            return count
            
        except Exception as e:
            self.logger.error(f"Error contando logs antiguos: {str(e)}")
            return 0
    
    def _get_old_reports_count(self):
        """Cuenta reportes antiguos sin eliminarlos"""
        try:
            reports_dir = Path("reports")
            if not reports_dir.exists():
                return 0
            
            count = 0
            cutoff_date = datetime.now() - timedelta(days=self.reports_retention_days)
            
            for item in reports_dir.iterdir():
                if item.is_file():
                    count += 1
                elif item.is_dir():
                    folder_name = item.name
                    if '_' in folder_name:
                        date_part = folder_name.split('_')[0]
                        try:
                            folder_date = datetime.strptime(date_part, "%Y-%m-%d")
                            if folder_date < cutoff_date:
                                count += 1
                        except ValueError:
                            continue
            
            return count
            
        except Exception as e:
            self.logger.error(f"Error contando reportes antiguos: {str(e)}")
            return 0
    
    def _get_old_docs_count(self):
        """Cuenta documentación antigua sin eliminarla"""
        try:
            docs_dir = Path("docs")
            if not docs_dir.exists():
                return 0
            
            count = 0
            organized_folders = ['✅_EXITOSOS', '❌_FALLIDOS', '⚠️_PARCIALES', '❓_DESCONOCIDOS']
            
            for item in docs_dir.iterdir():
                if item.is_file() and item.suffix == '.md':
                    count += 1
                elif item.is_dir() and item.name not in organized_folders:
                    count += 1
            
            return count
            
        except Exception as e:
            self.logger.error(f"Error contando documentación antigua: {str(e)}")
            return 0
