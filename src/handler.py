import os

import runpod
from vllm import LLM, SamplingParams

MODEL_ID = os.environ.get("MODEL_ID", "QuantTrio/Qwen3.6-35B-A3B-AWQ")
MAX_MODEL_LEN = int(os.environ.get("MAX_MODEL_LEN", "8192"))
GPU_MEMORY_UTILIZATION = float(os.environ.get("GPU_MEMORY_UTILIZATION", "0.90"))

engine_kwargs = {
    "model": MODEL_ID,
    "max_model_len": MAX_MODEL_LEN,
    "gpu_memory_utilization": GPU_MEMORY_UTILIZATION,
    "trust_remote_code": True,
}

quantization = os.environ.get("QUANTIZATION")
if quantization:
    engine_kwargs["quantization"] = quantization

llm = LLM(**engine_kwargs)


def handler(job):
    job_input = job["input"]

    sampling_params = SamplingParams(
        temperature=job_input.get("temperature", 0.7),
        top_p=job_input.get("top_p", 0.9),
        max_tokens=job_input.get("max_tokens", 512),
        stop=job_input.get("stop"),
    )

    outputs = llm.chat(job_input["messages"], sampling_params=sampling_params)
    result = outputs[0]

    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": result.outputs[0].text,
                },
                "finish_reason": result.outputs[0].finish_reason,
            }
        ],
        "usage": {
            "prompt_tokens": len(result.prompt_token_ids),
            "completion_tokens": len(result.outputs[0].token_ids),
            "total_tokens": len(result.prompt_token_ids)
            + len(result.outputs[0].token_ids),
        },
    }


runpod.serverless.start({"handler": handler})
