# world.py
# ------------------------------------------------------------
# The orchestrator for the entire AI Startup Studio.
# It spins up the runtime, spawns all agents,
# and manages the multi-agent conversation pipeline.
# ------------------------------------------------------------

from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntimeHost, GrpcWorkerAgentRuntime
from autogen_core import AgentId
from creator import Creator
import messages
import asyncio
import os

async def main():
    # Initialize and start runtime
    host = GrpcWorkerAgentRuntimeHost(address="localhost:50052")
    host.start()
    worker = GrpcWorkerAgentRuntime(host_address="localhost:50052")
    await worker.start()

    # Register the Creator agent
    await Creator.register(worker, "Creator", lambda: Creator("Creator"))
    creator_id = AgentId("Creator", "default")

    # Step 1: Spawn all agents
    await worker.send_message(messages.Message(content="register_all"), creator_id)

    # Create output directory
    os.makedirs("output", exist_ok=True)

    # --- PIPELINE EXECUTION ---
    print("\n🚀 Starting AI Startup Studio pipeline...\n")

    # 1️⃣ Research
    research = await worker.send_message(messages.Message("Find a critical AI problem worth solving."), AgentId("agent_research", "default"))
    with open("output/1_research.md", "w") as f:
        f.write(research.content)

    # 2️⃣ Design
    design_prompt = f"Here’s the research insight: {research.content}\nNow design a product concept."
    design = await worker.send_message(messages.Message(design_prompt), AgentId("agent_designer", "default"))
    with open("output/2_design.md", "w") as f:
        f.write(design.content)

    # 3️⃣ Engineering
    eng_prompt = f"Here’s the product design: {design.content}\nPropose a technical architecture and pseudocode."
    engineering = await worker.send_message(messages.Message(eng_prompt), AgentId("agent_engineer", "default"))
    with open("output/3_engineer.md", "w") as f:
        f.write(engineering.content)

    # 4️⃣ Review
    review_prompt = f"Evaluate this startup idea critically: {engineering.content}"
    review = await worker.send_message(messages.Message(review_prompt), AgentId("agent_reviewer", "default"))
    with open("output/4_review.md", "w") as f:
        f.write(review.content)

    # 5️⃣ PM Summary
    summary_prompt = f"Combine everything into a final startup pitch:\n\nResearch: {research.content}\n\nDesign: {design.content}\n\nEngineering: {engineering.content}\n\nReview: {review.content}"
    summary = await worker.send_message(messages.Message(summary_prompt), AgentId("agent_pm", "default"))
    with open("output/final_startup.md", "w") as f:
        f.write(summary.content)

    print("\n✅ Startup Studio run complete! Check the 'output' folder.\n")

    # Shutdown
    await worker.stop()
    await host.stop()

if __name__ == "__main__":
    asyncio.run(main())
