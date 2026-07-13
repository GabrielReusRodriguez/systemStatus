"""
Handler para obtener informacion y rendimiento de la RAM.
Implementa RF-003 y RF-004.
"""
import psutil
import subprocess
import os


class RamHandler:
    """Clase para manejar la obtencion de datos de la RAM."""

    def __init__(self):
        """Inicializa el handler de RAM."""
        pass

    def get_ram_info(self):
        """
        Obtiene la informacion basica de la RAM.

        Returns:
            dict: Diccionario con tipo y velocidad de la RAM
        """
        info = {}
        info['type'] = self._get_ram_type()
        info['speed'] = self._get_ram_speed()

        if info['type'] == 'Unknown':
            info['type'] = 'Desconocido'

        return info

    def _get_ram_type(self):
        """
        Obtiene el tipo de RAM (DDR3, DDR4, DDR5, etc.).

        Returns:
            str: Tipo de RAM
        """
        try:
            # Metodo 1: dmidecode
            try:
                result = subprocess.run(
                    ['dmidecode', '-t', 'memory'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    output = result.stdout.lower()
                    for ram_type in ['DDR5', 'DDR4', 'DDR3', 'DDR2']:
                        if ram_type.lower() in output:
                            return ram_type
                    if 'ddr' in output:
                        return 'DDR'
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

            # Metodo 2: lshw
            try:
                result = subprocess.run(
                    ['lshw', '-class', 'memory'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    output = result.stdout.lower()
                    for ram_type in ['DDR5', 'DDR4', 'DDR3', 'DDR2']:
                        if ram_type.lower() in output:
                            return ram_type
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

            return 'DDR4'

        except Exception:
            return 'Unknown'

    def _get_ram_speed(self):
        """
        Obtiene la velocidad de la RAM en MHz.

        Returns:
            float: Velocidad en MHz
        """
        try:
            try:
                result = subprocess.run(
                    ['dmidecode', '-t', 'memory'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if 'speed:' in line.lower():
                            parts = line.split()
                            for part in parts:
                                try:
                                    if 'mhz' in part.lower():
                                        return float(
                                            part.replace('mhz', '').strip()
                                        )
                                    return float(part)
                                except ValueError:
                                    continue
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
            return 0.0

        except Exception:
            return 0.0

    def get_ram_usage(self):
        """
        Obtiene el uso de RAM.

        Returns:
            dict: Diccionario con total, libre y porcentaje
        """
        mem = psutil.virtual_memory()

        return {
            'total': mem.total,
            'free': mem.free,
            'percent_free': (mem.free / mem.total) * 100
        }

    def format_ram_info(self):
        """
        Formatea la informacion de la RAM para mostrar.

        Returns:
            str: Cadena formateada con la informacion de la RAM
        """
        info = self.get_ram_info()
        speed = int(info['speed']) if info['speed'] > 0 else 0
        return (
            f"Tipo: {info['type']}\n"
            f"Velocidad: {speed} MHz"
        )

    def format_ram_usage(self):
        """
        Formatea el uso de la RAM con barra de progreso.

        Returns:
            str: Cadena formateada con el uso de RAM
        """
        usage = self.get_ram_usage()
        total = usage['total']
        free = usage['free']
        percent_free = usage['percent_free']

        total_str = self._format_size(total)
        free_str = self._format_size(free)
        free_bar = self._create_progress_bar(percent_free)

        return (
            f"RAM Total: {total_str}\n"
            f"RAM Libre: {free_str}\n"
            f"% Libre: {percent_free:06.2f}%\n"
            f"Libre:     |{free_bar}"
        )

    @staticmethod
    def _format_size(size_bytes):
        """
        Formatea un tamano en bytes a formato legible (RNF-008).

        Args:
            size_bytes: Tamano en bytes

        Returns:
            str: Tamano formateado (TB, GB, MB, KB, B)
        """
        size = float(size_bytes)
        if size >= 1024 ** 4:
            return f"{size / (1024 ** 4):.2f} TB"
        if size >= 1024 ** 3:
            return f"{size / (1024 ** 3):.2f} GB"
        if size >= 1024 ** 2:
            return f"{size / (1024 ** 2):.2f} MB"
        if size >= 1024:
            return f"{size / 1024:.2f} KB"
        return f"{int(size)} B"

    @staticmethod
    def _create_progress_bar(percentage, width=20):
        """
        Crea una barra de progreso usando caracteres █.

        Args:
            percentage: Porcentaje (0-100)
            width: Ancho de la barra en caracteres

        Returns:
            str: Barra de progreso con caracteres █
        """
        filled = int(round(percentage * width / 100))
        return "█" * filled
