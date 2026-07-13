# SystemStatus

## Metadatos del proyecto

| Campo | Valor |
|-------|-------|
| **Nombre** | SystemStatus |
| **Versión Spec** | 1.0.0 |
| **Fecha** | 2026-07-13 |
| **Autor** | Gabriel Reus |
| **Estado** | draft |
| **Repo** | git@github.com:GabrielReusRodriguez/systemStatus.git |

---

## 1. Vision General

### 1.1 Descripcion
Una aplicación que se ejecuta desde consola Linux para obtener el uso de recursos del ordenador en este preciso momento y muestre la información de forma visual de forma que te hagas una primera impresión rápidamente. 

### 1.2 Objetivos 
Mostrar por consola el uso y rendimiento de los recursos de la máquina local donde se ejecuta.

### 1.3 NO entra en objetivos
- Interfaz gráfica

---

## 2. Stack tecnológico
- Se usará Python 3 en un entorno virtual .

### Convenciones de  Código
- Nombrado de ficheros: camelCase
- Estructura de carpetas:
    -- src/ para la carpeta de código fuente
    -- test/ para la carpeta donde estarán los tests del codigo
    -- deps/ para el fichero requirements.txt con las dependencias del proyecto
    -- docs/ con la documentación del proyecto
    -- specs/ con las especificaciones del proyecto
- Idioma de los comentarios: español
- El código ha de pasar la validación de lintern sobre python

## 3. Arquitectura

### 3.1 Diagrama de componentes.
- La aplicación tendrá los siguientes componentes:
    -- systemStatus programa principal que se comunicará con los demás componentes para crear el reporte de situación.
    -- CpuHandler que obtendrá los datos referentes a la cpu.
    -- RamHandler que obtendrá los datos referentes a la ram.
    -- NetworkHandler que obtendrá los datos referentes a la red. 
    
# 4. Requisitos Funcionales

RF-001: Mostrar información de la cpu.
- Prioridad: Must
- Descripción: El programa ha de enseñar al usuario los datos referentes a la cpu del sistema: modelo, familia y frecuencia.

RF-002: Obtener el rendimiento de la cpu.
- Prioridad: Must
- Descripción: El programa ha de mostrar el uso de la cpu y los cores físicos mediante porcentajes y con una barra de progreso hecha en ascii art. Estos datos se actualizarán en tiempo real. Un ejemplo del formato sería:
```
Total CPU:   20.00%  |████████████████████
Core 01:     05.10%  |████████████
Core 02:     07.90%  |████████████████
Core 03:     01.10%  |█
Core 04:     00.10%  |
Core 05:     40.10%  |████████████████████
```
- Criterios de aceptación:
-- Aparece el modelo, familia de la cpu y la frecuencia de trabajo.
-- Aparece un porcentaje de la carga total por core físico.  
-- Se dibuja la barra de uso para cada core físico.

RF-003: Mostrar la información de la Memoria RAM.
- Prioridad: Must
- Descripcioń: El programa muestra el tipo de RAM (DDR5, DDR6... ) y la velocidad de la RAM.
- Criterios de aceptación:
-- Se visualiza el tipo de memoria RAM 

RF-004: Obtener el uso de la RAM. 
- Prioridad: Must
- Descripción: El programa ha de mostrar el total de RAM instalada en el sistema y  el total libre (ambas cantidades en formato legible para personas: Tb, Gb, Mb, Kb...)  así como el porcentaje de la RAM libre. Además se ha de mostrar un barra de progreso con el % de RAM libre. 
- Criterios de aceptación:
-- Se visualiza  el total de RAM instalada en el sistema
-- Se visualiza la RAM libre
-- Se visualiza el % de RAM libre
-- Se visualiza la  gráfica de RAM libre en forma de barra de progreso.

RF-005: Obtener uso de la red.
- Prioridad: Must
- Descripción: El programa muestra la cantidad de información subida y bajada desde el arranque del sistema.
- Criterios de aceptación:
-- Se visualiza la cantidad de información subida.
-- Se visualiza la cantidad de información bajada.

# 5. Requisitos NO Funcionales.

RNF-001: Rendimiento
- La aplicación debe ser ligera

RNF-002: Interfaz de usuario no bloqueante
- No se deben hacer llamadas bloqueantes, el usuario ha de poder controlar la aplicación en todo momento.

RNF-003: El programa ha de ser portable a cualquier distribución Linux.
- La aplicación ha de funcionar en cualquier distribución de Linux sin cambios en el código.

RNF-004: Presentación de datos.
- Se mostrarán los datos por consola pero actualizando los datos mostrados, no imprimiendolos de nuevo.

RNF-005: Salir de la aplicación
- El usuario podrá salir de la aplicación presionando la tecla 'q'

RNF-006: Formato de los porcentajes
- Todos los porcentajes serán con el formato: %d%d\.%d%d 

RNF-007: Separación entre secciones
- Cada sección (cpu, ram y red) estará separado de la siguiente por  2 líneas en blanco.

RNF-008: Formato de las cantidades de datos.
- Todas las cantidades de datos se mostrarán en formatos legibles para humanos, esto es: Tb, Gb, Mb, Kb, o B.

---

# 8. Instrucciones especificas para el agent IA.
## 8.1 Reglas de ejecución
- Antes de escribir código, lee toda la spec completa.
- Haz un commit por requisito funcional o tarea con el formato de mensaje: feat(RF-XXX): descripción.
- No improvises, si algo no está definido en la spec, detente y pregunta en lugar de asumir.

## 8.5 Criterios de "Done"
El proyecto se considerará completo cuando:
- Todos los RF marcados como "Must" estén implementados
- Todos los criterios de aceptación verificados.
- Lintern pasa sin warnings
- README actualizado con la documentación del proyecto.
