#!/bin/bash
poetry run lint || exit 1
poetry run test || exit 1
echo "Pre-push checks passed."
