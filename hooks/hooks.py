"""Observability hooks for AWS strand tools.

This module provides ObservabilityPlugin for the strands framework.
The plugin logs agent lifecycle events, tool invocations, and
output quality validation details for lightweight debugging and tracing.
"""

from strands.hooks import BeforeToolCallEvent, AfterToolCallEvent, BeforeInvocationEvent, AfterInvocationEvent, HookRegistry, HookProvider
from guardrails.output_guardrails import validate_output_quality
from guardrails.input_guardrails import validate_startup_description
from utils.console import print_agent_summary, print_warning, print_error, print_info, _error



class ObservabilityPlugin(HookProvider):
    """Plugin that logs agent and tool lifecycle events and validates output quality."""

    def __init__(self, agent_name: str, startup_description: str):
        """Initialize the logging and validation plugin for an agent.

        Args:
            agent_name: The name of the agent whose lifecycle events will be logged.
            startup_description: A description of the agent's purpose, validated before invocation.
        """
        self.agent_name = agent_name
        self.startup_description = startup_description

    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeInvocationEvent, self._before_agent)
        registry.add_callback(AfterInvocationEvent, self._after_agent)
        registry.add_callback(BeforeToolCallEvent, self._before_tool_call)
        registry.add_callback(AfterToolCallEvent, self._after_tool_call)

    def _before_agent(self, _event: BeforeInvocationEvent) -> None:
        """Hook called before the agent invocation begins."""
        if not self.startup_description:
            _error("No startup description provided — aborting.")
            return
        
        guard = validate_startup_description(self.startup_description)
        if not guard.passed:
            _error(f"Input rejected: {guard.reason}")
            return

    def _after_agent(self, event: AfterInvocationEvent) -> None:
        """Hook called after the agent invocation completes."""
        output = event.result.structured_output if event.result is not None else None
        if output is not None:
            quality = validate_output_quality(output, self.agent_name)
            for warning in quality.warnings:
                print_warning(warning)
            for error in quality.errors:
                print_error(error)
            if not quality.passed:
                print_error(f"[{self.agent_name}] Output failed quality check.")
            summary = getattr(output, "summary", None)
            if summary:
                print_agent_summary(self.agent_name, summary)
        print_info(f"[{self.agent_name}] Agent invocation completed")

    def _before_tool_call(self, event: BeforeToolCallEvent) -> None:
        """Hook called before a tool is invoked."""
        print_info(f"[{self.agent_name}] Calling: {event.tool_use['name']}")

    def _after_tool_call(self, event: AfterToolCallEvent) -> None:
        """Hook called after a tool completes execution."""
        print_info(f"[{self.agent_name}] Completed: {event.tool_use['name']}")