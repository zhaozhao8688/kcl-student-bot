"""
ReAct agent node implementations.
Implements the Reasoning-Action-Observation loop pattern.
"""

import json
from typing import Dict, Any, Literal
from datetime import datetime

from agents.react_state import ReActState
from agents.prompts import get_react_system_prompt, format_tool_history
from tools.tool_registry import tool_registry
from services.llm_service import llm_service
from utils.logger import setup_logger

logger = setup_logger(__name__)


def reasoning_node(state: ReActState) -> Dict[str, Any]:
    """
    Analyze the current situation and decide what action to take.
    This is the "Think" step of the ReAct loop.

    Args:
        state: Current ReAct state

    Returns:
        Updated state with current thought, action, and action_input
    """
    iteration = state.get("current_iteration", 0) + 1
    max_iterations = state.get("max_iterations", 5)

    logger.info(f"ReAct reasoning - iteration {iteration}/{max_iterations}")

    # Check iteration limit
    if iteration > max_iterations:
        logger.warning(f"Max iterations ({max_iterations}) reached, forcing final answer")
        return _generate_fallback_response(state, iteration)

    # Build context from tool history
    tool_calls = state.get("tool_calls", [])
    tool_history = format_tool_history(tool_calls)

    # Get system prompt
    has_ical_url = bool(state.get("ical_url"))
    system_prompt = get_react_system_prompt(
        tool_history=tool_history,
        has_ical_url=has_ical_url
    )

    # Build user message
    user_message = f"User question: {state['query']}"

    # Add observation from previous step if available
    if state.get("current_observation"):
        user_message += f"\n\nObservation from previous action:\n{state['current_observation']}"

    # Build messages array with conversation history
    messages = [{"role": "system", "content": system_prompt}]

    # Add conversation history (sliding window: last 10 messages)
    conversation_history = state.get("conversation_history") or []
    if conversation_history:
        for msg in conversation_history[-10:]:
            role = "assistant" if msg.get("role") == "ai" else msg.get("role", "user")
            messages.append({"role": role, "content": msg.get("content", "")})

    messages.append({"role": "user", "content": user_message})

    try:
        # Call LLM with lower temperature for consistent JSON output
        logger.info(f"Calling LLM with {len(messages)} messages")
        response = llm_service.generate(
            messages=messages,
            temperature=0.3,
            max_tokens=1500
        )

        logger.info(f"LLM response length: {len(response) if response else 0}")
        logger.debug(f"LLM response: {response}")

        if not response:
            logger.error("LLM returned empty response")
            return {
                "current_iteration": iteration,
                "should_stop": True,
                "final_response": "I received an empty response from the AI model. Please try again."
            }

        # Parse JSON response
        parsed = _parse_react_response(response)
        logger.info(f"Parsed response - action: {parsed.get('action')}, has_thought: {bool(parsed.get('thought'))}")

        thought = parsed.get("thought", "")
        action = parsed.get("action", "final_answer")
        action_input = parsed.get("action_input", {})

        logger.info(f"ReAct thought: {thought[:100]}...")
        logger.info(f"ReAct action: {action}")

        # Check if this is a final answer
        should_stop = (action == "final_answer")

        # Extract final response if this is the end
        final_response = None
        if should_stop:
            # Handle case where action_input might be a string or dict
            if isinstance(action_input, dict):
                final_response = action_input.get("response", str(action_input))
            else:
                # If action_input is a string or other type, use it directly
                final_response = str(action_input) if action_input else None

            if not final_response:
                logger.warning("final_answer action but no response content found")
                final_response = "I apologize, but I couldn't formulate a proper response. Please try again."

            logger.info("ReAct loop complete - final answer generated")

        # Build reasoning trace entry
        trace_entry = {
            "iteration": iteration,
            "thought": thought,
            "action": action,
            "action_input": action_input,
            "timestamp": datetime.now().isoformat()
        }

        reasoning_trace = state.get("reasoning_trace", []).copy()
        reasoning_trace.append(trace_entry)

        return {
            "current_iteration": iteration,
            "current_thought": thought,
            "current_action": action,
            "current_action_input": action_input,
            "current_observation": None,  # Clear for next step
            "reasoning_trace": reasoning_trace,
            "should_stop": should_stop,
            "final_response": final_response
        }

    except Exception as e:
        import traceback
        logger.error(f"Error in reasoning node: {str(e)}")
        logger.error(traceback.format_exc())
        # On error, treat as final answer with error message
        error_msg = str(e)
        # Don't expose internal errors to users, but log them
        if "api_key" in error_msg.lower() or "unauthorized" in error_msg.lower():
            user_error = "There was an authentication error with the AI service. Please contact support."
        elif "timeout" in error_msg.lower():
            user_error = "The request timed out. Please try again."
        else:
            user_error = "I encountered an error while processing your request. Please try again."
        return {
            "current_iteration": iteration,
            "should_stop": True,
            "final_response": user_error
        }


