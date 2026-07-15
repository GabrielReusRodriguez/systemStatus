"""Tests unitarios para el módulo cpuHandler."""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Agregar src al path para importar los módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# pylint: disable=wrong-import-position,import-error
from cpuHandler import (
    format_bytes,
    format_percentage,
    format_progress_bar,
    format_cpu_info_lineas,
    format_cpu_usage_lineas,
    _parse_cache_size,
    get_cpu_info,
    get_total_cpu_usage,
    get_per_core_usage,
)


class TestFormatBytes(unittest.TestCase):
    """Tests para la función format_bytes."""

    def test_cero_bytes(self):
        self.assertEqual(format_bytes(0), "0 B")

    def test_bytes_negativos(self):
        self.assertEqual(format_bytes(-100), "0 B")

    def test_bytes(self):
        self.assertEqual(format_bytes(500), "500 B")

    def test_kilobytes(self):
        self.assertEqual(format_bytes(1024), "1 Kb")
        self.assertEqual(format_bytes(1536), "2 Kb")

    def test_megabytes(self):
        self.assertEqual(format_bytes(1048576), "1 Mb")
        self.assertEqual(format_bytes(5242880), "5 Mb")

    def test_gigabytes(self):
        self.assertEqual(format_bytes(1073741824), "1 Gb")

    def test_terabytes(self):
        self.assertEqual(format_bytes(1099511627776), "1 Tb")


class TestFormatPercentage(unittest.TestCase):
    """Tests para la función format_percentage (RNF-006)."""

    def test_cero_por_ciento(self):
        self.assertEqual(format_percentage(0.0), "00,00%")

    def test_porcentaje_entero(self):
        self.assertEqual(format_percentage(5.0), "05,00%")

    def test_porcentaje_con_decimales(self):
        self.assertEqual(format_percentage(4.58), "04,58%")

    def test_porcentaje_alto(self):
        self.assertEqual(format_percentage(99.99), "99,99%")

    def test_porcentaje_un_digito(self):
        self.assertEqual(format_percentage(1.23), "01,23%")

    def test_porcentaje_cien(self):
        # 100% no es válido según RNF-006 (rango 00,00% a 99,99%)
        # pero la función debe manejarlo sin error
        resultado = format_percentage(100.0)
        self.assertEqual(resultado, "100,00%")


class TestFormatProgressBar(unittest.TestCase):
    """Tests para la función format_progress_bar."""

    def test_barra_cero(self):
        resultado = format_progress_bar(0.0, 10)
        self.assertEqual(resultado, "|          ")

    def test_barra_cien(self):
        resultado = format_progress_bar(100.0, 10)
        self.assertEqual(resultado, "|██████████")

    def test_barra_mitad(self):
        resultado = format_progress_bar(50.0, 10)
        self.assertEqual(resultado, "|█████     ")

    def test_barra_un_caracter(self):
        resultado = format_progress_bar(10.0, 10)
        self.assertEqual(resultado, "|█         ")

    def test_barra_ancho_personalizado(self):
        resultado = format_progress_bar(25.0, 20)
        self.assertEqual(len(resultado), 21)  # | + 20 caracteres
        self.assertTrue(resultado.startswith("|"))


class TestParseCacheSize(unittest.TestCase):
    """Tests para la función _parse_cache_size."""

    def test_kilobytes(self):
        self.assertEqual(_parse_cache_size("32K"), 32768)

    def test_megabytes(self):
        self.assertEqual(_parse_cache_size("512M"), 536870912)

    def test_gigabytes(self):
        self.assertEqual(_parse_cache_size("2G"), 2147483648)

    def test_bytes(self):
        self.assertEqual(_parse_cache_size("1024"), 1024)


class TestFormatCpuInfoLineas(unittest.TestCase):
    """Tests para la función format_cpu_info_lineas."""

    def test_formato_lineas(self):
        info = {
            'model': 'Test CPU',
            'frequency': 3500.0,
            'cores': 4,
            'threads': 8,
            'cache_l1': 262144,  # 256 Kb
            'cache_l2': 1048576,  # 1 Mb
        }
        lineas = format_cpu_info_lineas(info)

        self.assertEqual(len(lineas), 7)
        self.assertEqual(lineas[0], "CPU INFORMATION")
        self.assertEqual(lineas[1], "----------------------------------------")
        self.assertIn("Test CPU", lineas[2])
        self.assertIn("3500.00 MHz", lineas[3])
        self.assertIn("4 cores / 8 threads", lineas[4])
        self.assertIn("256 Kb", lineas[5])
        self.assertIn("1 Mb", lineas[6])


class TestFormatCpuUsageLineas(unittest.TestCase):
    """Tests para la función format_cpu_usage_lineas."""

    def test_formato_lineas_uso(self):
        uso_total = 25.50
        usos_cores = [10.0, 20.0, 30.0, 40.0]
        ancho_barra = 20

        lineas = format_cpu_usage_lineas(uso_total, usos_cores, ancho_barra)

        # 1 línea total + 4 líneas de cores
        self.assertEqual(len(lineas), 5)
        self.assertIn("Total CPU:", lineas[0])
        self.assertIn("25,50%", lineas[0])
        self.assertIn("Core 01:", lineas[1])
        self.assertIn("10,00%", lineas[1])


class TestGetCpuInfo(unittest.TestCase):
    """Tests para la función get_cpu_info."""

    @patch('cpuHandler.psutil')
    def test_retorna_campos_requeridos(self, mock_psutil):
        mock_psutil.cpu_count.side_effect = lambda logical=True: 4 if logical else 2
        mock_freq = MagicMock()
        mock_freq.max = 3500.0
        mock_psutil.cpu_freq.return_value = mock_freq

        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__ = lambda s: s
            mock_open.return_value.__exit__ = MagicMock(return_value=False)
            mock_open.return_value.readline.side_effect = [
                'model name\t: Test CPU\n',
                '\n',
            ]

            # Mock para _read_cache_total
            with patch('cpuHandler._read_cache_total', return_value=262144):
                info = get_cpu_info()

        self.assertIn('model', info)
        self.assertIn('frequency', info)
        self.assertIn('cores', info)
        self.assertIn('threads', info)
        self.assertIn('cache_l1', info)
        self.assertIn('cache_l2', info)


class TestGetCpuUsage(unittest.TestCase):
    """Tests para las funciones de uso de CPU."""

    @patch('cpuHandler.psutil')
    def test_get_total_cpu_usage(self, mock_psutil):
        mock_psutil.cpu_percent.return_value = 45.5
        uso = get_total_cpu_usage()
        self.assertEqual(uso, 45.5)

    @patch('cpuHandler.psutil')
    def test_get_per_core_usage(self, mock_psutil):
        mock_psutil.cpu_percent.return_value = [10.0, 20.0, 30.0, 40.0]
        usos = get_per_core_usage()
        self.assertEqual(len(usos), 4)
        self.assertEqual(usos[0], 10.0)


if __name__ == '__main__':
    unittest.main()
