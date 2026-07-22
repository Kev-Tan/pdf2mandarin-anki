# Code review

## Scope and verification

Reviewed every tracked source and project/documentation file. I also ran the supplied
command against `EP1.pdf`.

* `uv run .\main.py --pdf_path "D:\Personal\Mandarin\自然而然説中文\EP1.pdf"` fails on this Windows host with `UnicodeEncodeError` while printing the first Chinese word.
* With `PYTHONIOENCODING=utf-8`, the same command completes and produces the JSON output.
* `uv run python -m compileall -q .` completed successfully (excluding virtual-environment/cache directories).

## Findings

### High — default Windows invocation crashes on ordinary Chinese output

**Location:** `main.py:24`

The requested command fails before it writes output when the active Windows console uses
the common `cp1252` encoding: `print(word)` cannot encode Chinese characters. This makes
the documented CLI unusable in that environment.

Set or document a UTF-8 console encoding (for example `sys.stdout.reconfigure(encoding="utf-8")`
when supported, or `PYTHONIOENCODING=utf-8`), and avoid printing the full result data as
the normal execution path.

### High — sentence splitting has corrupted Chinese punctuation literals

**Location:** `tools/misc.py:21`

The regular expression contains mojibake (`ã€‚ï¼ï¼Ÿ`) rather than `。！？`.
Consequently it does not split at Chinese sentence-ending punctuation. Extracted pages can
therefore be treated as one oversized “sentence”, causing inaccurate word/sentence pairs
and unnecessarily large output records. Use an ASCII-only source representation such as
`r'(?<=[\u3002\uff01\uff1f.!?])'` and add a unit test with Chinese punctuation.

### Medium — extracted value differs from the value that was validated

**Location:** `tools/extract_words.py:18-21`

The code strips a highlight into `word` and validates that normalized value, but appends
the original `h['text']`. A highlight such as `"\n中文."` passes validation but later
matches using its newline and period, often returning no sentence and emitting a dirty
`word` in JSON. Append `word` (and normalize the desired Chinese punctuation/whitespace)
instead.

### Medium — PDF handle is not reliably closed

**Location:** `tools/misc.py:15-33`

`pymupdf.open()` is not used as a context manager and `doc.close()` is never called. On
Windows, repeated processing can retain file handles and prevent the source PDF from being
renamed or deleted. Wrap it in `with pymupdf.open(pdf_path) as doc:`.

### Medium — output is silently overwritten and depends on the current directory

**Location:** `main.py:35-36`

Every run replaces `word_sentence_pairs.json` in whichever directory launched the command.
This can silently destroy a previous run and makes automation unpredictable. Add an
`--output` argument, refuse overwrite by default (or require an explicit `--overwrite`),
and write relative to a deliberate output path.

### Medium — CLI input errors are not validated at the boundary

**Location:** `main.py:15, 18-19`

`--pdf_path` is optional even though both processing functions require it. Omitting it
causes a lower-level exception rather than a useful argparse error; nonexistent/unreadable
PDFs likewise surface as raw library errors. Mark the argument `required=True`, validate
that it is a readable PDF path, and report errors cleanly.

### Medium — dormant Tatoeba request can hang and defeats its async API

**Location:** `tools/generate_sample_sentences.py:5-28`

The coroutine uses blocking `requests.get()` with no timeout. If it is integrated as its
name and documentation imply, a slow/unresponsive API can block the entire async event loop
indefinitely. Use a synchronous function, or an async HTTP client; in either case set
connect/read timeouts and handle `requests.RequestException` and invalid JSON explicitly.

### Medium — Tatoeba audio ID is taken from the wrong result and output path is machine-specific

**Location:** `tools/generate_sample_sentences.py:13-20`

When the matching sentence is not the first API record, the code assigns
`res["data"][0]["id"]`, not `potential_sentence["id"]`. It would associate generated
audio with the wrong sentence. The `D:/Personal/...` path also prevents use on another
machine or project location. Use the matching record’s ID and inject/configure an output
directory. (The function currently computes this path but never uses it.)

### Low — no automated tests protect parsing or CLI behavior

**Locations:** project-wide

There are no tests. The punctuation encoding regression and the normalization mismatch
would both be caught by focused unit tests. Add tests for highlight normalization,
Chinese/ASCII sentence boundaries, duplicate/sub-string matching policy, PDF-open failure,
and an end-to-end CLI test using a temporary output file.

### Low — dependency and import hygiene obscures the actual runtime surface

**Locations:** `main.py:3-9`; `tools/extract_words.py:1-8`; `pyproject.toml`

Several imports are unused (`asyncio`, `PdfReader`, `re`, `pymupdf`, `is_chinese_sentence`,
and most imports in `extract_words.py`). `generate_audio`, `jieba`, `genanki`, and
potentially `nltk` are not wired into the current command. Remove unused imports and either
remove unused dependencies or implement the advertised features. Also populate the empty
`README.md` or make `overview.md` the project's declared readme.

## Suggested remediation order

1. Fix the encoded sentence-boundary regex, normalize the appended highlight, and add tests.
2. Make CLI encoding, argument validation, and output-path handling robust.
3. Close the PDF explicitly and reconcile the local-PDF versus Tatoeba workflow.
4. If Tatoeba/audio remain in scope, make network handling reliable and paths portable.
