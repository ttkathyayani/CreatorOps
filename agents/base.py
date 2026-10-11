class BaseAgent:
    """Base class for all CreatorOps AI Agents."""
    name = "Base Agent"
    description = "Abstract base agent"

    def run(self, data: dict) -> dict:
        """Execute the agent on the input dictionary and return structured output."""
        raise NotImplementedError("Subclasses must implement run(data).")
