# SystemStatus

## Metadatos del proyecto

| Campo             | Valor |
|-------------------|-------|
| **Nombre**        | SystemStatus |
| **Versión Spec**  | 1.1.0 |
| **Fecha**         | 2026-07-14 |
| **Autor**         | Gabriel Reus |
| **Estado**        | draft |
| **Repo**          | git@github.com:GabrielReusRodriguez/systemStatus.git |

---

## 1. Vision General

### 1.1 Descripcion
Como ingeniero informático, necesito una aplicación que se ejecute desde consola Linux para obtener el uso de recursos del ordenador en este preciso momento y muestre la información de forma visual y sencilla. 

### 1.2 Objetivos 
Mostrar por consola el uso y rendimiento de los recursos de la máquina local donde se ejecuta.

### 1.3 NO entra en objetivos
- Interfaz gráfica

---

## 2. Stack tecnológico
- Se usará Python 3 de un entorno virtual python .venv

### Convenciones de  Código
- Nombrado de ficheros: camelCase
- Estructura de carpetas:
    -- src/ para la carpeta de código fuente
    -- test/ para la carpeta donde estarán los tests del codigo
    -- deps/ para el fichero requirements.txt con las dependencias del proyecto
    -- docs/ para la documentación. Incluye las especificaciones  del proyecto
    -- .venv/ la carpeta con el entorno virtual de python
- Idioma de los comentarios: español
- El código ha de pasar la validación de lintern sobre python

## 3. Arquitectura

### 3.1 Diagrama de componentes.
- La aplicación tendrá los siguientes componentes:
    -- systemStatus programa principal que se comunicará con los demás componentes para crear el reporte de situación.
    -- CpuHandler que obtendrá los datos referentes a la cpu.
    -- RamHandler que obtendrá los datos referentes a la ram.
    -- NetworkHandler que obtendrá los datos referentes a la red. 

---

# 4. Requisitos Funcionales

| ID     | Descripción                  | Estado       | Spec                                                           |
|--------|------------------------------|--------------|----------------------------------------------------------------|
| RF-001 | Caracteristics de la CPU     | ✅ Aprobado  | [RF-001-Informacion_CPU.md](specs/RF-001-Informacion_CPU.md)   |
| RF-002 | Uso de la CPU                | ✅ Aprobado  | [RF-002-Uso_CPU.md](specs/RF-002-Uso-CPU.md)                   |
| RF-003 | Caracteristicas de la  RAM   | 🔄 Borrador  | [RF-003-Informacion_RAM.md](specs/RF-003-Informacion_RAM.md)   |
| RF-004 | Uso de la RAM                | 🔄 Borrador  | [RF-004-Uso_RAM.md](specs/RF-004-Uso_RAM.md)                   |
| RF-005 | Uso de la RED                | 🔄 Borrador  | [RF-005-Uso_RED.md](specs/RF-005-Uso_RED.md)                   |


# 5. Requisitos NO Funcionales.

RNF-001: Rendimiento
- La aplicación debe ser ligera

RNF-002: Interfaz de usuario no bloqueante
- La aplicación se ejecutará en bucle y SOLO actualizará los valores que hayan cambiado mediante logica de 'diferencial': calcula cambios y ejecuta actualizaciones solo donde sea estrictamente necesari. Eso significa que no imprimirá toda la pantalla si no solo los cambios.

No se deben hacer llamadas bloqueantes, el usuario ha de poder controlar la aplicación en todo momento.

RNF-003: El programa ha de ser portable a cualquier distribución Linux.
- La aplicación ha de funcionar en cualquier distribución de Linux sin cambios en el código.

RNF-004: Presentación de datos.
- Se mostrarán los datos por consola pero actualizando los datos mostrados, no imprimiendolos de nuevo.

RNF-005: Salir de la aplicación
- El usuario podrá salir de la aplicación presionando la tecla 'q' sin necesidad de entrarla precionando enter.

RNF-006: Formato de los porcentajes
- Todos los valores porcentuales deben expresarse con el patrón `NN,DD%` donde:
  - `NN` = 2 dígitos enteros con padding de cero a la izquierda
  - `DD` = 2 dígitos decimales
  - Separador decimal: coma (`,`)
  - Símbolo de porcentaje: `%` sin espacio previo
- Rango válido: `00,00%` a `99,99%`
- Ejemplos válidos: `04,58%`, `00,00%`, `99,99%`
- Ejemplos inválidos: `4,58%`, `4.5%`, `04.58%`, `100%`


RNF-007: Separación entre secciones
- Cada sección (cpu, ram y red) estará separado de la siguiente por  2 líneas en blanco.

RNF-008: Formato de las cantidades de datos.
- Todas las cantidades de datos se mostrarán en formatos legibles para humanos, esto es: Tb, Gb, Mb, Kb, o B.

RNF-009: Tiempo de refresco
- El tiempo de refresco de los datos ha de ser parametrizable. Si no se recibe nada, será cada 1 segundo.

---

# 8. Instrucciones especificas para el agent IA.
## 8.1 Reglas de ejecución
- Antes de escribir código, lee toda la spec completa.
- Haz un commit por requisito funcional o tarea con el formato de mensaje: feat(RF-XXX): descripción.
- No improvises, si algo no está definido en la spec, detente y pregunta en lugar de asumir.
- Implementa solo las RF con estado "Aprobado"

## 8.5 Criterios de "Done"
El proyecto se considerará completo cuando:
- Todos los RF marcados con estado "Aprobado" están implementados
- Todos los criterios de aceptación verificados.
- Cumple todos los Requisitos No Funcionales, RNF.
- Lintern pasa sin warnings
- README actualizado con la documentación del proyecto.