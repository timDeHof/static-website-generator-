#!/bin/bash

# Build the site with the production base path
python3 src/main.py "/static-website-generator-/"

# Print success message
echo "Site built successfully with production base path!"