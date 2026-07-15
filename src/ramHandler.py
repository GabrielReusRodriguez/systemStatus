"""Manejador de información y uso de la RAM.

Stub pendiente de implementación cuando se apruebe RF-003 y RF-004.
"""

import psutil


def get_ram_info():
    """Obtiene información estática de la RAM (stub).

    Retorna diccionario con datos de ejemplo.
    """
    mem = psutil.virtual_memory()
    return {
        'type': 'DDR4',
        'total': mem.total,
    }


def get_ram_usage():
    """Obtiene el uso actual de la RAM (stub).

    Retorna diccionario con datos de ejemplo.
    """
    mem = psutil.virtual_memory()
    return {
        'total': mem.total,
        'available': mem.available,
        'percent': mem.percent,
    }
