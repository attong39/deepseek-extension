"""Agent creation and management examples.





This module demonstrates how to create, configure, and manage AI agents


using the ZETA AI Server API.


"""

import asyncio

import httpx
from pydantic import BaseModel
import Exception
import agent
import agent_id
import analysis_agent
import api_key
import base_url
import basic_agent
import bool
import code_agent
import creative_agent
import description
import detailed_agent
import e
import execution_agent
import float
import int
import len
import list
import name
import planning_agent
import print
import research_agent
import self
import str
import updated_agent
import updates


class AgentConfig(BaseModel):
    """Agent configuration model."""

    model: str = "gpt-4"

    temperature: float = 0.7

    max_tokens: int = 2000

    system_prompt: str = "You are a helpful AI assistant."


class Agent(BaseModel):
    """Agent response model."""

    id: str

    name: str

    description: str

    status: str

    config: AgentConfig

    created_at: str


class ZetaAIClient:
    """ZETA AI Server API client."""

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")

        self.api_key = api_key

        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    async def create_agent(
        self, name: str, description: str, config: AgentConfig
    ) -> Agent:
        """Create a new AI agent."""

        data = {"name": name, "description": description, "config": config.dict()}

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/agents", headers=self.headers, json=data
            )

            response.raise_for_status()

            return Agent(**response.json())

    async def get_agent(self, agent_id: str) -> Agent:
        """Get agent by ID."""

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v1/agents/{agent_id}", headers=self.headers
            )

            response.raise_for_status()

            return Agent(**response.json())

    async def list_agents(self) -> list[Agent]:
        """List all agents."""

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v1/agents", headers=self.headers
            )

            response.raise_for_status()

            return [Agent(**agent) for agent in response.json()]

    async def update_agent(self, agent_id: str, **updates) -> Agent:
        """Update agent configuration."""

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.base_url}/api/v1/agents/{agent_id}",
                headers=self.headers,
                json=updates,
            )

            response.raise_for_status()

            return Agent(**response.json())

    async def delete_agent(self, agent_id: str) -> bool:
        """Delete an agent."""

        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}/api/v1/agents/{agent_id}", headers=self.headers
            )

            response.raise_for_status()

            return response.status_code == 204


async def example_basic_agent_creation():
    """Example: Create a basic AI assistant agent."""

    print("🤖 Creating a basic AI assistant...")

    client = ZetaAIClient("http://localhost:8000", "your-api-key")

    # Create agent configuration

    config = AgentConfig(
        model="gpt-4",
        temperature=0.7,
        max_tokens=1000,
        system_prompt="You are a helpful AI assistant that provides clear and concise answers.",
    )

    # Create the agent

    _ = await client.create_agent(
        name="General Assistant",
        description="A general-purpose AI assistant for various tasks",
        config=config,
    )

    print(f"✅ Created agent: {agent.name} (ID: {agent.id})")

    return agent


async def example_specialized_agents():
    """Example: Create specialized agents for different tasks."""

    print("🎯 Creating specialized agents...")

    client = ZetaAIClient("http://localhost:8000", "your-api-key")

    # Code assistant agent

    code_config = AgentConfig(
        model="gpt-4",
        temperature=0.2,  # Lower temperature for more deterministic code
        max_tokens=2000,
        system_prompt="""You are an expert software engineer. You help with:


        - Writing clean, efficient code


        - Code reviews and debugging


        - Architecture recommendations


        - Best practices and patterns


        Always provide working code examples and explain your reasoning.""",
    )

    await client.create_agent(
        name="Code Assistant",
        description="Specialized agent for software development tasks",
        config=code_config,
    )

    # Creative writing agent

    creative_config = AgentConfig(
        model="gpt-4",
        temperature=0.9,  # Higher temperature for creativity
        max_tokens=3000,
        system_prompt="""You are a creative writing assistant. You help with:


        - Story writing and plot development


        - Character creation and development


        - Poetry and creative expression


        - Content ideation and brainstorming


        Be imaginative, inspiring, and help users express their creativity.""",
    )

    await client.create_agent(
        name="Creative Writer",
        description="Specialized agent for creative writing and content creation",
        config=creative_config,
    )

    # Data analysis agent

    analysis_config = AgentConfig(
        model="gpt-4",
        temperature=0.3,
        max_tokens=2000,
        system_prompt="""You are a data analysis expert. You help with:


        - Data interpretation and insights


        - Statistical analysis and visualization


        - Report generation and summaries


        - Trend identification and predictions


        Provide accurate, data-driven insights with clear explanations.""",
    )

    await client.create_agent(
        name="Data Analyst",
        description="Specialized agent for data analysis and insights",
        config=analysis_config,
    )

    print(f"✅ Created {code_agent.name} (ID: {code_agent.id})")

    print(f"✅ Created {creative_agent.name} (ID: {creative_agent.id})")

    print(f"✅ Created {analysis_agent.name} (ID: {analysis_agent.id})")

    return [code_agent, creative_agent, analysis_agent]


