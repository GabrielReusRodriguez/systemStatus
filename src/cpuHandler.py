"""
Handler para obtener informacion y rendimiento de la CPU.
Implementa RF-001 y RF-002.
"""
import psutil


class CpuHandler:
    """Clase para manejar la obtencion de datos de la CPU."""

    def __init__(self):
        """Inicializa el handler de CPU."""
        self._cpu_info = None
        self._physical_cores = None

    def get_cpu_info(self):
        """
        Obtiene la informacion basica de la CPU.

        Returns:
            dict: Diccionario con modelo, familia y frecuencia de la CPU
        """
        if self._cpu_info is None:
            self._cpu_info = {}
            cpu_info = self._read_cpuinfo()
            self._cpu_info['model'] = cpu_info.get('model name', 'Unknown')
            self._cpu_info['family'] = cpu_info.get('cpu family', 'Unknown')

            cpu_freq = psutil.cpu_freq()
            if cpu_freq and cpu_freq.max > 0:
                self._cpu_info['frequency'] = cpu_freq.max
            else:
                try:
                    freq = float(cpu_info.get('cpu MHz', '0').strip())
                    self._cpu_info['frequency'] = freq if freq > 0 else 0.0
                except (ValueError, TypeError):
                    self._cpu_info['frequency'] = 0.0

        return self._cpu_info

    def get_physical_cores_count(self):
        """
        Obtiene el numero de cores fisicos.

        Returns:
            int: Numero de cores fisicos
        """
        if self._physical_cores is None:
            self._physical_cores = psutil.cpu_count(logical=False)
        return self._physical_cores

    @staticmethod
    def _read_cpuinfo():
        """
        Lee la informacion de /proc/cpuinfo.

        Returns:
            dict: Diccionario con la informacion del primer procesador
        """
        try:
            with open('/proc/cpuinfo', 'r', encoding='utf-8') as f:
                info = {}
                for line in f:
                    if line.strip() == '':
                        break
                    if ':' in line:
                        key, value = line.split(':', 1)
                        info[key.strip()] = value.strip()
                return info
        except (FileNotFoundError, IOError, PermissionError):
            return {}

    def get_physical_cores_usage(self, interval=0.1):
        """
        Obtiene el uso de CPU por core fisico.

        Args:
            interval: Tiempo de espera entre mediciones

        Returns:
            dict: Diccionario con uso total y por core fisico
        """
        all_core_percentages = psutil.cpu_percent(
            interval=interval, percpu=True
        )
        total_percentage = psutil.cpu_percent(interval=interval)

        physical_count = self.get_physical_cores_count()
        logical_count = psutil.cpu_count(logical=True)

        if physical_count > 0 and logical_count > 0:
            cores_per_physical = logical_count // physical_count
            physical_usage = []

            for i in range(physical_count):
                start_idx = i * cores_per_physical
                end_idx = start_idx + cores_per_physical
                physical_core_usage = sum(
                    all_core_percentages[start_idx:end_idx]
                ) / cores_per_physical
                physical_usage.append(physical_core_usage)
        else:
            physical_usage = []

        return {
            'total': total_percentage,
            'physical_cores': physical_usage
        }

    def format_cpu_info(self):
        """
        Formatea la informacion de la CPU para mostrar.

        Returns:
            str: Cadena formateada con la informacion de la CPU
        """
        info = self.get_cpu_info()
        return (
            f"Modelo: {info['model']}\n"
            f"Familia: {info['family']}\n"
            f"Frecuencia: {info['frequency']:.2f} MHz"
        )

    def format_cpu_usage(self):
        """
        Formatea el uso de la CPU con barras de progreso usando █.

        Returns:
            str: Cadena formateada con el uso de CPU
        """
        usage = self.get_physical_cores_usage()
        total = usage['total']
        physical_cores = usage['physical_cores']

        lines = []
        total_bar = self._create_progress_bar(total)
        lines.append(f"Total CPU:   {total:06.2f}%  |{total_bar}")

        for i, core_usage in enumerate(physical_cores, 1):
            core_bar = self._create_progress_bar(core_usage)
            lines.append(f"Core {i:02d}:     {core_usage:06.2f}%  |{core_bar}")

        return "\n".join(lines)

    @staticmethod
    def _create_progress_bar(percentage, width=20):
        """
        Crea una barra de progreso usando caracteres █.

        Args:
            percentage: Porcentaje de uso (0-100)
            width: Ancho de la barra en caracteres

        Returns:
            str: Barra de progreso con caracteres █
        """
        filled = int(round(percentage * width / 100))
        return "█" * filled
