# SystemStatus

## Descripcion
SystemStatus es una aplicacion CLI para monitorizar recursos del sistema en Linux.

## Instalacion

### Requisitos
- Python 3.8+
- Linux

### Pasos
1. Clonar el repositorio
2. Crear entorno virtual: `python3 -m venv venv`
3. Activar: `source venv/bin/activate`
4. Instalar deps: `pip install -r deps/requirements.txt`

## Uso
```bash
# Reporte unico (pulsa 'q' para salir)
python3 src/systemStatus.py

# Modo continuo (actualiza cada segundo, pulsa 'q' para salir)
python3 src/systemStatus.py -c

# Con intervalo personalizado
python3 src/systemStatus.py -c -i 2.0
```

## Requisitos Funcionales Implementados
- RF-001: Info CPU (modelo, familia, frecuencia)
- RF-002: Rendimiento CPU con cores FISICOS y barras █
- RF-003: Info RAM (tipo, velocidad)
- RF-004: Uso RAM (total, libre, %, barra █)
- RF-005: Uso red (subidos, bajados)

## Requisitos No Funcionales Implementados
- RNF-001: Aplicacion ligera
- RNF-002: No bloqueante
- RNF-003: Portable a cualquier distribucion Linux
- RNF-004: Actualizacion de datos sin reimprimir
- RNF-005: Salir con tecla 'q'
- RNF-006: Porcentajes en formato XX.XX%
- RNF-007: 2 lineas en blanco entre secciones
- RNF-008: Formato legible para cantidades (TB, GB, MB, KB, B)
