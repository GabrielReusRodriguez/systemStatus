"""Manejador de información y uso de la CPU."""

import psutil


def _parse_cache_size(size_str):
    """Convierte una cadena de tamaño de cache (ej: '32K') a bytes."""
    size_str = size_str.strip()
    if size_str.endswith('K'):
        return int(size_str[:-1]) * 1024
    if size_str.endswith('M'):
        return int(size_str[:-1]) * 1024 * 1024
    if size_str.endswith('G'):
        return int(size_str[:-1]) * 1024 * 1024 * 1024
    return int(size_str)


def _read_cpu_model():
    """Lee el modelo de la CPU desde /proc/cpuinfo."""
    try:
        with open('/proc/cpuinfo', 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                if linea.startswith('model name'):
                    return linea.split(':', 1)[1].strip()
    except (FileNotFoundError, PermissionError):
        return "Desconocido"
    return "Desconocido"


def _read_cache_total(nivel):
    """Lee el total de cache para un nivel dado (1 o 2) desde sysfs.

    Lee la cache de un solo core (cpu0) y multiplica por el número de cores.
    """
    cache_map = {1: [0, 1], 2: [2]}  # index0=L1d, index1=L1i, index2=L2
    indices = cache_map.get(nivel, [])
    total_bytes = 0

    for indice in indices:
        ruta = f'/sys/devices/system/cpu/cpu0/cache/index{indice}/size'
        try:
            with open(ruta, 'r', encoding='utf-8') as archivo:
                total_bytes += _parse_cache_size(archivo.read())
        except (FileNotFoundError, PermissionError):
            pass

    num_cores = psutil.cpu_count(logical=False) or 1
    return total_bytes * num_cores


def format_bytes(bytes_value):
    """Formatea bytes a formato legible para humanos (Tb, Gb, Mb, Kb, B)."""
    if bytes_value <= 0:
        return "0 B"
    unidades = ['B', 'Kb', 'Mb', 'Gb', 'Tb']
    for i, unidad in enumerate(unidades):
        if bytes_value < 1024 or i == len(unidades) - 1:
            return f"{bytes_value:.0f} {unidad}"
        bytes_value /= 1024
    return f"{bytes_value:.0f} Tb"


def format_percentage(valor):
    """Formatea un porcentaje con el patrón NN,DD% (RNF-006).

    Ejemplos: 04,58% | 00,00% | 99,99%
    """
    # Redondear para evitar problemas de precisión de punto flotante
    valor = round(valor, 2)
    entero = int(valor)
    decimal = int(round((valor - entero) * 100))
    return f"{entero:02d},{decimal:02d}%"


def get_cpu_info():
    """Obtiene información estática de la CPU.

    Retorna diccionario con: model, frequency, cores, threads,
    cache_l1 (bytes), cache_l2 (bytes).
    """
    modelo = _read_cpu_model()
    freq = psutil.cpu_freq()
    frecuencia = freq.max if freq else 0.0
    cores_fisicos = psutil.cpu_count(logical=False) or 0
    hilos = psutil.cpu_count(logical=True) or 0
    cache_l1 = _read_cache_total(1)
    cache_l2 = _read_cache_total(2)

    return {
        'model': modelo,
        'frequency': frecuencia,
        'cores': cores_fisicos,
        'threads': hilos,
        'cache_l1': cache_l1,
        'cache_l2': cache_l2,
    }


def init_cpu_usage():
    """Inicializa el medidor de uso de la CPU.

    Debe llamarse antes de get_total_cpu_usage() para que la primera
    lectura real retorne un valor válido.
    """
    psutil.cpu_percent(interval=None, percpu=True)


def get_total_cpu_usage():
    """Obtiene el porcentaje de uso total de la CPU.

    Retorna un float entre 0.0 y 100.0.
    """
    return psutil.cpu_percent(interval=None)


def get_per_core_usage():
    """Obtiene el porcentaje de uso por cada core físico.

    Retorna lista de floats entre 0.0 y 100.0.
    """
    return psutil.cpu_percent(interval=None, percpu=True)


def format_progress_bar(porcentaje, ancho):
    """Genera una barra de progreso en ASCII art.

    Args:
        porcentaje: valor entre 0.0 y 100.0
        ancho: ancho total de la barra en caracteres
    """
    relleno = int(porcentaje * ancho / 100)
    relleno = min(relleno, ancho)
    return f"|{'█' * relleno}{' ' * (ancho - relleno)}"


def format_cpu_info_lineas(info):
    """Formatea la información estática de la CPU en líneas para mostrar.

    Retorna lista de strings con las líneas formateadas.
    """
    return [
        "CPU INFORMATION",
        "----------------------------------------",
        f"Model: {info['model']}",
        f"Frequency: {info['frequency']:.2f} MHz",
        f"Cores: {info['cores']} cores / {info['threads']} threads",
        f"Cache L1: {format_bytes(info['cache_l1'])}",
        f"Cache L2: {format_bytes(info['cache_l2'])}",
    ]


def format_cpu_usage_lineas(usos_totales, usos_cores, ancho_barra):
    """Formatea el uso de la CPU en líneas con barras de progreso.

    Args:
        usos_totales: porcentaje total de uso de la CPU
        usos_cores: lista de porcentajes por core
        ancho_barra: ancho de las barras de progreso

    Retorna lista de strings con las líneas formateadas.
    """
    lineas = []
    pct_total = format_percentage(usos_totales)
    barra_total = format_progress_bar(usos_totales, ancho_barra)
    lineas.append(f"Total CPU:    {pct_total}  {barra_total}")

    for i, uso in enumerate(usos_cores, 1):
        pct_core = format_percentage(uso)
        barra_core = format_progress_bar(uso, ancho_barra)
        lineas.append(f"Core {i:02d}:      {pct_core}  {barra_core}")

    return lineas
