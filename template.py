"""
Day 1 — LLM API Foundation
AICB-P1: AI Practical Competency Program, Phase 1

Instructions:
    1. Fill in every section marked with TODO.
    2. Do NOT change function signatures.
    3. Copy this file to solution/solution.py when done.
    4. Run: pytest tests/ -v
"""
API_KEY = ''
from openai import OpenAI

import os
import time
from typing import Any, Callable

# ---------------------------------------------------------------------------
# Estimated costs per 1K OUTPUT tokens (USD) — update if pricing changes
# ---------------------------------------------------------------------------
COST_PER_1K_OUTPUT_TOKENS = {
    "gpt-4o": 0.010,
    "gpt-4o-mini": 0.0006,
}

OPENAI_MODEL = "gpt-4o"
OPENAI_MINI_MODEL = "gpt-4o-mini"


# ---------------------------------------------------------------------------
# Task 1 — Call GPT-4o
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API and return the response text + latency.

    Args:
        prompt:      The user message to send.
        model:       The OpenAI model to use (default: gpt-4o).
        temperature: Sampling temperature (0.0 – 2.0).
        top_p:       Nucleus sampling threshold.
        max_tokens:  Maximum number of tokens to generate.

    Returns:
        A tuple of (response_text: str, latency_seconds: float).

    Hint:
        from openai import OpenAI
        client = OpenAI(api_key=")
    """
    # TODO: import OpenAI, create client, call chat.completions.create,
    #       measure start/end time, return (response_text, latency)
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1", 
        api_key=API_KEY, 
    )
    start_time = time.time()

        
    response = client.chat.completions.create(
    model=OPENAI_MODEL,
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=temperature,
    top_p=top_p,
    max_tokens=max_tokens,
    )
    end_time = time.time()
    latency = end_time - start_time

    # 5. Trích xuất câu trả lời từ cấu trúc JSON trả về
    response_text = response.choices[0].message.content

    # 6. Trả về đúng định dạng tuple
    return response_text, latency




# ---------------------------------------------------------------------------
# Task 2 — Call GPT-4o-mini
# ---------------------------------------------------------------------------
def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API using gpt-4o-mini and return the
    response text + latency.

    Args:
        prompt:      The user message to send.
        temperature: Sampling temperature (0.0 – 2.0).
        top_p:       Nucleus sampling threshold.
        max_tokens:  Maximum number of tokens to generate.

    Returns:
        A tuple of (response_text: str, latency_seconds: float).

    Hint:
        Reuse call_openai() by passing model=OPENAI_MINI_MODEL.
    """
    # TODO: call call_openai with model=OPENAI_MINI_MODEL
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1", 
    api_key=API_KEY, 
    )
    start_time = time.time()

        
    response = client.chat.completions.create(
    model=OPENAI_MINI_MODEL,
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=temperature,
    top_p=top_p,
    max_tokens=max_tokens,
    )
    end_time = time.time()
    latency = end_time - start_time

    response_text = response.choices[0].message.content

    return response_text, latency


# ---------------------------------------------------------------------------
# Task 3 — Compare GPT-4o vs GPT-4o-mini
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:
    """
    Call both gpt-4o and gpt-4o-mini with the same prompt and return a
    comparison dictionary.

    Args:
        prompt: The user message to send to both models.

    Returns:
        A dict with keys:
            - "gpt4o_response":      str
            - "mini_response":       str
            - "gpt4o_latency":       float
            - "mini_latency":        float
            - "gpt4o_cost_estimate": float  (estimated USD for the response)

    Hint:
        Cost estimate = (len(response.split()) / 0.75) / 1000 * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]
        (0.75 words ≈ 1 token is a rough approximation)
    """
    # TODO: call call_openai and call_openai_mini, assemble and return the dict
    gpto4_response, gpt4o_latency = call_openai(prompt)
    mini_response, mini_latency = call_openai_mini(prompt)
    gpto4_cost_estimate = (len(gpto4_response.split()) / 0.75) / 1000 * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]
    return {
            "gpt4o_response": gpto4_response,
            "mini_response": mini_response,
            "gpt4o_latency": gpt4o_latency,
            "mini_latency": mini_latency,
            "gpt4o_cost_estimate": gpto4_cost_estimate
        }