def tool_execution_node(state: ReActState) -> Dict[str, Any]:
    """
    Execute the selected tool.
    This is the "Act" step of the ReAct loop.

    Args:
        state: Current ReAct state

    Returns:
        Updated state with tool call record
    """
    action = state.get("current_action", "")
    action_input = state.get("current_action_input", {})

    logger.info(f"Executing tool: {action} with input: {action_input}")

    # Create tool call record
    tool_call = {
        "tool_name": action,
        "tool_input": action_input,
        "result": None,
        "error": None,
        "timestamp": datetime.now().isoformat()
    }

    try:
        # Get tool from registry
        tool = tool_registry.get_tool(action)

        # Special handling for timetable tool (needs ical_url from state)
        if action == "timetable":
            ical_url = state.get("ical_url")
            if not ical_url:
                tool_call["error"] = "No iCal URL configured. User needs to set up their timetable subscription."
                tool_call["result"] = None
            else:
                days_ahead = action_input.get("days_ahead", 7)
                result = tool.execute(ical_url=ical_url, days_ahead=days_ahead)
                tool_call["result"] = _format_tool_result(action, result)

        # Search tool
        elif action == "search":
            query = action_input.get("query", state["query"])
            num_results = action_input.get("num_results", 5)
            result = tool.execute(query=query, num_results=num_results)
            tool_call["result"] = _format_tool_result(action, result)

        # Scraper tool
        elif action == "scraper":
            url = action_input.get("url", "")
            if not url:
                tool_call["error"] = "No URL provided for scraping"
            else:
                result = tool.execute(url=url)
                tool_call["result"] = _format_tool_result(action, result)

        # TikTok tool
        elif action == "tiktok":
            result = tool.execute(
                hashtags=action_input.get("hashtags"),
                profiles=action_input.get("profiles"),
                search_queries=action_input.get("search_queries"),
                results_per_page=action_input.get("results_per_page", 10)
            )
            tool_call["result"] = _format_tool_result(action, result)

        # Instagram tool
        elif action == "instagram":
            result = tool.execute(
                profiles=action_input.get("profiles"),
                hashtags=action_input.get("hashtags"),
                search_query=action_input.get("search_query"),
                search_type=action_input.get("search_type", "hashtag"),
                results_limit=action_input.get("results_limit", 10)
            )
            tool_call["result"] = _format_tool_result(action, result)

        else:
            tool_call["error"] = f"Unknown tool: {action}"

    except KeyError as e:
        logger.error(f"Tool not found: {action}")
        tool_call["error"] = f"Tool '{action}' not found in registry"
    except Exception as e:
        logger.error(f"Error executing tool {action}: {str(e)}")
        tool_call["error"] = str(e)

    # Add to tool calls history
    tool_calls = state.get("tool_calls", []).copy()
    tool_calls.append(tool_call)

    logger.info(f"Tool execution complete. Result length: {len(str(tool_call.get('result', '')))}, Error: {tool_call.get('error')}")

    return {"tool_calls": tool_calls}


def observation_node(state: ReActState) -> Dict[str, Any]:
    """
    Format tool output for the next reasoning step.
    This is the "Observe" step of the ReAct loop.

    Args:
        state: Current ReAct state

    Returns:
        Updated state with current_observation
    """
    tool_calls = state.get("tool_calls", [])

    if not tool_calls:
        logger.warning("No tool calls to observe")
        return {"current_observation": "No tool was executed."}

    # Get the most recent tool call
    latest_call = tool_calls[-1]

    tool_name = latest_call.get("tool_name", "unknown")
    result = latest_call.get("result")
    error = latest_call.get("error")

    if error:
        observation = f"Tool '{tool_name}' encountered an error: {error}"
    elif result is None:
        observation = f"Tool '{tool_name}' returned no results."
    else:
        # Truncate very long results
        result_str = str(result)
        if len(result_str) > 4000:
            result_str = result_str[:4000] + "\n... (result truncated)"
        observation = f"Tool '{tool_name}' returned:\n{result_str}"

    logger.info(f"Observation: {observation[:200]}...")

    return {"current_observation": observation}


def should_continue(state: ReActState) -> Literal["tool", "end"]:
    """
    Router function to determine if the loop should continue.

    Args:
        state: Current ReAct state

    Returns:
        "end" if should stop, "tool" if should continue to tool execution
    """
    if state.get("should_stop", False):
        logger.info("Router: should_stop is True, ending loop")
        return "end"

    iteration = state.get("current_iteration", 0)
    max_iterations = state.get("max_iterations", 5)

    if iteration >= max_iterations:
        logger.info(f"Router: max iterations ({max_iterations}) reached, ending loop")
        return "end"

    action = state.get("current_action", "")
    if action == "final_answer":
        logger.info("Router: action is final_answer, ending loop")
        return "end"

    logger.info(f"Router: continuing to tool execution (action: {action})")
    return "tool"


