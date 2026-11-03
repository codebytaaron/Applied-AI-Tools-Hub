# kotlin-intake-builder

Kotlin CLI template that generates an intake questionnaire.

This repo is intentionally written in **Kotlin** (not Python/JS) so GitHub shows a different language mix.

## Run
```bash
kotlinc src/Main.kt -include-runtime -d app.jar
java -jar app.jar
```

## Input format
Put your notes in `input.txt` (or pipe stdin). Output is printed to stdout.
