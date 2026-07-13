"""
Programa principal SystemStatus.
Coordinador que utiliza los diferentes handlers para crear el reporte.
Implementa RNF-004, RNF-005, RNF-006, RNF-007, RNF-008.
"""
import time
import sys
import select
import psutil
from cpuHandler import CpuHandler
from ramHandler import RamHandler
from networkHandler import NetworkHandler


class SystemStatus:
    """Clase principal que coordina la obtencion y visualizacion de datos."""

    def __init__(self):
        """Inicializa el programa SystemStatus."""
        self.cpu_handler = CpuHandler()
        self.ram_handler = RamHandler()
        self.network_handler = NetworkHandler()
        self._running = False

    def show_report(self, continuous=False, interval=1.0):
        """
        Muestra el reporte del sistema.

        Args:
            continuous: Si True, actualiza el reporte profundamente
            interval: Intervalo entre actualizaciones en segundos
        """
        self._running = True

        try:
            # Primera vez, imprimir completo
            self._print_report()

            if not continuous:
                # Modo no continuo, esperar a que se pulse 'q' para salir (RNF-005)
                while self._running:
                    if self._check_for_q():
                        self._running = False
                        print("\n")
                        break
                    time.sleep(0.1)
                return

            # Modo continuo (RNF-004: actualizar sin imprimir de nuevo)
            while self._running:
                self._move_cursor_up()
                self._print_report()

                # Esperar el intervalo o hasta que se pulse 'q' (RNF-005)
                start_time = time.time()
                while time.time() - start_time < interval:
                    if self._check_for_q():
                        self._running = False
                        print("\n")
                        break
                    time.sleep(0.1)

                if not self._running:
                    break

        except KeyboardInterrupt:
            self._running = False
            print("\n")

    def _check_for_q(self):
        """
        Comprueba si se ha pulsado la tecla 'q' (RNF-005).

        Returns:
            bool: True si se pulso 'q'
        """
        try:
            if select.select([sys.stdin], [], [], 0)[0]:
                char = sys.stdin.read(1)
                if char.lower() == 'q':
                    return True
        except Exception:
            pass
        return False

    def _move_cursor_up(self):
        """
        Mueve el cursor hacia arriba para actualizar en el mismo lugar (RNF-004).
        """
        physical_count = self.cpu_handler.get_physical_cores_count()

        # Calcular lineas totales del reporte:
        # Header: 3 lineas + 1 vacia = 4
        # CPU INFO: 1 header + 1 separador + 3 datos + 1 vacia = 6
        # CPU USAGE: 1 header + 1 separador + 1 total + N cores = 3 + N
        # 2 vacias (RNF-007) = 2
        # RAM INFO: 1 header + 1 separador + 2 datos + 1 vacia = 5
        # RAM USAGE: 1 header + 1 separador + 4 datos = 6
        # 2 vacias (RNF-007) = 2
        # NETWORK: 1 header + 1 separador + 2 datos + 1 vacia = 5
        # Footer: 3 lineas
        # Total: 4 + 6 + (3+N) + 2 + 5 + 6 + 2 + 5 + 3 = 36 + N

        total_lines = 36 + physical_count
        print(f"\033[{total_lines}A", end="", flush=True)

    def _print_report(self):
        """Imprime el reporte completo del sistema."""
        print("=" * 60)
        print("SYSTEM STATUS REPORT")
        print("=" * 60)
        print()

        # Seccion CPU
        print("CPU INFORMATION")
        print("-" * 40)
        print(self.cpu_handler.format_cpu_info())
        print()

        print("CPU USAGE")
        print("-" * 40)
        print(self.cpu_handler.format_cpu_usage())

        # RNF-007: 2 lineas en blanco entre secciones
        print()
        print()

        # Seccion RAM
        print("RAM INFORMATION")
        print("-" * 40)
        print(self.ram_handler.format_ram_info())
        print()

        print("RAM USAGE")
        print("-" * 40)
        print(self.ram_handler.format_ram_usage())

        # RNF-007: 2 lineas en blanco entre secciones
        print()
        print()

        # Seccion Network
        print("NETWORK USAGE")
        print("-" * 40)
        print(self.network_handler.format_network_usage())
        print()

        print("=" * 60)
        print("Press 'q' to exit")
        print("=" * 60)


def main():
    """Funcion principal de entrada al programa."""
    import argparse

    parser = argparse.ArgumentParser(
        description='SystemStatus - Monitor de recursos del sistema'
    )
    parser.add_argument(
        '-c', '--continuous',
        action='store_true',
        help='Modo continuo, actualiza el reporte cada segundo'
    )
    parser.add_argument(
        '-i', '--interval',
        type=float,
        default=1.0,
        help='Intervalo entre actualizaciones en segundos'
    )

    args = parser.parse_args()

    system_status = SystemStatus()
    system_status.show_report(
        continuous=args.continuous,
        interval=args.interval
    )


if __name__ == '__main__':
    main()
