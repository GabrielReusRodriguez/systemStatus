"""Tests unitarios para el módulo ramHandler."""

import sys
import os
import struct
import unittest
from unittest.mock import patch, MagicMock

# Agregar src al path para importar los módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# pylint: disable=wrong-import-position,import-error
from ramHandler import (
    _get_ram_from_dmidecode,
    _get_ram_from_sysfs,
    get_ram_info,
    format_ram_info_lineas,
)


class TestGetRamFromDmidecode(unittest.TestCase):
    """Tests para la función _get_ram_from_dmidecode."""

    @patch('ramHandler.subprocess.run')
    def test_dmidecode_exitoso(self, mock_run):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = (
            "Memory Device\n"
            "	Type: DDR4\n"
            "	Size: 16384 MB\n"
            "	Speed: 3200 MHz\n"
            "\n"
            "Memory Device\n"
            "	Type: DDR4\n"
            "	Size: 16384 MB\n"
            "	Speed: 3200 MHz\n"
        )
        mock_run.return_value = mock_result

        resultado = _get_ram_from_dmidecode()

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado['type'], 'DDR4')
        self.assertEqual(resultado['speed'], 3200)

    @patch('ramHandler.subprocess.run')
    def test_dmidecode_sin_permisos(self, mock_run):
        mock_run.side_effect = PermissionError()

        resultado = _get_ram_from_dmidecode()
        self.assertIsNone(resultado)

    @patch('ramHandler.subprocess.run')
    def test_dmidecode_no_encontrado(self, mock_run):
        mock_run.side_effect = FileNotFoundError()

        resultado = _get_ram_from_dmidecode()
        self.assertIsNone(resultado)

    @patch('ramHandler.subprocess.run')
    def test_dmidecode_codigo_retorno_no_cero(self, mock_run):
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        resultado = _get_ram_from_dmidecode()
        self.assertIsNone(resultado)

    @patch('ramHandler.subprocess.run')
    def test_dmidecode_tipo_unknown(self, mock_run):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = (
            "Memory Device\n"
            "	Type: Unknown\n"
            "	Speed: 3200 MHz\n"
        )
        mock_run.return_value = mock_result

        resultado = _get_ram_from_dmidecode()
        self.assertIsNone(resultado)

    @patch('ramHandler.subprocess.run')
    def test_dmidecode_sin_velocidad(self, mock_run):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = (
            "Memory Device\n"
            "	Type: DDR5\n"
        )
        mock_run.return_value = mock_result

        resultado = _get_ram_from_dmidecode()
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado['type'], 'DDR5')
        self.assertIsNone(resultado['speed'])


class TestGetRamFromSysfs(unittest.TestCase):
    """Tests para la función _get_ram_from_sysfs."""

    @patch('ramHandler.open', create=True)
    def test_sysfs_exitoso(self, mock_open_func):
        # Construir datos binarios simulando una entrada DMI tipo 17
        # Offset 0x17-0x18 = Speed (little-endian)
        datos = b'\x00' * 0x17 + struct.pack('<H', 2400)  # 2400 MHz
        # Insertar string "DDR4" en algún lugar del archivo
        datos = datos[:10] + b'DDR4' + datos[14:]

        mock_open_func.return_value.__enter__ = lambda s: s
        mock_open_func.return_value.__exit__ = MagicMock(return_value=False)
        mock_open_func.return_value.read.return_value = datos

        resultado = _get_ram_from_sysfs()

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado['type'], 'DDR4')
        self.assertEqual(resultado['speed'], 2400)

    @patch('ramHandler.open', create=True)
    def test_sysfs_archivo_no_existe(self, mock_open_func):
        mock_open_func.side_effect = FileNotFoundError()

        resultado = _get_ram_from_sysfs()
        self.assertIsNone(resultado)

    @patch('ramHandler.open', create=True)
    def test_sysfs_archivo_muy_corto(self, mock_open_func):
        mock_open_func.return_value.__enter__ = lambda s: s
        mock_open_func.return_value.__exit__ = MagicMock(return_value=False)
        mock_open_func.return_value.read.return_value = b'\x00' * 5

        resultado = _get_ram_from_sysfs()
        self.assertIsNone(resultado)

    @patch('ramHandler.open', create=True)
    def test_sysfs_tipo_no_encontrado(self, mock_open_func):
        datos = b'\x00' * 30  # Sin string de tipo conocido

        mock_open_func.return_value.__enter__ = lambda s: s
        mock_open_func.return_value.__exit__ = MagicMock(return_value=False)
        mock_open_func.return_value.read.return_value = datos

        resultado = _get_ram_from_sysfs()
        self.assertIsNone(resultado)


