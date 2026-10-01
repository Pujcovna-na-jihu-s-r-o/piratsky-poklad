# Namluvení hry (Gemini TTS)

1. Klíč uložte do souboru `.env` v této složce (`GEMINI_API_KEY=...`), soubor nikam nesdílejte.
2. Hlasová zkouška: `python gemini_tts.py test` → klipy v `test/` (Pepík ve 4 hlasech, Mlha ve 3, dialog).
3. Po výběru hlasů: `python gemini_tts.py build manifest.json audio/` (manifest vygeneruje `make_manifest.py`).

Potřebuje `ffmpeg` v PATH (převod na mp3). Bez něj přidejte `--wav`.
