from pathlib import Path
from json import loads, decoder

from typing import Optional, Union


class Translator:
    def __init__(
        self,
        fallback_locale: str,
        default_locale: Optional[str] = None,
        locale_folder_path: Union[Path, str] = Path("locales"),
        debug: bool = False,
    ) -> None:
        """
        Args:
            fallback_locale (str): The locale to fallback to a key is not found in the provided locale
            default_locale (str, optional): The default locale to use if no locale is provided. Defaults to None.
            locale_folder_path (Path, optional): The path to the directory containing the locale files. Defaults to "locales").
            debug (bool, optional): Enable debug mode which reloads the provided locales on each translation. Defaults to False.

        """

        # Check if the user has input arguments of the wrong type to prevent
        # possible type errors and directly show the user if he has done something wrong
        if type(fallback_locale) is not str:
            raise TypeError("fallback_locale must be a string")

        if default_locale and type(default_locale) is not str:
            raise TypeError("default_locale must be a string")

        if type(debug) is not bool:
            raise TypeError("debug must be a boolean")

        if not isinstance(locale_folder_path, Path) and type(locale_folder_path) is not str:
            raise TypeError("locale_folder_path must be a Path or a string")
        locale_folder_path = locale_folder_path if type(locale_folder_path) is Path else Path(locale_folder_path)
        if not locale_folder_path.is_dir():
            raise TypeError("locale_folder_path must be a folder")

        if debug:
            print("Running Yet Another i18n in debug mode, please disable it in production")

        self.locale_folder_path = locale_folder_path
        self.debug = debug
        self.default_locale = default_locale
        self.fallback_locale = fallback_locale

        self.locales = {}
        self._load_files()

        if default_locale and default_locale not in self.locales:
            raise ValueError(
                f"Default locale '{default_locale}' not found in locales ({', '.join(self.locales.keys())})"
            )
        if fallback_locale not in self.locales:
            raise ValueError(
                f"Fallback locale '{fallback_locale}' not found in locales ({', '.join(self.locales.keys())})"
            )

    def _load_files(self):
        json_files = self.locale_folder_path.glob("*.json")

        for json_file in json_files:
            with open(json_file, "r") as file:
                content = file.read()

                # Skip empty files without rising an error
                if len(content) == 0:
                    continue

                try:
                    data = loads(content)
                except decoder.JSONDecodeError as error:
                    raise SyntaxError(f"Cannot read json file {json_file}: {error}")
                self.locales[json_file.stem] = data

        if self.locales == {}:
            raise FileNotFoundError(f"Could not find any valid json files in '{self.locale_folder_path.absolute()}'")

    def __call__(self, key: str, locale: Optional[str] = None, args: dict = {}) -> str:
        """
        Translate a key to a string based on the provided locale.

        Args:
            key (str): The key to translate
            locale (str, optional): The locale to use. Overrides default locale. Uses default locale if not provided. Defaults to None.
            args (dict, optional): Arguments to replace dynamic placeholders in the translated string. Defaults to {}.

        Returns:
            str: The translated string of the key. If key is not found in the provided locale, it will fallback to the fallback locale.

        Raises:
            ValueError: If locale is provided but not found in locales
            ValueError: If no locale is provided and no default locale is set
            KeyError: If key is not found in the provided locale and the fallback locale
        """

        if type(args) is not dict:
            raise TypeError("args must be a dictionary")
        if locale and type(locale) is not str:
            raise TypeError("locale must be a string")
        if type(key) is not str:
            raise TypeError("key must be a string")

        if self.debug:
            self._load_files()

        if locale:
            if locale not in self.locales:
                raise ValueError(f"Locale '{locale}' not found in locales ({', '.join(self.locales.keys())})")
        else:  # probably intent to use default locale
            if not self.default_locale:
                raise ValueError("No locale provided and no default locale set")
            locale = self.default_locale

        try:
            template = self._get_template_from_key(key, locale)
        except KeyError:
            locale = self.fallback_locale

            try:
                template = self._get_template_from_key(key, locale)
            except KeyError:
                raise KeyError(f"Key '{key}' not found in fallback locale '{locale}'")
        try:
            translation = template.format(**args)
        except KeyError as e:
            raise KeyError(f"Missing required translation argument: {e}")

        return translation

    def _get_template_from_key(self, key_path: str, locale: str) -> str:
        keys = key_path.split(".")

        final_key = self.locales[locale]
        for key in keys:
            final_key = final_key[key]

        return final_key
