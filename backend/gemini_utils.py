import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_structure(text):

    prompt = f"""
Analyze the following text and extract a workflow.

Return ONLY valid JSON.

Use EXACTLY this schema:

{{
  "nodes": [
    {{
      "id": "A",
      "label": "Student submits assignment"
    }}
  ],
  "edges": [
    {{
      "source": "A",
      "target": "B"
    }}
  ]
}}

Rules:
1. Every node must contain id and label.
2. Label should be a natural workflow step.
3. Preserve actors when relevant.
4. Edges must be objects.
5. Return only JSON.
6. No markdown fences.
7. Do not change the meaning or intent of the original text when shortening labels.
8. Keep labels concise while preserving the complete workflow context.
9. If two or more consecutive dependent actions form a single logical workflow step, combine and summarize them into one concise label without losing information or changing the meaning.
10. Do not merge independent workflow steps.
11. Remove unnecessary details, articles (a, an, the), and filler words while preserving the original meaning.
12. If the same actor appears in more than two consecutive workflow steps, use an appropriate pronoun (e.g., he, she, they, it) in subsequent labels to avoid repetition, provided the reference remains clear. If the actor changes, use the new actor explicitly instead of a pronoun.

Text:

{text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    cleaned = response.text.strip()
    cleaned = cleaned.replace("```json", "")
    cleaned = cleaned.replace("```", "")
    cleaned = cleaned.strip()

    try:
        workflow = json.loads(cleaned)
    except json.JSONDecodeError:
        raise ValueError("Gemini returned invalid JSON.")

    if "nodes" not in workflow:
        raise ValueError("Workflow JSON missing 'nodes'.")

    if "edges" not in workflow:
        raise ValueError("Workflow JSON missing 'edges'.")

    if not isinstance(workflow["nodes"], list):
        raise ValueError("'nodes' must be a list.")

    if not isinstance(workflow["edges"], list):
        raise ValueError("'edges' must be a list.")

    for node in workflow["nodes"]:
        if "id" not in node:
            raise ValueError("Node missing 'id'.")

        if "label" not in node:
            raise ValueError("Node missing 'label'.")

    for edge in workflow["edges"]:
        if "source" not in edge:
            raise ValueError("Edge missing 'source'.")

        if "target" not in edge:
            raise ValueError("Edge missing 'target'.")

    return workflow


def json_to_mermaid(data):

    direction = "LR"

    if len(data["nodes"]) > 6:
        direction = "TD"

    lines = [f"flowchart {direction}"]

    for node in data["nodes"]:
        lines.append(
            f'{node["id"]}["{node["label"]}"]'
        )

    for edge in data["edges"]:
        lines.append(
            f'{edge["source"]} --> {edge["target"]}'
        )

    return "\n".join(lines)