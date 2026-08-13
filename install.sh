set -eu

REPO="https://github.com/theranser/brokie.git"
INSTALL_DIR="$HOME/.local/share/brokie"
BIN="$HOME/.local/bin/brokie"

if ! command -v uv >/dev/null 2>&1; then
    echo "Error: uv is not installed or not in PATH. Please install uv first." >&2
    exit 1
fi

rm -rf "$INSTALL_DIR"
git clone "$REPO" "$INSTALL_DIR"

uv sync --project "$INSTALL_DIR"

mkdir -p "$(dirname "$BIN")"
cat >"$BIN" <<EOF
#!/bin/sh
. "$INSTALL_DIR/.venv/bin/activate"
exec uv run --quiet --project "$INSTALL_DIR" "$INSTALL_DIR/src/main.py" "\$@"
EOF
chmod +x "$BIN"

echo "Installed. Run 'brokie' to start."
