# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repo builds and publishes arm64 Docker images (no application code, no tests, no README). Each top-level directory containing a `Dockerfile` is one image, published to `ghcr.io/<owner>/<directory-name>`:

- `rocky9/` — base image (Rocky Linux 9, toolchain, ja/en locales, Asia/Tokyo TZ, `tini` as ENTRYPOINT)
- `python/` — `FROM rocky9`; Python (`PYTHON_VERSION`) + `uv` + git/ssh
- `go/` — `FROM rocky9`; Go (`GO_VERSION`) + `golangci-lint`

Comments in the Dockerfiles and workflows are written in Japanese; keep that style when editing them.

## Building locally

The images are arm64-only (Dockerfiles download `linux-arm64` / `tini-arm64` binaries). `python` and `go` take the base via `BASE_IMAGE` (default `rocky9:latest`), so build `rocky9` first:

```bash
docker build -t rocky9:latest rocky9
docker build -t python:local python        # or: go
```

There is no lint/test tooling; CI is the only check.

## CI architecture (`.github/workflows/`)

- `docker-images.yml` — triggers on PRs and pushes to `main` touching `rocky9/**`, `python/**`, `go/**`, or `.github/workflows/*.yml`. A `changes` job (dorny/paths-filter) decides what to build. PRs build only (`push: false`); `main` builds and pushes. Build order is `rocky9` → (`python`, `go`); a change in `rocky9/**` or in the workflows rebuilds all of them, and `python`/`go` still run when `rocky9` is skipped but not when it fails.
- `_build-image.yml` — reusable workflow that builds one image (input `image` = directory name). Runs on `ubuntu-24.04-arm`. With `rocky9-base: true` it passes `BASE_IMAGE=ghcr.io/<owner>/rocky9:latest`, so downstream images are built on the just-pushed base.

### Tagging

Every image gets `latest` and `sha-<commit>`. If `version-arg` is set (`PYTHON_VERSION` / `GO_VERSION`), the workflow greps `^ARG <name>=` from the Dockerfile and adds a `major.minor` tag (e.g. `go:1.27`, `python:3.14`). So the version `ARG` must stay as a plain `ARG NAME=value` line near the top-level of that Dockerfile, or the version step fails.

## Conventions when editing Dockerfiles

- Downloaded binaries/installers (tini, Go, golangci-lint, uv) are pinned by version **and** verified with a `*_SHA256` ARG via `sha256sum -c`. When bumping a version, update the matching SHA256 too (use the arm64 artifact's checksum; for `uv` it is the checksum of the installer script).
- Add a new image by creating `<name>/Dockerfile` and wiring it into both `docker-images.yml` (paths, `changes` filter + output, a job calling `_build-image.yml`) — workflow path filters are explicit per directory.

## Dev container

`.devcontainer/` contains `python` and `python-egress` configurations.
