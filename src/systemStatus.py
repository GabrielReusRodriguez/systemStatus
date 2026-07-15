"""Programa principal SystemStatus.

Muestra información y uso de los recursos del sistema en tiempo real
con actualizaciones diferenciales en la terminal.
"""

import argparse
import os
import sys
import time
import tty
import termios
import select

# Agregar src al path para importar módulos hermanos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# pylint: disable=wrong-import-position,import-error
from cpuHandler import (
    get_cpu_info,
    get_total_cpu_usage,
    get_per_core_usage,
    init_cpu_usage,
    format_cpu_info_lineas,
    format_cpu_usage_lineas,
)
from ramHandler import get_ram_info, format_ram_info_lineas


def parse_args():
    """Parsea los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description='SystemStatus - Monitor de recursos del sistema'
    )
    parser.add_argument(
        '--refresh',
        type=float,
        default=1.0,
        help='Intervalo de refresco en segundos (default: 1.0)'
    )
    return parser.parse_args()


def get_terminal_width():
    """Obtiene el ancho del terminal."""
    try:
        return os.get_terminal_size().columns
    except (ValueError, OSError):
        return 80


class KeyboardHandler:
    """Maneja la entrada del teclado en modo raw para detectar 'q' sin Enter."""

    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.is_terminal = os.isatty(self.fd)
        self.old_settings = None
        if self.is_terminal:
            self.old_settings = termios.tcgetattr(self.fd)
            tty.setraw(self.fd)

    def restore(self):
        """Restaura la configuración original de la terminal."""
        if self.old_settings is not None:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

    def is_q_pressed(self):
        """Verifica si la tecla 'q' fue presionada (no bloqueante)."""
        if not self.is_terminal:
            return False
        if select.select([sys.stdin], [], [], 0)[0]:
            char = sys.stdin.read(1)
            return char == 'q'
        return False


class Display:
    """Maneja la visualización diferencial en la terminal.

    Solo actualiza las líneas que han cambiado desde la última impresión.
    """

    def __init__(self):
        self.lineas_previas = []
        self.first_render = True

    def update(self, lineas):
        """Actualiza la pantalla con las nuevas líneas.

        Compara cada línea con la anterior y solo reescribe las que cambiaron.
        """
        if self.first_render:
            # Limpiar pantalla y posicionar cursor al inicio
            sys.stdout.write("\033[2J\033[H")
            for i, linea in enumerate(lineas):
                sys.stdout.write(f"\033[{i + 1};1H\033[K{linea}")
            sys.stdout.flush()
            self.first_render = False
        else:
            # Actualizar solo líneas que cambiaron
            for i in range(max(len(lineas), len(self.lineas_previas))):
                linea_nueva = lineas[i] if i < len(lineas) else None
                linea_previa = self.lineas_previas[i] if i < len(self.lineas_previas) else None

                if linea_nueva != linea_previa:
                    sys.stdout.write(f"\033[{i + 1};1H\033[K")
                    if linea_nueva is not None:
                        sys.stdout.write(linea_nueva)
            sys.stdout.flush()

        self.lineas_previas = list(lineas)

    def clear(self):
        """Limpia la pantalla y restaura el cursor."""
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()


def calcular_ancho_barra():
    """Calcula el ancho óptimo de la barra de progreso basado en el terminal.

    Calcula el ancho disponible para la barra restando el prefijo
    de las líneas de uso al ancho total del terminal.
    """
    ancho_terminal = get_terminal_width()

    # Ancho fijo del prefijo de cada línea de uso
    # "Total CPU:    XX,XX%  " o "Core XX:      XX,XX%  "
    prefijo_total = len("Total CPU:    XX,XX%  ")
    prefijo_core = len("Core XX:      XX,XX%  ")
    prefijo_max = max(prefijo_total, prefijo_core)

    # Ancho disponible para la barra (incluyendo el '|')
    ancho_barra = ancho_terminal - prefijo_max - 1
    return max(10, ancho_barra)


def main():
    """Función principal del programa."""
    args = parse_args()
    intervalo = args.refresh

    keyboard = KeyboardHandler()
    display = Display()

    try:
        # Obtener información estática de la CPU
        info_cpu = get_cpu_info()
        lineas_info = format_cpu_info_lineas(info_cpu)

        # Obtener información estática de la RAM (RF-003)
        info_ram = get_ram_info()
        lineas_ram = format_ram_info_lineas(info_ram)

        # Inicializar medidor de uso (primera lectura retorna 0)
        init_cpu_usage()
        time.sleep(0.1)

        # Obtener número de cores para calcular ancho de barra
        ancho_barra = calcular_ancho_barra()

        # Obtener primera lectura de uso
        uso_total = get_total_cpu_usage()
        usos_cores = get_per_core_usage()
        lineas_uso = format_cpu_usage_lineas(uso_total, usos_cores, ancho_barra)

        # Combinar: CPU info + separator + CPU uso + separator + RAM info (RNF-007)
        lineas_completas = (
            lineas_info + ['', ''] + lineas_uso + ['', ''] + lineas_ram
        )
        display.update(lineas_completas)

        # Bucle principal
        while True:
            time.sleep(intervalo)

            # Verificar si se presionó 'q' (RNF-005)
            if keyboard.is_q_pressed():
                break

            # Recalcular ancho de barra por si cambió el tamaño del terminal
            ancho_barra = calcular_ancho_barra()

            # Obtener nuevos datos de uso
            uso_total = get_total_cpu_usage()
            usos_cores = get_per_core_usage()
            lineas_uso = format_cpu_usage_lineas(uso_total, usos_cores, ancho_barra)

            # Combinar y actualizar solo lo que cambió
            lineas_completas = (
                lineas_info + ['', ''] + lineas_uso + ['', ''] + lineas_ram
            )
            display.update(lineas_completas)

    except KeyboardInterrupt:
        pass
    finally:
        keyboard.restore()
        display.clear()


if __name__ == '__main__':
    main()
