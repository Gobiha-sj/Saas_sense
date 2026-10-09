
import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools import (
    subscription_search,
    analyze_usage,
    calculate_waste,
    renewal_analysis,
    contract_analysis,
    memory_search,
)
from memory import save_memory


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. Check your .env file."
    )

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.5-flash-lite"


# Instructions for the AI agent
SYSTEM_PROMPT = """
You are SAAS-SENSE, an autonomous SaaS subscription
optimization agent.

Investigate subscriptions and identify:
- Unused and low-usage licenses
- Expensive subscriptions
- Orphaned employee licenses
- Duplicate subscriptions
- Upcoming renewals
- Downgrade and consolidation opportunities
- Potential savings

Use tools to gather evidence before making recommendations.
Never invent database information.
Low usage alone does not prove a subscription should be cancelled.
Consider employee status, department, usage, cost, plan,
contract, renewal date, and previous decisions.
Never actually cancel a subscription.

Return a report using exactly this structure:

FINDING
Brief summary of the important findings.

EVIDENCE
Bullet points containing relevant evidence.

RECOMMENDATION
Choose Retain, Review, Downgrade, Reclaim, or Cancel.
Explain the reason.

ESTIMATED SAVINGS
Give monthly and annual estimates when available.
Label savings as estimates.

CONFIDENCE
High, Medium, or Low, with a short reason.

Keep the report concise and professional.
"""


# Gemini function declarations
FUNCTION_DECLARATIONS = [
    {
        "name": "subscription_search",
        "description": "Search subscriptions by application or department.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "application": {
                    "type": "STRING",
                    "description": "Application name, or null for all applications.",
                    "nullable": True,
                },
                "department": {
                    "type": "STRING",
                    "description": "Department name, or null for all departments.",
                    "nullable": True,
                },
            },
            "required": ["application", "department"],
        },
    },
    {
        "name": "analyze_usage",
        "description": "Analyze SaaS license usage.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "application": {
                    "type": "STRING",
                    "description": "Application name, or null for all applications.",
                    "nullable": True,
                },
                "min_logins": {
                    "type": "INTEGER",
                    "description": "Minimum login threshold; normally 5.",
                },
            },
            "required": ["application", "min_logins"],
        },
    },
    {
        "name": "calculate_waste",
        "description": "Estimate monthly and annual SaaS waste.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "application": {
                    "type": "STRING",
                    "description": "Application name, or null for all applications.",
                    "nullable": True,
                },
            },
            "required": ["application"],
        },
    },
    {
        "name": "renewal_analysis",
        "description": "Find subscriptions renewing within a specified number of days.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "days": {
                    "type": "INTEGER",
                    "description": "Number of days to look ahead.",
                },
            },
            "required": ["days"],
        },
    },
    {
        "name": "contract_analysis",
        "description": "Retrieve SaaS contract information.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "application": {
                    "type": "STRING",
                    "description": "Application name, or null for all applications.",
                    "nullable": True,
                },
            },
            "required": ["application"],
        },
    },
    {
        "name": "memory_search",
        "description": "Search previous subscription investigations.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "query": {
                    "type": "STRING",
                    "description": "Keywords for the previous investigation.",
                },
            },
            "required": ["query"],
        },
    },
]

GEMINI_TOOLS = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration.model_validate(item)
            for item in FUNCTION_DECLARATIONS
        ]
    )
]


# Execute a tool requested by Gemini
def execute_tool(name, arguments):
    if name == "subscription_search":
        return subscription_search(
            arguments.get("application"),
            arguments.get("department"),
        )

    if name == "analyze_usage":
        return analyze_usage(
            arguments.get("application"),
            arguments.get("min_logins", 5),
        )

    if name == "calculate_waste":
        return calculate_waste(
            arguments.get("application"),
        )

    if name == "renewal_analysis":
        return renewal_analysis(
            arguments.get("days", 30),
        )

    if name == "contract_analysis":
        return contract_analysis(
            arguments.get("application"),
        )

    if name == "memory_search":
        return memory_search(
            arguments.get("query", ""),
        )

    return {"error": f"Unknown tool: {name}"}


# Main autonomous agent loop
def run_agent(question):
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=question)],
        )
    ]

    investigation_log = []

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=GEMINI_TOOLS,
        automatic_function_calling=(
            types.AutomaticFunctionCallingConfig(disable=True)
        ),
        temperature=0.2,
    )

    # Allow up to 10 investigation rounds
    for step in range(10):
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=config,
        )

        if not response.candidates:
            return "Gemini returned no response. Please try again."

        candidate = response.candidates[0]

        if candidate.content is None:
            return "Gemini returned no response content."

        function_calls = response.function_calls or []

        # No function calls means the agent has its final answer
        if not function_calls:
            answer = response.text or "No text response was returned."

            try:
                save_memory(
                    question,
                    json.dumps(investigation_log, default=str),
                    answer,
                )
            except Exception as exc:
                print(f"Warning: Could not save memory: {exc}")

            return answer

        # Preserve the model's function-call response
        contents.append(candidate.content)

        # Run each requested tool and return its result
        for call in function_calls:
            name = call.name
            arguments = dict(call.args or {})

            try:
                result = execute_tool(name, arguments)
            except Exception as exc:
                result = {"error": f"{name} failed: {exc}"}

            investigation_log.append({
                "step": step + 1,
                "tool": name,
                "arguments": arguments,
                "result": result,
            })

            contents.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_function_response(
                            name=name,
                            response={"result": result},
                        )
                    ],
                )
            )

    return (
        "Unable to complete the investigation after 10 rounds. "
        "Please ask a more specific question."
    )