class TestGetRamInfo(unittest.TestCase):
    """Tests para la función get_ram_info."""

    @patch('ramHandler._get_ram_from_dmidecode')
    @patch('ramHandler.psutil')
    def test_usa_dmidecode(self, mock_psutil, mock_dmidecode):
        mock_mem = MagicMock()
        mock_mem.total = 17179869184  # 16 GB
        mock_psutil.virtual_memory.return_value = mock_mem

        mock_dmidecode.return_value = {'type': 'DDR4', 'speed': 3200}

        info = get_ram_info()

        self.assertEqual(info['type'], 'DDR4')
        self.assertEqual(info['speed'], 3200)
        self.assertEqual(info['total'], 17179869184)
        mock_dmidecode.assert_called_once()

    @patch('ramHandler._get_ram_from_sysfs')
    @patch('ramHandler._get_ram_from_dmidecode')
    @patch('ramHandler.psutil')
    def test_fallback_a_sysfs(self, mock_psutil, mock_dmidecode, mock_sysfs):
        mock_mem = MagicMock()
        mock_mem.total = 8589934592  # 8 GB
        mock_psutil.virtual_memory.return_value = mock_mem

        mock_dmidecode.return_value = None
        mock_sysfs.return_value = {'type': 'DDR3', 'speed': 1600}

        info = get_ram_info()

        self.assertEqual(info['type'], 'DDR3')
        self.assertEqual(info['speed'], 1600)
        mock_dmidecode.assert_called_once()
        mock_sysfs.assert_called_once()

    @patch('ramHandler._get_ram_from_sysfs')
    @patch('ramHandler._get_ram_from_dmidecode')
    @patch('ramHandler.psutil')
    def test_no_disponible(self, mock_psutil, mock_dmidecode, mock_sysfs):
        mock_mem = MagicMock()
        mock_mem.total = 4294967296  # 4 GB
        mock_psutil.virtual_memory.return_value = mock_mem

        mock_dmidecode.return_value = None
        mock_sysfs.return_value = None

        info = get_ram_info()

        self.assertEqual(info['type'], 'No disponible')
        self.assertIsNone(info['speed'])
        self.assertEqual(info['total'], 4294967296)


class TestFormatRamInfoLineas(unittest.TestCase):
    """Tests para la función format_ram_info_lineas."""

    def test_formato_con_velocidad(self):
        info = {'type': 'DDR4', 'speed': 3200, 'total': 17179869184}
        lineas = format_ram_info_lineas(info)

        self.assertEqual(len(lineas), 5)
        self.assertEqual(lineas[0], "RAM INFORMATION")
        self.assertEqual(lineas[1], "----------------------------------------")
        self.assertEqual(lineas[2], "Type: DDR4")
        self.assertEqual(lineas[3], "Speed: 3200 MHz")
        self.assertIn("16 Gb", lineas[4])

    def test_formato_sin_velocidad(self):
        info = {'type': 'DDR5', 'speed': None, 'total': 8589934592}
        lineas = format_ram_info_lineas(info)

        self.assertEqual(len(lineas), 5)
        self.assertEqual(lineas[2], "Type: DDR5")
        self.assertEqual(lineas[3], "Speed: No disponible")
        self.assertIn("8 Gb", lineas[4])

    def test_formato_no_disponible(self):
        info = {'type': 'No disponible', 'speed': None, 'total': 4294967296}
        lineas = format_ram_info_lineas(info)

        self.assertEqual(lineas[2], "Type: No disponible")
        self.assertEqual(lineas[3], "Speed: No disponible")


if __name__ == '__main__':
    unittest.main()
