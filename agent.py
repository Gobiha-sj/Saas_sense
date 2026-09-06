import json
import os
from dotenv import load_dotenv
from openai import OpenAI

from tools import (
    subscription_search,
    analyze_usage,
    calculate_waste,
    renewal_analysis,
    contract_analysis,
    memory_search
)
from memory import save_memory

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is not set. Check your .env file.")

client = OpenAI(api_key=api_key)

MODEL = "gpt-5.6-luna"

SYSTEM_PROMPT = """
You are SaaS-Sense, an autonomous SaaS subscription optimization agent.

Investigate SaaS subscriptions using the available tools and identify:
unused licenses, low usage, expensive subscriptions, orphaned licenses,
duplicate subscriptions, upcoming renewals, downgrade opportunities,
consolidation opportunities and potential savings.

Use the ReAct approach internally:
Reason -> Action -> Observation -> Reason -> Action -> Final Answer.

Never invent database information. Use tools whenever required.

Do not recommend cancellation only because usage is low. Consider usage,
employee, department, plan, cost, contract, renewal date and previous decisions.

Return a professional business report using exactly this structure:

FINDING
Brief summary of the important findings.

EVIDENCE
Bullet points containing relevant data from the tools.

RECOMMENDATION
Specific action such as Retain, Review, Downgrade, Reclaim or Cancel.

ESTIMATED SAVINGS
Give monthly and annual savings when they can be calculated.

CONFIDENCE
High, Medium or Low, with one short reason.

Keep the response concise and professional.
"""

TOOLS = [
    {
        "type": "function",
        "name": "subscription_search",
        "description": "Search SaaS subscriptions by application or department.",
        "parameters": {
            "type": "object",
            "properties": {
                "application": {
                    "type": ["string", "null"]
                },
                "department": {
                    "type": ["string", "null"]
                }
            },
            "required": ["application", "department"]
        }
    },
    {
        "type": "function",
        "name": "analyze_usage",
        "description": "Analyze SaaS license usage.",
        "parameters": {
            "type": "object",
            "properties": {
                "application": {
                    "type": ["string", "null"]
                },
                "min_logins": {
                    "type": "integer"
                }
            },
            "required": ["application", "min_logins"]
        }
    },
    {
        "type": "function",
        "name": "calculate_waste",
        "description": "Calculate estimated SaaS waste and savings.",
        "parameters": {
            "type": "object",
            "properties": {
                "application": {
                    "type": ["string", "null"]
                }
            },
            "required": ["application"]
        }
    },
    {
        "type": "function",
        "name": "renewal_analysis",
        "description": "Find subscriptions renewing within a specified number of days.",
        "parameters": {
            "type": "object",
            "properties": {
                "days": {
                    "type": "integer"
                }
            },
            "required": ["days"]
        }
    },
    {
        "type": "function",
        "name": "contract_analysis",
        "description": "Analyze SaaS contract information.",
        "parameters": {
            "type": "object",
            "properties": {
                "application": {
                    "type": ["string", "null"]
                }
            },
            "required": ["application"]
        }
    },
    {
        "type": "function",
        "name": "memory_search",
        "description": "Search previous SaaS investigations.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string"
                }
            },
            "required": ["query"]
        }
    }
]

def execute_tool(name, arguments):
    if name == "subscription_search":
        return subscription_search(
            arguments.get("application"),
            arguments.get("department")
        )

    if name == "analyze_usage":
        return analyze_usage(
            arguments.get("application"),
            arguments.get("min_logins", 5)
        )

    if name == "calculate_waste":
        return calculate_waste(
            arguments.get("application")
        )

    if name == "renewal_analysis":
        return renewal_analysis(
            arguments.get("days", 30)
        )

    if name == "contract_analysis":
        return contract_analysis(
            arguments.get("application")
        )

    if name == "memory_search":
        return memory_search(
            arguments.get("query", "")
        )

    return {"error": "Unknown tool"}

def run_agent(question):
    messages = [
        {
            "role": "user",
            "content": question
        }
    ]

    investigation_log = []

    for _ in range(10):
        response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            tools=TOOLS,
            input=messages
        )

        tool_calls = [
            item for item in response.output
            if item.type == "function_call"
        ]

        if not tool_calls:
            answer = response.output_text

            save_memory(
                question,
                json.dumps(investigation_log, default=str),
                answer
            )

            return answer

        messages += response.output

        for tool_call in tool_calls:
            try:
                arguments = json.loads(tool_call.arguments)
            except Exception:
                arguments = {}

            result = execute_tool(
                tool_call.name,
                arguments
            )

            investigation_log.append({
                "tool": tool_call.name,
                "arguments": arguments,
                "result": result
            })

            messages.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": json.dumps(result, default=str)
            })

    return "Unable to complete the investigation."