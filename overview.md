# python-extract overview

`python-extract` is an early-stage Mandarin study-data utility. It reads highlighted text from a PDF, keeps short strings made entirely of Chinese characters, and searches Tatoeba for a Mandarin example sentence containing each extracted word. The intended workflow is to turn vocabulary highlighted while reading into material that can later be used for study cards and audio.

## Current workflow

```text
Highlighted PDF -> tools/extract_words.py -> short Chinese highlights
                -> tools/generate_sample_sentences.py -> Tatoeba sentence search
```

Run the command-line entry point with a PDF path:

```powershell
uv run python main.py --pdf_path "C:\path\to\highlights.pdf"
```

The program prints each extracted word, then prints one matching sentence when Tatoeba returns one. At the end, it prints the extracted-word count and list.

## Setup

The project targets Python 3.13, as recorded in `.python-version`, and uses [uv](https://docs.astral.sh/uv/) for dependency management.

1. Install Python 3.13 and uv.
2. From the project root, install the locked dependencies:

   ```powershell
   uv sync
   ```

3. Run the program with the command above.

`uv sync` creates or updates the local `.venv` environment from `pyproject.toml` and `uv.lock`. An internet connection is required when searching Tatoeba.

## Project layout

| Path | Responsibility |
| --- | --- |
| `main.py` | Parses `--pdf_path`, coordinates extraction and sentence lookup, and writes results to standard output. |
| `tools/extract_words.py` | Reads PDF highlights and filters them into candidate Chinese words. |
| `tools/generate_sample_sentences.py` | Searches the Tatoeba API for an example sentence containing a word. |
| `tools/generate_audio.py` | Provides an asynchronous Azure/Edge TTS helper for Taiwanese Mandarin MP3 files. |
| `pyproject.toml` | Declares Python version and package dependencies. |
| `uv.lock` | Pins the exact dependency versions used by uv. |

## Tools code

### `tools/extract_words.py`

`extract_words(args)` calls `pdf_highlight_extractor.reader.extract_highlights` with `args.pdf_path`. That library returns the text associated with each PDF highlight. The function examines every highlight and:

1. Removes leading/trailing newlines and periods for the filtering check.
2. Keeps it only if it is fewer than 10 characters long.
3. Keeps it only if `is_chinese()` confirms every character is in the CJK Unified Ideographs range (`U+4E00` to `U+9FFF`).

It returns a list of the original highlighted text values. A value that passes after trimming is therefore added in its original, untrimmed form. The module currently imports `pymupdf`, `jieba`, `requests`, `edge_tts`, and `Path`, but does not use them.

### `tools/generate_sample_sentences.py`

`retrieve_sample_sentences(word)` is an asynchronous function that builds a Tatoeba API request for Mandarin (`lang=cmn`). It URL-encodes the word, requests up to 25 relevance-sorted results, and scans the returned `data` list. It prints and returns the first sentence whose text contains the word; it returns `False` when no returned sentence contains it. HTTP errors and unexpected response shapes are printed rather than raised.

`main.py` calls this coroutine once per extracted word with `asyncio.run()`. Although this module imports `generate_audio`, it does not currently call it.

### `tools/generate_audio.py`

`generate_audio(text, destination_path, rate="-15%")` is an async helper that creates the destination directory if needed, then uses `edge_tts` to save an MP3. It uses the `zh-TW-YunJheNeural` Taiwanese Mandarin voice at a speech rate 15% below normal by default. Call and await it from an async workflow, for example after selecting a sentence.

## Current limitations and implementation notes

- The extractor only considers PDF **highlights**; ordinary PDF text is not extracted.
- Only contiguous Chinese characters are accepted. Punctuation, Latin letters, digits, and Chinese text outside the selected Unicode range cause a highlight to be excluded.
- Duplicate highlights are retained and no vocabulary normalization or segmentation is performed.
- Sentence retrieval is sequential and uses blocking `requests` inside an async function, which can be slow for many words.
- The sentence-search code computes an audio filename using the first returned Tatoeba record's ID, but does not create the file; this is a remnant of the planned audio-generation step.
- The project declares `genanki`, but card generation has not yet been wired into the code.

## Dependencies

The runtime dependencies are `pdf-highlight-extractor` for highlight reading, `edge-tts` for speech generation, `requests` for Tatoeba requests, and `genanki` for future Anki export work. `pymupdf` and `jieba` are also declared, though they are not used by the current implementation.
