import tempfile
from json import dumps
from pathlib import Path

from yai18n import Translator

import pytest


def test_working():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = Path(temp_dir, "en.json")
        with open(temp_file_path, "w") as file:
            content = {"test": "test"}
            file.write(dumps(content))

        t = Translator("en", locale_folder_path=temp_dir)
        assert t("test", "en") == "test"


def test_empty_file():
    with tempfile.TemporaryDirectory() as temp_dir:
        open(Path(temp_dir, "en.json"), "w").close()

        with open(Path(temp_dir, "es.json"), "w") as file:
            content = {"test": "test"}
            file.write(dumps(content))

        Translator("es", locale_folder_path=temp_dir)


def test_broken_file():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = Path(temp_dir, "en.json")
        with open(temp_file_path, "w") as file:
            file.write("{")

        with pytest.raises(SyntaxError):
            Translator("en", locale_folder_path=temp_dir)
