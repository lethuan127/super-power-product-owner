#!/bin/bash
# Copies the Vietnamese project, then adds a feedback line with no issue link,
# as an older plugin version wrote it.
set -e
F="$(cd "$(dirname "$0")/../_fixtures" && pwd)"
cp -R "$F/project-vi/." .
printf '\n## [2026-11-14] feedback | Góp ý plugin write-guide: gợi ý lỗi hay gặp khi thiếu thông tin\n' >> log.md
