# llm-inference-runpod

RunPod serverless GPU worker for LLM inference using vLLM.

## Overview

Docker image that runs a vLLM-backed RunPod serverless handler. Defaults to Qwen3.6-35B-A3B (AWQ 4-bit) targeting 24GB NVIDIA GPUs (e.g. RTX 4090).

## Key Files

- `Dockerfile` — builds on `vllm/vllm-openai`, adds RunPod SDK and handler
- `src/handler.py` — RunPod serverless handler, loads vLLM engine at startup
- `.github/workflows/build.yaml` — builds and pushes Docker image on release
- `.github/workflows/release.yaml` — semantic-release for versioning

## Commands

- Build: `docker build -t llm-inference-runpod .`
- No local run without an NVIDIA GPU

## Conventions

- Conventional commits (semantic-release)
- GitHub Actions pinned to full commit SHA with version comment
- All env vars configured in Dockerfile, overridable at runtime
