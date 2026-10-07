import asyncio

from rich.console import Console
from textual.widgets import Input, Static

from mini_grep.app import GrepFileApp
from mini_grep.index import FileIndexError


def result_text(app):
    console = Console(width=100, color_system=None)
    with console.capture() as capture:
        console.print(app.query_one("#results", Static).content)
    return capture.get()


async def ready(app, pilot):
    await app.workers.wait_for_complete()
    await pilot.pause()


def test_startup_input_found_missing_and_invalid(tmp_path):
    (tmp_path / "demo.txt").write_text("data", encoding="utf-8")

    async def scenario():
        app = GrepFileApp(tmp_path)
        async with app.run_test(size=(80, 24)) as pilot:
            await ready(app, pilot)
            assert app.index.names == ("demo.txt",)
            command_input = app.query_one("#command_input", Input)
            assert command_input.has_focus
            assert command_input.region.bottom <= 24
            await pilot.press(*"grep demo.txt", "enter")
            assert "FOUND" in result_text(app)
            assert "demo.txt" in result_text(app)
            assert command_input.value == ""
            command_input.value = "grep missing.txt"
            await pilot.press("enter")
            assert "NOT FOUND" in result_text(app)
            command_input.value = "grep"
            await pilot.press("enter")
            assert "missing_argument" in result_text(app)
            assert app.query_one("#results", Static).has_class("error")

    asyncio.run(scenario())


def test_refresh_help_and_quit_shortcuts(tmp_path):
    async def scenario():
        app = GrepFileApp(tmp_path)
        async with app.run_test() as pilot:
            await ready(app, pilot)
            (tmp_path / "new.txt").touch()
            await pilot.press("ctrl+r")
            await ready(app, pilot)
            assert app.index.names == ("new.txt",)
            await pilot.press("f1")
            assert "refresh" in result_text(app)
            await pilot.press("ctrl+q")

    asyncio.run(scenario())


def test_command_refresh_and_failed_refresh_keep_snapshot(tmp_path, monkeypatch):
    (tmp_path / "existing.txt").touch()

    async def scenario():
        app = GrepFileApp(tmp_path)
        async with app.run_test() as pilot:
            await ready(app, pilot)
            old_index = app.index

            def deny_index(directory):
                raise FileIndexError("access denied")

            monkeypatch.setattr("mini_grep.app.build_index", deny_index)
            app.query_one("#command_input", Input).value = "refresh"
            await pilot.press("enter")
            await ready(app, pilot)
            assert app.index is old_index
            assert "access denied" in result_text(app)
            assert not app.query_one("#command_input", Input).disabled
            app.query_one("#command_input", Input).value = "help"
            await pilot.press("enter")
            assert "grep <filename>" in result_text(app)
            app.query_one("#command_input", Input).value = "quit"
            await pilot.press("enter")

    asyncio.run(scenario())


def test_missing_directory_is_recoverable(tmp_path):
    async def scenario():
        directory = tmp_path / "missing"
        app = GrepFileApp(directory)
        async with app.run_test() as pilot:
            await ready(app, pilot)
            assert app.index is None
            assert "Cannot index" in result_text(app)
            directory.mkdir()
            await pilot.press("ctrl+r")
            await ready(app, pilot)
            assert app.index is not None

    asyncio.run(scenario())


def test_stale_file_and_literal_filename(tmp_path):
    path = tmp_path / "[red]report.txt"
    path.touch()

    async def scenario():
        app = GrepFileApp(tmp_path)
        async with app.run_test() as pilot:
            await ready(app, pilot)
            command_input = app.query_one("#command_input", Input)
            command_input.value = f"grep {path.name}"
            await pilot.press("enter")
            assert "[red]report.txt" in result_text(app)
            path.unlink()
            command_input.value = f"grep {path.name}"
            await pilot.press("enter")
            assert "Refresh" in result_text(app)
            assert app.query_one("#results", Static).has_class("error")

    asyncio.run(scenario())


def test_entry_warnings_are_visible(tmp_path, monkeypatch):
    from mini_grep.index import IndexWarning, build_index

    index = build_index(tmp_path)

    def partial_index(directory):
        from dataclasses import replace

        return replace(index, warnings=(IndexWarning(tmp_path / "locked.txt", "access denied"),))

    monkeypatch.setattr("mini_grep.app.build_index", partial_index)

    async def scenario():
        app = GrepFileApp(tmp_path)
        async with app.run_test() as pilot:
            await ready(app, pilot)
            assert "WARNING" in result_text(app)
            assert "locked.txt" in result_text(app)
            assert "access denied" in result_text(app)

    asyncio.run(scenario())
