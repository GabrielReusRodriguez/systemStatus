# RF-002: Obtener el rendimiento de la cpu.
- Descripcion: El programa ha de mostrar el uso de la cpu y los cores fisicos mediante porcentajes y con una barra de progreso hecha en ascii art. Estos datos se actualizaran en tiempo real según un parámetro temporal en segundos que informará el usuario al ejecutarlo que indicará el tiempo que tarda el programa en actualizar los datos. 
En caso que no lo informe, el tiempo entre actualizaciones será 1 segundo
- La salida tendra el siguiente formato:
```
Total CPU:    20,00%  |████████████████████
Core 01:      05,10%  |██████████████████
Core 02:      07,90%  |██████████████████
Core 03:      01,10%  |█
Core 04:      00,10%  |
Core 05:      40,10%  |████████████████████
```
- Criterios de aceptacion: 
-- Aparece un porcentaje del total de uso de la CPU.
-- Aparece un porcentaje de la carga total por core fisico.
-- Se dibuja la barra de uso para cada core fisico y para la cpu.
