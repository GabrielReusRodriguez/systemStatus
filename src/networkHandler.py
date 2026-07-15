"""Manejador de información y uso de la red.

Stub pendiente de implementación cuando se apruebe RF-005.
"""

import psutil


def get_network_usage():
    """Obtiene el uso actual de la red (stub).

    Retorna diccionario con datos de ejemplo.
    """
    counters = psutil.net_io_counters()
    return {
        'bytes_sent': counters.bytes_sent,
        'bytes_recv': counters.bytes_recv,
    }
