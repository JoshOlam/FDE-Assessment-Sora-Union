from typing import Optional

from dotenv import find_dotenv, load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

load_dotenv(find_dotenv())

# Mock Database
ORDERS_DB = {
    "ORD-123": {"status": "shipped", "amount": 50, "item": "Wireless Mouse"},
    "ORD-456": {"status": "delivered", "amount": 150, "item": "Mechanical Keyboard"},
    "ORD-789": {"status": "processing", "amount": 20, "item": "USB-C Cable"},
}

TICKETS_DB = []

@tool
def lookup_order(order_id: str) -> str:
    """Look up the status and details of an order using the order ID."""
    order = ORDERS_DB.get(order_id)
    if order:
        return f"Order {order_id} is currently {order['status']}. Item: {order['item']}, Amount: ${order['amount']}."
    return f"Order {order_id} not found."

@tool
def process_refund(order_id: str) -> str:
    """Process a refund for a given order ID. Checks order amount for manager approval."""
    order = ORDERS_DB.get(order_id)
    if not order:
        return f"Cannot process refund: Order {order_id} not found."
    
    amount = int(order["amount"])
    if amount > 100:
        return f"Refund for order {order_id} requires manager approval as the amount (${amount}) exceeds $100. Please escalate to human agent."
    
    # Simulate processing refund
    ORDERS_DB[order_id]["status"] = "refunded"
    return f"Refund of ${amount} for order {order_id} has been processed successfully."

@tool
def escalate_to_human(issue_description: str, order_id: Optional[str] = None) -> str:
    """Escalate the issue to a human agent by creating a support ticket. Use this when you cannot resolve the issue."""
    ticket_id = f"TKT-{len(TICKETS_DB) + 100}"
    ticket = {
        "ticket_id": ticket_id,
        "issue": issue_description,
        "order_id": order_id,
        "status": "open"
    }
    TICKETS_DB.append(ticket)
    return f"Ticket {ticket_id} has been created for human escalation."

# Global chat history for memory
chat_history = []

def run_support_agent(query: str):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [lookup_order, process_refund, escalate_to_human]
    
    system_prompt = "You are a helpful customer support AI agent. You can look up orders, process refunds, and escalate to a human agent if needed. If a refund requires manager approval, you MUST escalate it to a human using the escalate_to_human tool."
    
    agent = create_agent(llm, tools, system_prompt=system_prompt)
    
    # Append user query
    chat_history.append(("user", query))
    
    response = agent.invoke({"messages": chat_history})
    
    # Update chat history with new messages from the response
    # The response["messages"] contains the full conversation including the new AI messages.
    # We can just replace our history with the updated messages to maintain state.
    chat_history.clear()
    chat_history.extend(response["messages"])
    
    return {"output": response["messages"][-1].content}

if __name__ == "__main__":
    print("=========================================")
    print("Welcome to the AI Customer Support Agent!")
    print("=========================================")
    print("Available test orders:")
    print("- ORD-123: Shipped, $50")
    print("- ORD-456: Delivered, $150 (Requires manager approval for refund)")
    print("- ORD-789: Processing, $20")
    print("Type 'exit' or 'quit' to quit.\n")
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                print("\nExiting...")
                break
            
            if not user_input.strip():
                continue
                
            result = run_support_agent(user_input)
            print(f"\nAgent: {result['output']}")
        except Exception as e:
            print(f"Error: {e}")
            if "OPENAI_API_KEY" in str(e):
                print("\nPlease make sure you have set the OPENAI_API_KEY environment variable in your .env file.")
                break
        except KeyboardInterrupt:
            print("\nExiting...")
            break
