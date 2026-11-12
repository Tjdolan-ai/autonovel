# Run an autonovel tool with UTF-8 file handling (your chapters use curly quotes and em dashes).
# Usage:  .\run.ps1 evaluate.py --chapter 11
$env:PYTHONUTF8 = "1"
uv run python @args
