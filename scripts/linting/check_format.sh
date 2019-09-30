
#!/bin/bash

# Go to repository root.
cd "$(dirname "$0")"
cd ../..

./lib/linting/check_cc_file.sh

