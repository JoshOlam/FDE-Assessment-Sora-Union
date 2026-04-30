# AI Customer Support Agent Prototype

This repository contains a lightweight mock AI Agent designed to automate customer support inquiries. The agent is built using Python, Langchain, and OpenAI. It acts as an orchestrator that determines user intent, extracts variables like order IDs, and calls appropriate tools (mock databases and APIs) to resolve issues or gracefully escalate to a human agent when necessary.

## Problem Framing

Customer support teams spend a massive amount of time fielding repetitive requests: "Where is my order?" or "I want a refund." While standard chatbots often struggle with natural language and force users down rigid decision trees, an LLM-based agent can smoothly identify the intent, extract relevant entities (like order IDs), and execute function calls to backend services to resolve the issue directly.

If the agent cannot resolve the issue (e.g., an unsupported request or complex situation like large refunds requiring manager approval), it degrades gracefully by escalating the context to a human agent via a ticketing system.

## Solution Overview

This system uses a lightweight mock Python environment to simulate:
1. **The User**: Providing natural language inquiries.
2. **The AI Agent**: Acting as the orchestrator to determine user intent, extracting necessary variables, and deciding which tools to call.
3. **The Tools / Services**: 
   - A database to look up order status and details (`lookup_order`).
   - An API to process refunds with conditional logic (e.g. managers approval needed for amounts > $100) (`process_refund`).
   - A fallback tool to create escalation tickets (`escalate_to_human`).
4. **Conversational Memory**: 
   - A global chat history object tracks conversational state so the agent remembers your name and context across multiple interactions in the same session.

## Prerequisites

- Python 3.10+
- `uv` package manager

## Setup and Run Instructions

1. **Install dependencies**:
   Make sure you have `uv` installed, then run:
   ```bash
   uv sync
   ```
   Or if you don't have `uv`, install standard dependencies:
   ```bash
   pip install langchain langchain-openai langgraph python-dotenv
   ```

2. **Set up Environment Variables**:
   Copy the example environment file and add your OpenAI API key:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set `OPENAI_API_KEY=your-api-key-here`.

3. **Run the Agent**:
   Start the interactive prompt by running:
   ```bash
   uv run main.py
   ```
   Or standard Python:
   ```bash
   python main.py
   ```

## Example Usage

When the program runs, you will be greeted with an interactive prompt. You can ask questions such as:
- "Hello, my name is John." (Tests conversational memory)
- "What is the status of order ORD-123?"
- "I want to get a refund for ORD-123."
- "Can you process a refund for ORD-456?" (This will test the escalation flow as it exceeds $100).
- "I need help with something else." (This will test the direct escalation to a human agent).

## Video Walkthrough

A complete conversational video covering the problem framing, solution architecture, tradeoffs, and iteration process can be found in this [Loom video](https://www.loom.com/share/78016cbad0394bbab7343a5586cacee4).