def _parse_react_response(response: str) -> Dict[str, Any]:
    """
    Parse the LLM response as JSON.

    Args:
        response: Raw LLM response string

    Returns:
        Parsed JSON as dictionary
    """
    # Clean the response - remove markdown code fences if present
    cleaned = response.strip()

    # Remove ```json and ``` markers
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to parse JSON response: {e}")
        # If parsing fails, treat the entire response as a final answer
        return {
            "thought": "Unable to parse structured response",
            "action": "final_answer",
            "action_input": {"response": response}
        }


def _format_tool_result(tool_name: str, result: Any) -> str:
    """
    Format tool result for inclusion in observations.

    Args:
        tool_name: Name of the tool
        result: Raw result from tool execution

    Returns:
        Formatted string representation
    """
    if result is None:
        return "No results found."

    if tool_name == "search":
        if not result:
            return "No search results found."
        lines = []
        for i, item in enumerate(result, 1):
            lines.append(f"{i}. {item.get('title', 'Untitled')}")
            lines.append(f"   URL: {item.get('link', 'N/A')}")
            lines.append(f"   {item.get('snippet', '')}")
            lines.append("")
        return "\n".join(lines)

    elif tool_name == "scraper":
        if not result:
            return "Failed to scrape the page or no content found."
        # Truncate long content
        if len(result) > 3000:
            return result[:3000] + "\n... (content truncated)"
        return result

    elif tool_name == "timetable":
        if not result:
            return "No upcoming events found in your timetable."
        lines = ["Upcoming events:"]
        for event in result:
            start = event.get("start", "")
            if hasattr(start, "strftime"):
                start = start.strftime("%a %d %b, %H:%M")
            lines.append(f"- {event.get('summary', 'Untitled')}")
            lines.append(f"  When: {start}")
            if event.get("location"):
                lines.append(f"  Where: {event.get('location')}")
            lines.append("")
        return "\n".join(lines)

    elif tool_name == "tiktok":
        if not result:
            return "No TikTok videos found."
        lines = ["TikTok videos found:"]
        for video in result[:5]:  # Limit to 5 videos
            lines.append(f"- {video.get('description', 'No description')[:100]}")
            author = video.get("author", {})
            lines.append(f"  By: @{author.get('username', 'unknown')}")
            stats = video.get("stats", {})
            lines.append(f"  Views: {stats.get('views', 0):,} | Likes: {stats.get('likes', 0):,}")
            lines.append(f"  URL: {video.get('url', 'N/A')}")
            lines.append("")
        return "\n".join(lines)

    elif tool_name == "instagram":
        if not result:
            return "No Instagram posts found."
        lines = ["Instagram posts found:"]
        for post in result[:5]:  # Limit to 5 posts
            caption = post.get("caption", "No caption")
            if len(caption) > 100:
                caption = caption[:100] + "..."
            lines.append(f"- {caption}")
            author = post.get("author", {})
            lines.append(f"  By: @{author.get('username', 'unknown')}")
            stats = post.get("stats", {})
            lines.append(f"  Likes: {stats.get('likes', 0):,} | Comments: {stats.get('comments', 0):,}")
            if post.get("location"):
                lines.append(f"  Location: {post.get('location')}")
            lines.append(f"  URL: {post.get('url', 'N/A')}")
            lines.append("")
        return "\n".join(lines)

    else:
        # Generic formatting
        if isinstance(result, (list, dict)):
            return json.dumps(result, indent=2, default=str)
        return str(result)


def _generate_fallback_response(state: ReActState, iteration: int) -> Dict[str, Any]:
    """
    Generate a fallback response when max iterations are reached.

    Args:
        state: Current ReAct state
        iteration: Current iteration number

    Returns:
        State update with fallback final response
    """
    # Compile what we know from tool calls
    tool_calls = state.get("tool_calls", [])

    if not tool_calls:
        response = "I apologize, but I wasn't able to find the information you requested. Could you please rephrase your question?"
    else:
        # Compile results from successful tool calls
        successful_results = []
        for call in tool_calls:
            if call.get("result") and not call.get("error"):
                successful_results.append(f"From {call['tool_name']}:\n{call['result']}")

        if successful_results:
            compiled_info = "\n\n".join(successful_results)
            response = f"Based on the information I gathered:\n\n{compiled_info}\n\nNote: I reached my reasoning limit, so this response may be incomplete."
        else:
            response = "I apologize, but I encountered issues while trying to find information for your request. Please try again or rephrase your question."

    return {
        "current_iteration": iteration,
        "should_stop": True,
        "final_response": response
    }
