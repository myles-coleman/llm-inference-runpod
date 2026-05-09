# llm-inference-runpod

RunPod serverless GPU worker for LLM inference using [vLLM](https://github.com/vllm-project/vllm).

Defaults to [Qwen3.6-35B-A3B-AWQ](https://huggingface.co/QuantTrio/Qwen3.6-35B-A3B-AWQ) (4-bit quantized, fits on 24GB GPUs).

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_ID` | `QuantTrio/Qwen3.6-35B-A3B-AWQ` | HuggingFace model ID |
| `QUANTIZATION` | `awq` | Quantization format (`awq`, `gptq`, or empty for none) |
| `MAX_MODEL_LEN` | `8192` | Maximum sequence length |
| `GPU_MEMORY_UTILIZATION` | `0.90` | Fraction of GPU memory to use |
| `HF_TOKEN` | — | HuggingFace token for gated models |

## Request Format

```json
{
  "input": {
    "messages": [
      {"role": "user", "content": "Hello!"}
    ],
    "temperature": 0.7,
    "max_tokens": 512
  }
}
```

## Response Format

```json
{
  "choices": [
    {
      "message": {"role": "assistant", "content": "..."},
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 50,
    "total_tokens": 60
  }
}
```

## Deploy to RunPod

1. Push the image to Docker Hub (CI does this on release, or build manually):
   ```bash
   docker build -t beebecomebigbee/llm-inference-runpod:latest .
   docker push beebecomebigbee/llm-inference-runpod:latest
   ```

2. In RunPod, create a serverless endpoint:
   - **Container Image**: `beebecomebigbee/llm-inference-runpod:latest`
   - **GPU**: RTX 4090 (24GB) or equivalent
   - **Container Disk**: 20 GB
   - **Volume Disk**: 40 GB (for model cache)
   - **Volume Mount Path**: `/runpod-volume`
   - Set env var `HF_HOME=/runpod-volume/huggingface` to cache models across cold starts

3. Send requests to the endpoint URL provided by RunPod.

## Swapping Models

Override `MODEL_ID` and `QUANTIZATION` in the RunPod endpoint env vars:

```
# Gemma 3 12B (AWQ, fits 24GB)
MODEL_ID=casperhansen/gemma-3-12b-it-awq
QUANTIZATION=awq

# Qwen3.6-27B (AWQ, fits 24GB)
MODEL_ID=Qwen/Qwen3.6-27B-AWQ
QUANTIZATION=awq

# Smaller model, no quantization needed
MODEL_ID=Qwen/Qwen3.6-35B-A3B
QUANTIZATION=
```