def streaming_chatbot() -> None:
    """
    Run an interactive streaming chatbot in the terminal.

    Behaviour:
        - Streams tokens from OpenAI as they arrive (print each chunk).
        - Maintains the last 3 conversation turns in history.
        - Typing 'quit' or 'exit' ends the loop.

    Hints:
        - Keep a list `history` of {"role": ..., "content": ...} dicts.
        - Use stream=True in client.chat.completions.create() and iterate:
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                print(delta, end="", flush=True)
        - After each turn, append the assistant reply to history.
        - Trim history to the last 3 turns: history = history[-3:]
    """
    # Khởi tạo client 
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=API_KEY
    )
    
    # Keep a list `history` of {"role": ..., "content": ...} dicts.
    history = []
    
    # enter while-loop
    while True:
        # read user input
        user_input = input("You: ")
        
        # Typing 'quit' or 'exit' ends the loop.
        if user_input.lower() in ['quit', 'exit']:
            break
            
        history.append({"role": "user", "content": user_input})
        
        # Use stream=True in client.chat.completions.create()
        stream = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=history,
            stream=True
        )
        
        assistant_reply = ""
        print("Assistant: ", end="")
        
        # iterate for chunk in stream
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            print(delta, end="", flush=True)
            assistant_reply += delta
            
        print() # Xuống dòng cho đẹp sau khi stream xong
        
        # After each turn, append the assistant reply to history.
        history.append({"role": "assistant", "content": assistant_reply})
        
        # Trim history to the last 3 turns: history = history[-3:]
        history = history[-3:]


# ---------------------------------------------------------------------------
# Bonus Task A — Retry with backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    """
    Call fn(). If it raises an exception, retry up to max_retries times
    with exponential backoff (base_delay * 2^attempt).
    """
    attempt = 0
    while True:
        try:
            return fn()
        except Exception as e:
            if attempt >= max_retries:
                raise e
            
            # Tính toán thời gian chờ theo công thức Exponential Backoff
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)
            
            # Tăng biến đếm số lần thử
            attempt += 1


# ---------------------------------------------------------------------------
# Bonus Task B — Batch compare
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:
    """
    Run compare_models on each prompt in the list.
    """
    results = []
    
    # Duyệt qua từng câu prompt trong danh sách
    for prompt in prompts:
        # Gọi hàm compare_models (chắc chắn rằng bạn đã định nghĩa nó ở trên)
        result_dict = compare_models(prompt)
        
        # Thêm key "prompt" chứa câu hỏi gốc vào dictionary
        result_dict["prompt"] = prompt
        
        # Đưa vào danh sách kết quả tổng
        results.append(result_dict)
        
    return results


# ---------------------------------------------------------------------------
# Bonus Task C — Format comparison table
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:
    """
    Format a list of compare_models results as a readable text table.
    """
    def truncate(text: str, max_len: int = 40) -> str:
        if not text: return "".ljust(max_len)
        clean_text = text.replace("\n", " ").strip()
        if len(clean_text) > max_len:
            clean_text = clean_text[:max_len - 3] + "..."
        return clean_text.ljust(max_len)

    headers = (
        f"{'Prompt'.ljust(40)} | "
        f"{'GPT-4o Response'.ljust(40)} | "
        f"{'Mini Response'.ljust(40)} | "
        f"{'GPT-4o Latency'.ljust(15)} | "
        f"{'Mini Latency'.ljust(15)}"
    )
    
    separator = "-" * len(headers)
    table_rows = [headers, separator]

    for res in results:
        prompt = truncate(res.get("prompt", ""))
        gpt4o_resp = truncate(res.get("gpt4o_response", ""))
        mini_resp = truncate(res.get("mini_response", ""))
        
        gpt4o_lat = f"{res.get('gpt4o_latency', 0):.2f}s".ljust(15)
        mini_lat = f"{res.get('mini_latency', 0):.2f}s".ljust(15)
        
        row_string = f"{prompt} | {gpt4o_resp} | {mini_resp} | {gpt4o_lat} | {mini_lat}"
        table_rows.append(row_string)

    return "\n".join(table_rows)
# ---------------------------------------------------------------------------
# Entry point for manual testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_prompt = "Explain the difference between temperature and top_p in one sentence."
    print("=== Comparing models ===")
    result = compare_models(test_prompt)
    for key, value in result.items():
        print(f"{key}: {value}")

    print("\n=== Starting chatbot (type 'quit' to exit) ===")
    streaming_chatbot()
