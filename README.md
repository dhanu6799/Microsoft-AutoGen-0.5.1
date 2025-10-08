# 🧠 AI Startup Studio & Autogen Playground

This repository explores **Autogen's multi-agent framework** through a series of labs and culminates in a complete project —  
an **AI Startup Studio** that autonomously ideates, designs, and documents startup-style product ideas.

---

## 📁 Repository Structure

| Folder / File | Description |
|----------------|-------------|
| **AI_Startup_Studio/** | Full multi-agent pipeline simulating a startup team — Researcher, Designer, Engineer, Reviewer, and PM. |
| **Agent Creator/** | Mini project showing how new agents can be programmatically created and launched (`agent.py`, `creator.py`, `messages.py`, `world.py`). |
| **sandbox/** | Experiments with multi-model reasoning, structured outputs, and team workflows. |
| **1_lab1_autogen_agentchat.ipynb** | Intro to Autogen AgentChat — chat-based LLM agents. |
| **2_lab2_autogen_agentchat.ipynb** | Multi-model and structured output demonstrations. |
| **3_lab3_autogen_core.ipynb** | Deep dive into Autogen Core — agent identity, message routing, and lifecycles. |
| **4_lab4_autogen_distributed.ipynb** | Running distributed agents across gRPC runtimes. |
| **mcp_server_fetch.ipynb** | Example of an MCP-based agent that fetches external content. |
| **mcp_windows_setup.md** | Setup guide for running MCP on Windows. |
| **tickets.db** | SQLite demo for tool + database integration. |

---

## 🚀 AI Startup Studio Workflow

```
Creator Agent  →  Registers Specialized Agents
   │
   ├─ ResearchAgent  →  Finds a real-world problem
   ├─ DesignerAgent  →  Drafts a product concept
   ├─ EngineerAgent  →  Proposes system architecture
   ├─ ReviewerAgent  →  Evaluates strengths & risks
   └─ PMAgent        →  Summarizes final startup brief
```


🗂️ Output


Every stage produces a Markdown file under /output/:
1_research.md
2_design.md
3_engineer.md
4_review.md
final_startup.md

Each file contains detailed reasoning, features, and evaluations for the proposed startup idea.

Each file in this repository contains detailed reasoning, features, and evaluations for the proposed startup ideas.  
This project demonstrates how autonomous multi-agent systems can simulate an end-to-end **AI-driven startup incubation process** using **Autogen Core** and **Autogen AgentChat**.

---

## 🧩 Tech Stack Overview

| Layer | Library / Concept |
|--------|------------------|
| **Agent Runtime** | `autogen_core` — manages agent identities (`AgentId`), message passing (`RoutedAgent`), and runtime orchestration. |
| **LLM Brain** | `autogen_agentchat` — powers each agent’s thinking and conversation via `AssistantAgent` (uses OpenAI GPT-4o-mini). |
| **Communication** | gRPC runtime from `autogen_ext.runtimes.grpc` enabling distributed agents. |
| **Environment** | Python 3.12 +, `uv` for lightweight virtual environments. |
| **Visualization (optional)** | LangGraph / Streamlit for visualizing the workflow. |

---

## ⚙️ Installation & Run Guide

```
# 1️⃣  Clone the repository
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>/AI_Startup_Studio

# 2️⃣  Create virtual environment (recommended)
uv venv
uv pip install autogen-core autogen-agentchat autogen-ext python-dotenv

# 3️⃣  Run the orchestrator
uv run world.py
```

Expected Console Output:
```
✅ Registered agent_research (Agent)
✅ Registered agent_designer (Agent)
✅ Registered agent_engineer (Agent)
✅ Registered agent_reviewer (Agent)
✅ Registered agent_pm (Agent)

🚀 Starting AI Startup Studio pipeline...

[Stage 1: Research ✅]
[Stage 2: Design ✅]
[Stage 3: Engineering ✅]
[Stage 4: Review ✅]
[Stage 5: PM Summary ✅]

✅  Startup Studio run complete! Check the 'output' folder.

```

🧠 Core Concepts Simplified
|Concept	|Explanation|
|----------------|-------------|
|Autogen Core|	The body 🦾 — gives each agent an identity, mailbox, and a way to pass messages through the runtime.|
|Autogen AgentChat|	The brain 🧠 — lets each agent think, reason, and reply using an LLM like GPT-4o.|
|Combined System|	The AI Startup Studio combines both: Autogen Core manages message flow, and AgentChat generates intelligent responses.|

🧩 Architecture Diagram

Autogen Core = Body (message routing & runtime)

Autogen AgentChat = Brain (reasoning & creativity)

🧱 Example: Folder Agent Creator/

File	Purpose

agent.py	Defines generic agent behavior and conversation logic.

creator.py	Spawns and registers all specialized agents.

messages.py	Defines message structure and routing helpers.

world.py	The orchestrator — runs the full multi-agent startup pipeline.

Output/	Sample markdown outputs from a full run.


✨ Future Enhancements

Add LangGraph visualization for real-time agent flow.

Extend with external tools (APIs, web scrapers, DB connectors).

Deploy as an autonomous Startup Incubator API.
