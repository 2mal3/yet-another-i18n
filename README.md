# yet another i18n

A lightweight and developer-friendly Python translation library designed for simplicity and flexibility.

## Features

- 🌐 json-based translation: easy-to-use translations powered by simple JSON files.
- 🔄 fallback language support: automatically provides translations in a fallback language when a specific translation is unavailable.
- 🧩 nested values and placeholders: fully supports nested structures and dynamic placeholders within translations.
- 🎛️ flexible translation styles: offers both preconfigured translations and on-the-fly translation generation.
- 🛠️ developer experience focused api: designed with developers in mind, drawing inspiration from other projects.
- ⚡ lightweight and simple: under 150 lines of code with no dependencies beyond Python's standard library.

## Usage

### 1. Initialization

Create a `Translator` instance by specifying at least the fallback locale.

```python
from yai18n import Translator

translator = Translator(
    fallback_locale="en",
)
```

- **fallback_locale** (required): The locale to use if the requested key is not found in any other locale.
- **default_locale** (optional): The primary locale used when none is explicitly provided.
- **locale_folder_path** (optional): Directory containing your JSON locale files. (default: `"locales"`)
- **debug** (optional): If `True`, locale files are reloaded before each translation (useful for development).

### 2. Locale Files

Each locale file should be a JSON file named `<locale>.json` within the specified `locale_folder_path`. Example:

`en.json`:

```json
{
  "greeting": {
    "hello": "Hello, {name}!"
  }
}
```

### 3. Translation

To translate a key, simply call the `Translator` instance:

```python
message = translator("greeting.hello", locale="en", args={"name": "Alice"})
print(message)  # Outputs: "Hello, Alice!"
```

- **key**: A string path (e.g., `"section.subsection.key"`) to the translated text.
- **locale** (optional): Override the default locale for this translation.
- **args** (optional): A dictionary to format dynamic placeholders in the translated text.

### 4. Fallback Behavior

If a key does not exist in the requested locale, the translator automatically uses the `fallback_locale`.
If the key is not found there either, a `KeyError` is raised.

### 5. Error Handling

- **ValueError**: Raised if a requested locale or default locale is not found.
- **TypeError**: Raised if arguments to methods are of incorrect types.
- **KeyError**: Raised if a translation key cannot be found in both the given and fallback locales.
