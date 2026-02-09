import sys

from ollama_client import OllamaClient

from config import OllamaConfig
from logger import logger


def invoke(prompt: str, model: str = "qwen3:8b") -> str:
    config = OllamaConfig(non_thinking_model=model)
    client = OllamaClient(
        model=config.non_thinking_model,
        base_url=config.base_url,
        timeout=config.timeout
    )
    response = client.chat(
        messages=[{"role": "user", "content": prompt}],
        temperature=config.temperature,
        top_p=config.top_p
    )
    return response["message"]["content"]


def optimize_with_judge_rules(current_prompt, failed_response, judge_prompt):
    optimizer_prompt = f"""
    【角色】你是一位顶级的提示词工程师。
    【背景】我有一个"生成提示词"，但它生成的回答未能通过"AI裁判"的审核。

    【生成提示词】
    ---
    {current_prompt}
    ---

    【它生成的失败回答】
    ---
    {failed_response}
    ---

    【AI裁判的规则书 (它失败的原因)】
    ---
    {judge_prompt}
    ---

    【任务】
    请仔细研究"AI裁判的规则书"，并重写"生成提示词"，确保新提示词能生成一个可以通过该规则审核的回答。

    【要求】
    请只返回优化后的新版"生成提示词"，不要包含任何其他说明或解释。
    """
    return invoke(optimizer_prompt)


def run_ai_judge_optimization(initial_prompt, retrieved_text, final_judge_prompt, max_iterations=5):
    current_generating_prompt = initial_prompt

    print("\n" + "=" * 30)
    print("开始最终的、由AI裁判驱动的自动化优化流程")
    print("=" * 30 + "\n")

    for i in range(max_iterations):
        print(f"--- 最终流程：第 {i+1} 轮迭代 ---")

        prompt_for_generator = current_generating_prompt.format(retrieved_text=retrieved_text)
        generated_response = invoke(prompt_for_generator)

        print(f"生成的回答:\n---\n{generated_response}\n---")

        judge_prompt_filled = final_judge_prompt.format(response_to_judge=generated_response)
        judgment = invoke(judge_prompt_filled)

        judgment_cleaned = judgment.strip().replace("。", "")
        print(f"AI裁判的判决: {judgment_cleaned}")

        if judgment_cleaned == "通过":
            print("\n✅ 优化成功！生成的回答已通过AI裁判的审核。")
            break
        else:
            print("❌ 未通过审核，正在根据裁判的规则进行优化...")
            current_generating_prompt = optimize_with_judge_rules(
                current_generating_prompt,
                generated_response,
                final_judge_prompt
            )
            print("-" * 20 + "\n")
    else:
        print("\n达到最大迭代次数，停止优化。")

    print("\n" + "=" * 30)
    print("最终采纳的生成提示词：")
    print("=" * 30)
    print(current_generating_prompt)

    return current_generating_prompt


if __name__ == "__main__":
    retrieved_text = """
    关于公司的福利政策，我们提供全面的健康保险，覆盖员工及其直系家属。
    年度体检是标配。此外，每年有15天的带薪年假，以及5天的带薪病假。
    我们还提供每月500元的交通补贴和300元的餐饮补贴。
    为了鼓励员工成长，公司设有每年高达8000元的教育培训基金，员工可以申请用于课程学习或购买专业书籍。
    健身方面，公司与多家健身房有合作，员工可享受折扣价。
    """

    initial_prompt = """
    根据以下信息，回答新员工关于公司福利的问题。

    【参考信息】
    {retrieved_text}
    """

    final_judge_prompt = """
    【角色】你是一位追求极致员工体验的内部沟通专家，眼光苛刻。
    【任务】严格判断【待评估的回答】是否合格。
    【评判标准】
    1.  **欢迎氛围 (必须满足)**: 必须有明确的、热情的欢迎语。
    2.  **结构化呈现 (必须满足)**: 必须使用列表或分段。
    【待评估的回答】
    ---
    {response_to_judge}
    ---
    【输出要求】请只回答"通过"或"不通过"。
    """

    run_ai_judge_optimization(initial_prompt, retrieved_text, final_judge_prompt)
