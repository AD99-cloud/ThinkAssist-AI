import os
import json

from dotenv import load_dotenv
from groq import Groq

from SRC.TOOLS.calculator import calculate
from SRC.TOOLS.device_lookup import lookup_device_spec

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY was not found.")

client = Groq(api_key=api_key)

MODEL_NAME = "openai/gpt-oss-20b"


CALCULATOR_TOOL = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": (
            "Perform arithmetic calculations. "
            "Use this when the user asks for mathematical calculations, "
            "percentages, totals, discounts, division, multiplication, "
            "addition, or subtraction."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": (
                        "A mathematical expression such as "
                        "'149.99 * 0.85' or '(200 + 50) / 2'."
                    )
                }
            },
            "required": ["expression"]
        }
    }
}


DEVICE_LOOKUP_TOOL = {
    "type": "function",
    "function": {
        "name": "lookup_device_spec",
        "description": (
            "Look up structured specifications for the "
            "ThinkPad P1 Gen 7. Use this for questions about "
            "known ports or device features."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": (
                        "Specification category. "
                        "Currently supported categories are "
                        "'ports' and 'features'."
                    )
                },
                "item": {
                    "type": "string",
                    "description": (
                        "Specific item to look up, such as "
                        "'hdmi', 'usb_a', 'usb_c', "
                        "'camera', or 'wireless'."
                    )
                }
            },
            "required": ["category", "item"]
        }
    }
}


TOOLS = [
    CALCULATOR_TOOL,
    DEVICE_LOOKUP_TOOL
]


def run_tool_question(question: str):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a technical support AI assistant for "
                "the ThinkPad P1 Gen 7. "
                "Use the calculator tool when arithmetic is required. "
                "Use lookup_device_spec when the user asks about a "
                "structured device specification that the tool supports. "
                "Do not invent tool results."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
        temperature=0.1
    )

    assistant_message = response.choices[0].message

    # No tool was selected
    if not assistant_message.tool_calls:
        return {
            "answer": assistant_message.content,
            "tool_used": None
        }

    # Add the assistant's tool-call message
    messages.append(assistant_message)

    tools_used = []

    for tool_call in assistant_message.tool_calls:

        tool_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        if tool_name == "calculate":

            expression = arguments["expression"]

            result = calculate(expression)

        elif tool_name == "lookup_device_spec":

            category = arguments["category"]
            item = arguments["item"]

            result = lookup_device_spec(
                category=category,
                item=item
            )

        else:
            result = {
                "error": f"Unknown tool: {tool_name}"
            }

        tools_used.append(tool_name)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_name,
            "content": json.dumps(result)
        })

    # Give the tool result back to the model
    final_response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.1
    )

    return {
        "answer": final_response.choices[0].message.content,
        "tool_used": tools_used[0] if len(tools_used) == 1 else tools_used
    }