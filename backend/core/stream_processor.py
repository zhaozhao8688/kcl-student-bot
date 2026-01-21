"""Streaming chat processor using Server-Sent Events (SSE).

Streams agent execution logs to the frontend in real-time.
"""

import json
import asyncio
from typing import Optional, AsyncGenerator
from datetime import datetime
from agents.react_graph import create_react_agent_graph
from agents.react_state import create_initial_state
from services.supabase_service import supabase_service
from utils.logger import setup_logger

logger = setup_logger(__name__)


async def stream_chat(
    query: str,
    session_id: str,
    ical_url: Optional[str] = None,
    conversation_history: Optional[list] = None
) -> AsyncGenerator[str, None]:
    """
    Process a chat message and stream execution logs via SSE.

    Args:
        query: User's query message
        session_id: Session identifier
        ical_url: Optional iCal URL for timetable queries
        conversation_history: Optional list of previous messages in the conversation

    Yields:
        SSE formatted strings with log events and final response
    """
    try:
        yield _sse_event("status", {"message": "Starting agent..."})

        # Create a fresh graph for this request (to avoid state issues)
        graph = create_react_agent_graph()

        # Prepare initial state
        initial_state = create_initial_state(
            query=query,
            user_id=session_id,
            ical_url=ical_url,
            max_iterations=5,
            conversation_history=conversation_history
        )

        yield _sse_event("log", {"content": f"Processing query: {query}"})

        # Run the graph with streaming
        current_iteration = 0
        final_response = None

        # Use stream mode to get intermediate states
        async for event in _run_graph_with_events(graph, initial_state):
            event_type = event.get("type")
            data = event.get("data", {})

            if event_type == "reasoning_start":
                current_iteration = data.get("iteration", 0)
                yield _sse_event("log", {
                    "content": f"ReAct reasoning - iteration {current_iteration}/5",
                    "iteration": current_iteration
                })

            elif event_type == "thought":
                thought = data.get("thought", "")
                yield _sse_event("log", {
                    "content": f"Thought: {thought[:150]}{'...' if len(thought) > 150 else ''}",
                    "iteration": current_iteration
                })

            elif event_type == "action":
                action = data.get("action", "")
                action_input = data.get("action_input", {})
                if action == "final_answer":
                    yield _sse_event("log", {
                        "content": "Action: final_answer (generating response)",
                        "iteration": current_iteration
                    })
                else:
                    yield _sse_event("log", {
                        "content": f"Action: {action}",
                        "iteration": current_iteration,
                        "action_input": action_input
                    })

            elif event_type == "tool_start":
                tool_name = data.get("tool_name", "")
                yield _sse_event("log", {
                    "content": f"Executing tool: {tool_name}",
                    "iteration": current_iteration
                })

            elif event_type == "tool_result":
                tool_name = data.get("tool_name", "")
                success = data.get("success", False)
                if success:
                    yield _sse_event("log", {
                        "content": f"Tool {tool_name} completed successfully",
                        "iteration": current_iteration
                    })
                else:
                    error = data.get("error", "Unknown error")
                    yield _sse_event("log", {
                        "content": f"Tool {tool_name} failed: {error}",
                        "iteration": current_iteration
                    })

            elif event_type == "observation":
                obs = data.get("observation", "")
                # Truncate long observations
                if len(obs) > 200:
                    obs = obs[:200] + "..."
                yield _sse_event("log", {
                    "content": f"Observation: {obs}",
                    "iteration": current_iteration
                })

            elif event_type == "complete":
                final_response = data.get("response", "")
                iterations = data.get("iterations", 0)
                tool_calls = data.get("tool_calls", 0)
                yield _sse_event("log", {
                    "content": f"Completed in {iterations} iteration(s) with {tool_calls} tool call(s)",
                    "iteration": iterations
                })

        # Send final response
        if final_response:
            yield _sse_event("response", {"content": final_response})

            # Save to database in background
            try:
                _save_messages(session_id, query, final_response)
            except Exception as db_error:
                logger.error(f"Error saving to database: {db_error}")

        yield _sse_event("done", {"message": "Stream complete"})

    except Exception as e:
        logger.error(f"Error in stream_chat: {str(e)}", exc_info=True)
        yield _sse_event("error", {"message": str(e)})
        yield _sse_event("done", {"message": "Stream complete with error"})


