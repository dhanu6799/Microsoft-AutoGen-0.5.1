# 🛠️ Getting Started with MCP (Model Context Protocol) on Windows + WSL

Over the weekend, I got Microsoft’s **AutoGen MCP tools** running locally on my Windows machine. Since the docs assume Linux/macOS, I wanted to share a **step-by-step Windows-friendly guide** for anyone struggling.

---

## 🌐 What is MCP?

**Model Context Protocol (MCP)** is an open standard that lets AI agents interact with external tools (APIs, databases, fetchers, etc.) in a consistent, secure way.  

Think of it as **“plug-and-play tools for LLM agents”** — you run a tool server, and your agent can call it through MCP without custom glue code.

---

## 🖥️ Why Windows Needs Extra Steps

Most MCP and AutoGen examples assume Unix-like environments. On Windows:
- Python environments can get confusing (WSL vs native Windows)  
- Some commands like `uvx` aren’t available by default  
- You may see endless `ModuleNotFoundError` until the right packages are installed  

---

## ⚡ Step 1: Install WSL + Python

1. Enable WSL and install Ubuntu from the Microsoft Store.  
2. Inside WSL, install Python + pip:

   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip python3-venv
3. (Optional but cleaner) Create a virtual environment:

python3 -m venv autogen-env
source autogen-env/bin/activate

## ⚡ Step 2: Install AutoGen + MCP Dependencies

Inside your environment:

<pre>
pip install --upgrade pip
pip install pyautogen autogen-core autogen-agentchat autogen-ext
pip install openai anthropic
pip install requests pillow python-dotenv pydantic ipython jupyterlab tiktoken
pip install mcp mcp-server-fetch
</pre>pre>

## ⚡ Step 3: Replace uvx with Python

The docs often use:

<pre>
StdioServerParams(command="uvx", args=["mcp-server-fetch"])
</pre>


But Windows doesn’t ship uvx. Instead, call the MCP fetch server with Python:

<pre>
fetch_mcp_server = StdioServerParams(
    command="python3",
    args=["-m", "mcp_server_fetch"],
    read_timeout_seconds=30,
)
</pre>

## ⚡ Step 4: Full Example

There is a working script that uses the MCP fetch tool to let an AutoGen agent summarize a webpage: I have saved it as mcp_server_fetch.

🐛 Common Pitfalls I Hit

ModuleNotFoundError: autogen_agentchat → install pyautogen and subpackages.

ModuleNotFoundError: dotenv / tiktoken / mcp → pip install missing libraries.

FileNotFoundError: 'uvx' → replace with python3 -m mcp_server_fetch.

🚀 Final Thoughts

MCP unlocks a powerful way to let AI agents safely extend into real-world APIs and tools.

If you’re on Windows, the key is:
👉 Use WSL + Python venv
👉 Install all AutoGen + MCP deps together
👉 Swap uvx → python3 -m

Now you can run the same MCP-enabled agents as Linux/macOS users. 
