"""Textual presentation and interaction; indexing and lookup live in independent modules."""

import asyncio
from pathlib import Path

from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.widgets import Footer, Header, Input, Static

from mini_grep.display import HELP, file_table, literal
from mini_grep.index import FileIndex, FileIndexError, build_index
from mini_grep.parser import CommandSyntaxError, parse_command
from mini_grep.search import FileAccessError, find_file


class GrepFileApp(App[None]):
    """A small filename-search TUI with manual refresh and visible snapshot status."""

    TITLE = "Mini Grep"
    SUB_TITLE = "Academic filename search"
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", priority=True),
        Binding("ctrl+r", "refresh", "Refresh", priority=True),
        Binding("f1", "help", "Help", priority=True),
    ]
    CSS = """
    #container { width: 100%; height: 1fr; padding: 0 1; }
    #status { height: auto; max-height: 5; margin-bottom: 1; }
    #help { height: auto; border: round $accent; padding: 0 1; }
    #results_scroll { height: 1fr; min-height: 3; border: round $primary; padding: 0 1; }
    #results { height: auto; }
    #results.error { color: $error; }
    #results.missing { color: $warning; }
    #command_input { margin-top: 1; }
    """

    def __init__(self, directory: Path | None = None) -> None:
        super().__init__()
        self.directory = directory if directory is not None else Path(".")
        self.index: FileIndex | None = None
        self._refreshing = False

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="container"):
            yield Static("Building index...", id="status", markup=False)
            yield Static(
                'Exact filenames: grep example.txt or grep "my file.txt"\n'
                "Commands: refresh | help | quit. F1 shows full help.",
                id="help",
                markup=False,
            )
            with VerticalScroll(id="results_scroll"):
                yield Static("Enter grep <filename> to search.", id="results", markup=False)
            yield Input(
                placeholder='grep example.txt | grep "my file.txt" | help', id="command_input"
            )
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#command_input", Input).focus()
        self.action_refresh()

    def action_refresh(self) -> None:
        if not self._refreshing:
            self._refreshing = True
            self.run_worker(self._refresh_index(), group="index")

    async def _refresh_index(self) -> None:
        command_input = self.query_one("#command_input", Input)
        command_input.disabled = True
        self.query_one("#status", Static).update(literal(f"Indexing: {self.directory}"))
        try:
            # A thread avoids blocking Textual's event loop during slow directory IO.
            new_index = await asyncio.to_thread(build_index, self.directory)
        except FileIndexError as error:
            self._show_error(str(error))
            self._update_status("Refresh failed. Previous snapshot retained.")
        else:
            # Publish only a completed snapshot; never expose a partially built index.
            self.index = new_index
            self._update_status()
            results = self.query_one("#results", Static)
            results.set_classes("")
            message = Text(f"Index refreshed: {len(new_index.entries)} files.\n", style="green")
            if new_index.warnings:
                message.append("WARNING: skipped unreadable entries:\n", style="yellow")
                for warning in new_index.warnings[:5]:
                    message.append_text(literal(f"{warning.path.name}: {warning.reason}\n"))
                if len(new_index.warnings) > 5:
                    message.append(f"...and {len(new_index.warnings) - 5} more; refresh to retry.")
            results.update(message)
        finally:
            self._refreshing = False
            command_input.disabled = False
            command_input.focus()

    def _update_status(self, message: str = "") -> None:
        if self.index is None:
            status = f"Directory: {self.directory}\nNo index available. {message}"
        else:
            status = (
                f"Directory: {self.index.directory}\n"
                f"Indexed: {len(self.index.entries)} files | Skipped: {len(self.index.warnings)} | "
                f"Last refresh (UTC): {self.index.refreshed_at:%Y-%m-%d %H:%M:%S}\n{message}"
            )
        self.query_one("#status", Static).update(literal(status.replace("\n", " | ")))

    def _show_error(self, message: str) -> None:
        results = self.query_one("#results", Static)
        results.set_classes("error")
        results.update(literal(f"ERROR: {message}"))

    def action_help(self) -> None:
        results = self.query_one("#results", Static)
        results.set_classes("")
        results.update(Text(HELP))

    def on_input_submitted(self, event: Input.Submitted) -> None:
        event.input.value = ""
        try:
            command = parse_command(event.value)
        except CommandSyntaxError as error:
            self._show_error(f"Invalid command ({error.code}): {error}")
            return
        if command.name == "quit":
            self.exit()
        elif command.name == "help":
            self.action_help()
        elif command.name == "refresh":
            self.action_refresh()
        else:
            if self._refreshing or self.index is None:
                self._show_error("Index unavailable. Wait for indexing or use refresh to retry.")
                return
            assert command.filename is not None
            try:
                entry = find_file(self.index, command.filename)
            except FileAccessError as error:
                self._show_error(str(error))
                return
            results = self.query_one("#results", Static)
            if entry is None:
                results.set_classes("missing")
                results.update(
                    literal(f"NOT FOUND: {command.filename}. Use refresh for new files.")
                )
            else:
                results.set_classes("")
                results.update(file_table(entry))
