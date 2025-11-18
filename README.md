# Mini GREP TUI en Python — Buscador interactivo de archivos

Aplicación ligera construida con [Textual](https://github.com/Textualize/textual) que emula un `grep nombre.ext` sobre **el directorio actual** y muestra los resultados en una interfaz de terminal enriquecida.

-----------------------------------------------------------------------------------------------------------

## Características

- Índice de todos los archivos del directorio actual (sin entrar en subdirectorios).
- Uso de **búsqueda binaria** para localizar rápidamente el archivo solicitado.
- Interfaz TUI con panel de ayuda, tabla de resultados y validación inmediata del comando.
- Información detallada del archivo encontrado:
  - Ruta absoluta
  - Tamaño en bytes
  - Fecha de última modificación
- Mensajes claros cuando el archivo no existe o el comando es inválido.

-----------------------------------------------------------------------------------------------------------

## Requisitos

- Python 3.9 o superior.
- Dependencias: `textual` (incluye `rich`).

Instalación rápida (opcionalmente dentro de un entorno virtual):

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install textual
```

-----------------------------------------------------------------------------------------------------------

## Uso

1. Asegúrate de estar en el directorio que deseas inspeccionar.
2. Ejecuta la aplicación:

```bash
python grep_tui.py
```

3. En el campo de entrada escribe comandos del tipo:
   - `grep archivo.txt`
   - `grep reporte.pdf`

Solo se consideran los archivos que estén en el mismo directorio desde donde corriste el programa.

-----------------------------------------------------------------------------------------------------------

## Estructura

```
grep-c/
├── README.md
└── grep_tui.py
```

`grep_tui.py` contiene toda la lógica de indexación, búsqueda binaria y renderizado de la interfaz con Textual.

-----------------------------------------------------------------------------------------------------------

## Próximos pasos sugeridos

- Agregar filtros por extensión o patrones parciales.
- Integrar búsquedas recursivas opcionales.
- Mostrar metadatos adicionales (propietario, permisos).
- Empaquetar como aplicación ejecutable (`pyinstaller`, `textual build`, etc.).
