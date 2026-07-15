# SystemStatus

Monitor de recursos del sistema en tiempo real para Linux.

## Descripción

SystemStatus es una aplicación de consola que muestra el uso y rendimiento de los recursos de la máquina local. Está diseñada para ser ligera, portable a cualquier distribución Linux y no bloqueante.

## Instalación

```bash
# Clonar el repositorio
git clone git@github.com:GabrielReusRodriguez/systemStatus.git
cd systemStatus

# Crear entorno virtual
python3 -m venv .venv

# Activar entorno virtual
source .venv/bin/activate

# Instalar dependencias
pip install -r deps/requirements.txt
```

## Uso

```bash
# Ejecutar con intervalo de refresco por defecto (1 segundo)
python src/systemStatus.py

# Ejecutar con intervalo de refresco personalizado
python src/systemStatus.py --refresh 2

# Salir de la aplicación
Presionar la tecla 'q'
```

## Características

- **RF-001**: Información de la CPU (modelo, frecuencia, cores, threads, cache L1/L2)
- **RF-002**: Uso de la CPU en tiempo real con barras de progreso ASCII
- **Actualización diferencial**: Solo se actualizan los valores que cambiaron
- **Input no bloqueante**: La tecla 'q' se detecta sin necesidad de presionar Enter
- **Barra de progreso adaptable**: Se ajusta al ancho del terminal
- **Formato de porcentajes**: Patrón `NN,DD%` (ej: `04,58%`)

## Arquitectura

```
src/
├── systemStatus.py      # Programa principal
├── cpuHandler.py        # Manejador de CPU
├── ramHandler.py        # Manejador de RAM (stub)
└── networkHandler.py    # Manejador de red (stub)
```

## Ejecutar Tests

```bash
python -m unittest test.testCpuHandler -v
```

## Verificar Código

```bash
# Ejecutar pylint
PYTHONPATH=src pylint src/*.py test/*.py
```

## Licencia

GPLv3