async def _run_graph_with_events(graph, initial_state) -> AsyncGenerator[dict, None]:
    """
    Run the graph and yield events for each step in real-time.

    Uses LangGraph's stream() to get intermediate states as nodes complete.
    """
    from queue import Queue, Empty
    import threading

    loop = asyncio.get_running_loop()
    event_queue = Queue()
    final_result = {}

    def run_graph_streaming():
        """Run graph.stream() in a thread and push events to queue."""
        nonlocal final_result
        last_iteration = 0
        last_tool_count = 0

        try:
            for state in graph.stream(initial_state):
                # state is a dict with node name as key and updated state as value
                for node_name, node_state in state.items():
                    current_iteration = node_state.get("current_iteration", 0)

                    if node_name == "reasoning":
                        # Emit reasoning events
                        if current_iteration > last_iteration:
                            event_queue.put({
                                "type": "reasoning_start",
                                "data": {"iteration": current_iteration}
                            })
                            last_iteration = current_iteration

                        thought = node_state.get("current_thought", "")
                        if thought:
                            event_queue.put({
                                "type": "thought",
                                "data": {"thought": thought}
                            })

                        action = node_state.get("current_action", "")
                        action_input = node_state.get("current_action_input", {})
                        if action:
                            event_queue.put({
                                "type": "action",
                                "data": {"action": action, "action_input": action_input}
                            })

                    elif node_name == "tool_execution":
                        # Emit tool events
                        tool_calls = node_state.get("tool_calls", [])
                        if len(tool_calls) > last_tool_count:
                            tc = tool_calls[-1]
                            tool_name = tc.get("tool_name", "")

                            event_queue.put({
                                "type": "tool_start",
                                "data": {"tool_name": tool_name}
                            })

                            if tc.get("error"):
                                event_queue.put({
                                    "type": "tool_result",
                                    "data": {
                                        "tool_name": tool_name,
                                        "success": False,
                                        "error": tc.get("error")
                                    }
                                })
                            else:
                                event_queue.put({
                                    "type": "tool_result",
                                    "data": {"tool_name": tool_name, "success": True}
                                })

                            last_tool_count = len(tool_calls)

                    elif node_name == "observation":
                        # Emit observation
                        obs = node_state.get("current_observation", "")
                        if obs:
                            event_queue.put({
                                "type": "observation",
                                "data": {"observation": str(obs)[:300]}
                            })

                    # Track final state
                    final_result.update(node_state)

        except Exception as e:
            logger.error(f"Error in graph streaming: {e}")
            event_queue.put({"type": "error", "data": {"error": str(e)}})
        finally:
            event_queue.put(None)  # Signal completion

    # Start graph execution in thread
    thread = threading.Thread(target=run_graph_streaming)
    thread.start()

    # Yield events as they arrive
    while True:
        try:
            # Use asyncio-friendly polling
            event = await loop.run_in_executor(None, lambda: event_queue.get(timeout=0.1))

            if event is None:
                # Stream complete
                break

            yield event

        except Empty:
            # No event yet, continue polling
            if not thread.is_alive():
                # Thread finished but queue might still have events
                try:
                    while True:
                        event = event_queue.get_nowait()
                        if event is None:
                            break
                        yield event
                except Empty:
                    pass
                break

    thread.join()

    # Emit complete event
    yield {
        "type": "complete",
        "data": {
            "response": final_result.get("final_response", ""),
            "iterations": final_result.get("current_iteration", 0),
            "tool_calls": len(final_result.get("tool_calls", []))
        }
    }


def _sse_event(event_type: str, data: dict) -> str:
    """Format data as an SSE event string."""
    event_data = {
        "type": event_type,
        "timestamp": datetime.now().isoformat(),
        **data
    }
    return f"data: {json.dumps(event_data)}\n\n"


def _save_messages(session_id: str, user_message: str, assistant_message: str) -> None:
    """Save messages to database."""
    supabase_service.save_chat_message(
        user_id=session_id,
        role="user",
        content=user_message,
        session_id=session_id
    )
    supabase_service.save_chat_message(
        user_id=session_id,
        role="assistant",
        content=assistant_message,
        session_id=session_id
    )
