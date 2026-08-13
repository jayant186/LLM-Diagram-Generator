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
Analyze the following text and convert it into a meaningful diagram structure.

Return ONLY valid JSON.

Use EXACTLY this schema:

{{
  "nodes": [
    {{
      "id": "A",
      "label": "Artificial Intelligence"
    }},
    {{
      "id": "B",
      "label": "Education"
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

1. Every node must contain "id" and "label".
2. Every edge must contain "source" and "target".
3. Extract MULTIPLE meaningful concepts, actions, outcomes, applications,
   problems, causes, effects, or goals from the text.
4. DO NOT summarize the entire text into a single node.
5. Each major idea should normally be represented as a separate node.
6. Identify relationships between ideas and represent them using edges.
7. Preserve the meaning and intent of the original text.
8. Labels should be concise but informative.
9. Do not create unnecessary nodes for filler words or minor details.
10. Do not merge independent concepts into one node.
11. If the text contains a list of applications, problems, benefits,
    causes, effects, or examples, create separate nodes for the
    individual items when they are meaningful.
12. If one concept causes, leads to, enables, affects, or relates to
    another concept, create an edge between them.
13. The diagram should represent the STRUCTURE and RELATIONSHIPS
    of the complete text, not merely its main conclusion.
14. Do not invent information that is not present in the text.
15. Use unique IDs such as A, B, C, D, etc.
16. Return only JSON.
17. Do not use markdown fences.
18. For a paragraph containing several distinct ideas, aim for
    approximately 5-15 meaningful nodes rather than one summary node.
19. Do not artificially split a single simple action into many nodes.

Example:

Text:
"AI is used in education and healthcare. It analyzes large amounts
of data and helps people make better decisions. However, it raises
concerns about privacy and job displacement."

Expected structure should contain separate nodes for concepts such as:

Artificial Intelligence
Education
Healthcare
Data Analysis
Better Decisions
Privacy
Job Displacement

and appropriate edges connecting them.

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