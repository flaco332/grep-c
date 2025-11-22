import os
from datetime import datetime

from rich.table import Table
from rich.text import Text

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Static
from textual.containers import Vertical


class GrepFileApp(App):
    """Mini buscador de archivos tipo 'grep nombre.ext' en el directorio actual."""

    CSS = """
    Screen {
        align: center middle;
    }

    #container {
        width: 90%;
        height: 80%;
    }

    #help {
        height: 3;
        border: solid green;
        padding: 1 2;
    }

    #results {
        border: solid cyan;
        padding: 1 2;
        height: 1fr;
        overflow: auto;
    }

    #command_input {
        border: solid magenta;
        padding: 0 1;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.files_sorted: list[str] = []
        self.file_info: dict[str, dict] = {}

    def index_files(self) -> None:
        """Indexa los archivos del directorio actual y prepara estructuras para búsqueda binaria."""
        entries = os.listdir(".")
        files = [f for f in entries if os.path.isfile(f)]

        # Ordenamos para poder hacer búsqueda binaria
        self.files_sorted = sorted(files)

        self.file_info = {}
        for name in self.files_sorted:
            stat = os.stat(name)
            self.file_info[name] = {
                "size": stat.st_size,
                "mtime": datetime.fromtimestamp(stat.st_mtime),
                "path": os.path.abspath(name),
            }

    def binary_search(self, target: str) -> int:
        """Búsqueda binaria simple sobre self.files_sorted."""
        low, high = 0, len(self.files_sorted) - 1
        while low <= high:
            mid = (low + high) // 2
            value = self.files_sorted[mid]
            if value == target:
                return mid
            if value < target:
                low = mid + 1
            else:
                high = mid - 1
        return -1

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="container"):
            help_text = (
                "[b]Buscador de archivos (solo directorio actual)[/b]\n"
                "Escribe comandos tipo: [green]grep nombre_archivo.ext[/green]\n"
                "Ejemplo: [yellow]grep holamundo.txt[/yellow]"
            )
            yield Static(help_text, id="help")
            yield Static("Sin resultados aún.", id="results")
            yield Input(
                placeholder="Escribe: grep holamundo.txt y presiona Enter",
                id="command_input",
            )
        yield Footer()

    def on_mount(self) -> None:
        """Se ejecuta al iniciar la app."""
        self.index_files()
        # Poner el foco en el input
        self.query_one("#command_input", Input).focus()

    def render_not_found(self, filename: str) -> Table:
        table = Table(title="Resultado de búsqueda")
        table.add_column("Estado", style="red", no_wrap=True)
        table.add_column("Detalle", style="white")

        table.add_row("No encontrado", f"El archivo '{filename}' no existe en el directorio actual.")
        return table

    def render_found(self, filename: str) -> Table:
        info = self.file_info[filename]

        table = Table(title="Archivo encontrado")
        table.add_column("Campo", style="cyan", no_wrap=True)
        table.add_column("Valor", style="white")

        table.add_row("Nombre", filename)
        table.add_row("Ruta absoluta", info["path"])
        table.add_row("Tamaño (bytes)", str(info["size"]))
        table.add_row("Última modificación", info["mtime"].strftime("%Y-%m-%d %H:%M:%S"))

        return table

    def render_error(self, message: str) -> Text:
        return Text(f"Error: {message}", style="bold red")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        command = event.value.strip()
        # Limpiar input
        event.input.value = ""

        results_widget = self.query_one("#results", Static)

        # Validar comando
        if not command:
            results_widget.update(self.render_error("Comando vacío. Usa: grep archivo.ext"))
            return

        if not command.startswith("grep "):
            results_widget.update(
                self.render_error("Comando inválido. Debes usar: grep nombre_archivo.ext")
            )
            return

        filename = command[5:].strip()
        if not filename:
            results_widget.update(
                self.render_error("No especificaste el nombre del archivo después de 'grep'.")
            )
            return

        # Búsqueda binaria
        idx = self.binary_search(filename)

        if idx == -1:
            results_widget.update(self.render_not_found(filename))
        else:
            results_widget.update(self.render_found(filename))


if __name__ == "__main__":
    GrepFileApp().run()