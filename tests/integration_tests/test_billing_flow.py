from langgraph.types import Command

from agent.agent import app


def test_urgent_billing_flow_pauses_and_resumes() -> None:
    initial_state = {
        "email_content": "I was charged twice for my subscription! This is urgent!",
        "sender_email": "customer@example.com",
        "email_id": "email_123",
        "messages": [],
    }
    config = {"configurable": {"thread_id": "customer_123"}}

    # First invoke should pause at human_review
    result = app.invoke(initial_state, config)
    assert "__interrupt__" in result

    # Resume with human input
    human_response = Command(
        resume={
            "approved": True,
            "edited_response": "We sincerely apologize for the double charge. I've initiated an immediate refund...",
        }
    )
    final_result = app.invoke(human_response, config)
    assert final_result is not None
