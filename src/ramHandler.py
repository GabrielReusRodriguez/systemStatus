"""Manejador de información y uso de la RAM.

Obtiene información estática (tipo, velocidad, capacidad) y uso actual
de la memoria RAM del sistema.
"""

import re
import subprocess
import psutil

# pylint: disable=wrong-import-position,import-error
from cpuHandler import format_bytes

# Expresiones regulares para parsear salida de dmidecode
_RE_DMIDECODE_TYPE = re.compile(r'^\s*Type:\s+(.+)$', re.MULTILINE)
_RE_DMIDECODE_SPEED = re.compile(r'^\s*Speed:\s+(\d+)\s+MHz', re.MULTILINE)

# Tipos de memoria conocidos para detección en sysfs
_TIPOS_RAM = [
    'DDR5', 'DDR4', 'DDR3', 'DDR2', 'DDR',
    'LPDDR5', 'LPDDR4', 'LPDDR3', 'LPDDR2', 'LPDDR',
    'HBM3', 'HBM2', 'HBM',
]


def _get_ram_from_dmidecode():
    """Intenta obtener tipo y velocidad de RAM usando dmidecode.

    Retorna dict con 'type' y 'speed' (MHz) o None si falla.
    """
    try:
        resultado = subprocess.run(
            ['dmidecode', '-t', 'memory'],
            capture_output=True, text=True, timeout=5, check=False
        )
        if resultado.returncode != 0:
            return None

        texto = resultado.stdout

        tipo_match = _RE_DMIDECODE_TYPE.search(texto)
        velocidad_match = _RE_DMIDECODE_SPEED.search(texto)

        tipo = tipo_match.group(1).strip() if tipo_match else None
        velocidad = int(velocidad_match.group(1)) if velocidad_match else None

        # dmidecode puede retornar "Unknown" o "Not Specified"
        if tipo and tipo.lower() not in ('unknown', 'not specified', 'other'):
            return {'type': tipo, 'speed': velocidad}

    except (FileNotFoundError, subprocess.TimeoutExpired, PermissionError):
        return None

    return None


def _get_ram_from_sysfs():
    """Intenta obtener tipo y velocidad de RAM desde entradas DMI de sysfs.

    Lee el archivo binario DMI tipo 17 (Memory Device) y extrae
    el tipo de memoria y la velocidad buscando strings conocidos.

    Retorna dict con 'type' y 'speed' (MHz) o None si falla.
    """
    ruta_dmi = '/sys/firmware/dmi/entries/17-0/raw'

    try:
        with open(ruta_dmi, 'rb') as archivo:
            datos = archivo.read()
    except (FileNotFoundError, PermissionError, OSError):
        return None

    if len(datos) < 20:
        return None

    # Decodificar como latin-1 para preservar todos los bytes
    texto = datos.decode('latin-1')

    # Buscar tipo de memoria entre los strings conocidos
    tipo = None
    for tipo_candidato in _TIPOS_RAM:
        if tipo_candidato in texto:
            tipo = tipo_candidato
            break

    if tipo is None:
        return None

    # La velocidad está en el offset 0x17-0x18 (2 bytes little-endian)
    # Estructura DMI type 17: offset 0x17-0x18 = Speed (MHz)
    velocidad = None
    if len(datos) >= 22:
        velocidad_raw = int.from_bytes(datos[0x17:0x19], byteorder='little')
        if 0 < velocidad_raw < 100000:
            velocidad = velocidad_raw

    return {'type': tipo, 'speed': velocidad}


def get_ram_info():
    """Obtiene información estática de la RAM.

    Intenta detectar tipo y velocidad usando dmidecode (primero)
    y sysfs como fallback. Si ambos fallan, muestra "No disponible".

    Retorna diccionario con: type, speed (MHz o None), total (bytes).
    """
    mem = psutil.virtual_memory()

    # Intentar dmidecode primero, luego sysfs
    info = _get_ram_from_dmidecode()
    if info is None:
        info = _get_ram_from_sysfs()

    if info is None:
        info = {'type': 'No disponible', 'speed': None}

    info['total'] = mem.total
    return info


def format_ram_info_lineas(info):
    """Formatea la información estática de la RAM en líneas para mostrar.

    Retorna lista de strings con las líneas formateadas.
    """
    velocidad_str = f"{info['speed']} MHz" if info['speed'] else "No disponible"
    return [
        "RAM INFORMATION",
        "----------------------------------------",
        f"Type: {info['type']}",
        f"Speed: {velocidad_str}",
        f"Total: {format_bytes(info['total'])}",
    ]


def get_ram_usage():
    """Obtiene el uso actual de la RAM.

    Retorna diccionario con: total, available, percent.
    """
    mem = psutil.virtual_memory()
    return {
        'total': mem.total,
        'available': mem.available,
        'percent': mem.percent,
    }
