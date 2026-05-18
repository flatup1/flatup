#!/usr/bin/env bash
# AIKA LINE Bot の回帰テスト一括実行。
# 依存ゼロ(標準ライブラリ unittest のみ)。pytest 不要。
#
# 実行:
#   ./tests/run.sh
# または
#   cd code && python3 -m unittest discover -s tests -v

set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODE_ROOT="$(cd "$HERE/.." && pwd)"

cd "$CODE_ROOT"
exec python3 -m unittest discover -s tests "$@"
