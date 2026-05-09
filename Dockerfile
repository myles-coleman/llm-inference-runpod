FROM vllm/vllm-openai:latest

RUN pip install --no-cache-dir runpod

COPY src/ /app/src/

ENV MODEL_ID="QuantTrio/Qwen3.6-35B-A3B-AWQ" \
    QUANTIZATION="awq" \
    MAX_MODEL_LEN="8192" \
    GPU_MEMORY_UTILIZATION="0.90"

CMD ["python3", "/app/src/handler.py"]
