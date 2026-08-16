#!/bin/sh
set -eu

export UV_CACHE_DIR="${UV_CACHE_DIR:-.uv-cache}"
export UV_TOOL_DIR="${UV_TOOL_DIR:-.uv-tools}"

uvx aptitude-resolver mcp --help
uvx aptitude-publisher inspect --help
uvx aptitude-publisher publish --help
