FROM vllm/vllm-openai:latest

ENV MODEL_ID="QuantTrio/Qwen3.6-35B-A3B-AWQ" \
    QUANTIZATION="awq" \
    MAX_MODEL_LEN="8192" \
    GPU_MEMORY_UTILIZATION="0.90"

ENTRYPOINT ["python3", "-m", "vllm.entrypoints.openai.api_server"]
CMD ["--model", "QuantTrio/Qwen3.6-35B-A3B-AWQ", \
     "--quantization", "awq", \
     "--max-model-len", "8192", \
     "--gpu-memory-utilization", "0.90", \
     "--host", "0.0.0.0", \
     "--port", "8000"]
