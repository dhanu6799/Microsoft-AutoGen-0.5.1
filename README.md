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

```text
Creator Agent  →  Registers Specialized Agents
   │
   ├─ ResearchAgent  →  Finds a real-world problem
   ├─ DesignerAgent  →  Drafts a product concept
   ├─ EngineerAgent  →  Proposes system architecture
   ├─ ReviewerAgent  →  Evaluates strengths & risks
   └─ PMAgent        →  Summarizes final startup brief
🗂️ Output

Every stage produces a Markdown file under /output/:
1_research.md
2_design.md
3_engineer.md
4_review.md
final_startup.md

Each file contains detailed reasoning, features, and evaluations for the proposed startup idea.
