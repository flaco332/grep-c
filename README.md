# Mini GREP en C — Buscador de patrones en archivos `.txt`

Este proyecto implementa una herramienta tipo **grep simplificado**, desarrollada en lenguaje **C** para la materia de *Estructuras de Datos*.  
El programa busca un patrón dentro de todos los archivos `.txt` del **directorio actual** (búsqueda no recursiva) y almacena las coincidencias en una **lista enlazada**.

-----------------------------------------------------------------------------------------------------------

## Características principales

- Búsqueda de coincidencias dentro de archivos `.txt`.
- No recorre subdirectorios (no recursivo).
- Manejo de archivos mediante `dirent.h`.
- Coincidencias almacenadas en una **lista enlazada**.
- Registro por coincidencia:
  - Archivo
  - Número de línea
  - Columna donde inicia el patrón
  - Texto completo de la línea
- Menú interactivo por consola.
- Posibilidad de extender a:
  - Eliminación de archivos con coincidencias
  - Exportación de resultados
  - Búsquedas recursivas

-----------------------------------------------------------------------------------------------------------

## Estructura del proyecto

grep-c/
│── README.md
│── Makefile
│
├── src/
│ ├── main.c
│ ├── search.c
│ ├── search.h
│ ├── list.c
│ └── list.h
│
├── docs/
│ └── reporte.md
│
└── data/
└── (archivos .txt para pruebas)

-----------------------------------------------------------------------------------------------------------

Compilar desde terminal:

```bash
make

gcc src/main.c src/search.c src/list.c -o mini_grep

./mini_grep

