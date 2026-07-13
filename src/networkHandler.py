"""
Handler para obtener informacion de la red.
Implementa RF-005.
"""
import psutil


class NetworkHandler:
    """Clase para manejar la obtencion de datos de red."""

    def __init__(self):
        """Inicializa el handler de red."""
        pass

    def get_network_usage(self):
        """
        Obtiene el uso de red (bytes enviados y recibidos).

        Returns:
            dict: Diccionario con bytes enviados y recibidos
        """
        net_io = psutil.net_io_counters()

        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv
        }

    def format_network_usage(self):
        """
        Formatea el uso de red para mostrar (RNF-005, RNF-008).

        Returns:
            str: Cadena formateada con el uso de red
        """
        usage = self.get_network_usage()

        sent_str = self._format_size(usage['bytes_sent'])
        recv_str = self._format_size(usage['bytes_recv'])

        return (
            f"Subidos: {sent_str}\n"
            f"Bajados: {recv_str}"
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
