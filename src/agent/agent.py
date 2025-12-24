"""Email agent workflow graph definition.

This module defines the LangGraph workflow for processing emails:
- read_email: reads incoming email content
- classify_intent: determines the type of request
- search_documentation: searches relevant docs
- bug_tracking: handles bug-related requests
- draft_response: generates reply drafts
- human_review: allows human oversight
- send_reply: sends the final response
"""

from langgraph.graph import START, END, StateGraph
from langgraph.types import RetryPolicy

from agent.utils.state import EmailAgentState
from agent.utils.nodes import (
    read_email,
    classify_intent,
    search_documentation,
    bug_tracking,
    draft_response,
    human_review,
    send_reply,
)

# Create the graph
workflow = StateGraph(EmailAgentState)

# Add nodes with appropriate error handling
workflow.add_node("read_email", read_email)
workflow.add_node("classify_intent", classify_intent)

# Add retry policy for nodes that might have transient failures
workflow.add_node(
    "search_documentation",
    search_documentation,
    retry_policy=RetryPolicy(max_attempts=3)
)
workflow.add_node("bug_tracking", bug_tracking)
workflow.add_node("draft_response", draft_response)
workflow.add_node("human_review", human_review)
workflow.add_node("send_reply", send_reply)

# Add only the essential edges
workflow.add_edge(START, "read_email")
workflow.add_edge("read_email", "classify_intent")
workflow.add_edge("send_reply", END)

# Compile without custom checkpointer; LangGraph Server will handle persistence
app = workflow.compile()