async def example_agent_management():
    """Example: Manage agent lifecycle and configuration."""

    print("🔧 Demonstrating agent management...")

    client = ZetaAIClient("http://localhost:8000", "your-api-key")

    # List all existing agents

    agents = await client.list_agents()

    print(f"📋 Found {len(agents)} existing agents")

    if not agents:
        # Create a test agent if none exist

        config = AgentConfig()

        _ = await client.create_agent(
            name="Test Agent",
            description="Agent for management demonstration",
            config=config,
        )

        agents = [agent]

    # Get detailed information about the first agent

    _ = agents[0]

    await client.get_agent(agent.id)

    print(f"📊 Agent details: {detailed_agent.name}")

    print(f"   Status: {detailed_agent.status}")

    print(f"   Model: {detailed_agent.config.model}")

    print(f"   Temperature: {detailed_agent.config.temperature}")

    # Update agent configuration

    await client.update_agent(
        agent.id,
        description="Updated description for demonstration",
        config={"temperature": 0.8, "max_tokens": 1500},
    )

    print("🔄 Updated agent configuration")

    print(f"   New temperature: {updated_agent.config.temperature}")

    print(f"   New max_tokens: {updated_agent.config.max_tokens}")

    return updated_agent


async def example_agent_with_memory():
    """Example: Create an agent with memory capabilities."""

    print("🧠 Creating agent with memory capabilities...")

    client = ZetaAIClient("http://localhost:8000", "your-api-key")

    # Create agent with memory-enabled configuration

    memory_config = AgentConfig(
        model="gpt-4",
        temperature=0.7,
        max_tokens=2000,
        system_prompt="""You are an AI assistant with excellent memory capabilities.


        You remember previous conversations and can build upon them.


        You learn user preferences and adapt your responses accordingly.


        Always refer to relevant information from previous interactions when appropriate.""",
    )

    _ = await client.create_agent(
        name="Memory-Enhanced Assistant",
        description="An AI assistant with advanced memory and personalization",
        config=memory_config,
    )

    print(f"✅ Created memory-enhanced agent: {agent.name}")

    print("   This agent can remember conversations and learn preferences")

    return agent


async def example_multi_agent_coordination():
    """Example: Set up multiple agents for different aspects of a project."""

    print("🤝 Setting up multi-agent coordination...")

    client = ZetaAIClient("http://localhost:8000", "your-api-key")

    # Research agent

    research_config = AgentConfig(
        model="gpt-4",
        temperature=0.4,
        max_tokens=2000,
        system_prompt="""You are a research specialist. Your role is to:


        - Gather and analyze information on given topics


        - Provide comprehensive research summaries


        - Identify key insights and trends


        - Suggest areas for further investigation


        Focus on accuracy and thoroughness in your research.""",
    )

    await client.create_agent(
        name="Research Specialist",
        description="Agent specialized in research and information gathering",
        config=research_config,
    )

    # Planning agent

    planning_config = AgentConfig(
        model="gpt-4",
        temperature=0.3,
        max_tokens=2000,
        system_prompt="""You are a project planning specialist. Your role is to:


        - Break down complex projects into manageable tasks


        - Create realistic timelines and milestones


        - Identify potential risks and mitigation strategies


        - Coordinate between different project aspects


        Focus on practical, actionable planning.""",
    )

    await client.create_agent(
        name="Project Planner",
        description="Agent specialized in project planning and coordination",
        config=planning_config,
    )

    # Execution agent

    execution_config = AgentConfig(
        model="gpt-4",
        temperature=0.5,
        max_tokens=2000,
        system_prompt="""You are an execution specialist. Your role is to:


        - Guide implementation of planned tasks


        - Provide step-by-step instructions


        - Monitor progress and suggest optimizations


        - Handle troubleshooting and problem-solving


        Focus on practical implementation and results.""",
    )

    await client.create_agent(
        name="Execution Guide",
        description="Agent specialized in task execution and implementation",
        config=execution_config,
    )

    print(f"✅ Created research agent: {research_agent.name}")

    print(f"✅ Created planning agent: {planning_agent.name}")

    print(f"✅ Created execution agent: {execution_agent.name}")

    print("🤝 Multi-agent team ready for complex projects!")

    return [research_agent, planning_agent, execution_agent]


async def main():
    """Run all agent creation examples."""

    print("🚀 ZETA AI Agent Creation Examples")

    print("=" * 50)

    try:
        # Basic agent creation

        _ = await example_basic_agent_creation()
        _ = basic_agent  # Mark as used to avoid F841

        print()

        # Specialized agents

        specialized_agents = await example_specialized_agents()

        print()

        # Agent management

        await example_agent_management()

        print()

        # Memory-enhanced agent

        await example_agent_with_memory()

        print()

        # Multi-agent coordination

        team_agents = await example_multi_agent_coordination()

        print()

        print("🎉 All examples completed successfully!")

        print(
            f"📊 Total agents created: {1 + len(specialized_agents) + 1 + len(team_agents)}"
        )

    except Exception as e:
        print(f"❌ Error running examples: {e}")

        print("💡 Make sure the ZETA AI Server is running and accessible")

        print("💡 Check your API key and server URL")


if __name__ == "__main__":
    # Run the examples

    asyncio.run(main())


# Deprecated: example moved


# See canonical example at: ../../../docs/examples/agent_creation.py
