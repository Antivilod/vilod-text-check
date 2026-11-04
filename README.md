# Vilod Text Check

A read-only UTF-8 file checker for documentation, generated text and small source files. Reports line and column numbers without copying the text into the output.

## Quick start

Python 3.10+, standard library only. Download Code > Download ZIP, extract it and open a terminal in the extracted folder.

```sh
python text_check.py example.txt
python text_check.py --max-line-length 120 example.txt
python -m unittest discover -v
```

On Windows `py` can replace `python`. The clean bundled example exits 0. Exit 1 means findings; exit 2 means an encoding, input or option error.

Checks: trailing ASCII spaces/tabs, mixed LF/CRLF/CR endings, bare CR, UTF-8 BOM, missing final newline, NUL characters, and U+2013/U+2014 long dashes. Use `--allow-long-dashes` when those punctuation characters are intentional. Optional `--max-line-length N` counts Unicode code points, not display width. Lines and columns are one-based.

A consistent CRLF file is accepted. An empty file is accepted. Reports contain counts and positions, never source text or the input path. Each file is limited to 16 MiB. At most 1000 findings are listed; `issue_count` still counts all findings and `truncated` indicates omitted details. No automatic fixes, recursive traversal or language-specific parsing.

## По-русски

Проверка текстового файла перед коммитом: лишние пробелы в конце строк, смешанные переносы, BOM, нулевые символы и длинные тире. Полезно для README и текстов, где нужен обычный короткий дефис. Длинные тире можно разрешить флагом `--allow-long-dashes`.

Файл не изменяется. В JSON-отчёте только типы замечаний и их позиции. Программа не ищет секреты и не заменяет проверку приватности. Синтетический пример лежит рядом с кодом; свои файлы храните вне репозитория.

## Version and checks

Source preview 0.1.0. Ten unit tests and CLI smoke checks passed on Linux. Windows has not been tested. No network requests, accounts or telemetry. Python source only, no EXE installer.

MIT, copyright (c) 2026 Vilod. See LICENSE and SECURITY.md.
