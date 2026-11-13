#!/bin/bash
# Copies the shared fixtures into the run's workspace (the current folder).
set -e
F="$(cd "$(dirname "$0")/../_fixtures" && pwd)"
cp -R "$F/project-vi/." .
