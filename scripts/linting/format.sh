#!/bin/bash

# Go to repository root.
cd "$(dirname "$0")"
cd ../..

./scripts/linting/format_cc_file.sh

