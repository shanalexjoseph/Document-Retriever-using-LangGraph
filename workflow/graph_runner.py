from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from workflow.state_def import CourtOrderState
from workflow.nodes import (
    extract_fields,
    check_customer,
    validate_action,
    execute_action,
    reject_invalid_action,
    reject_non_customer
)
from workflow.ocr_utils import extract_text_from_pdf

graph = StateGraph(CourtOrderState)

graph.add_node("extract_fields", RunnableLambda(extract_fields))
graph.add_node("check_customer", RunnableLambda(check_customer))
graph.add_node("validate_action", RunnableLambda(validate_action))
graph.add_node("execute_action", RunnableLambda(execute_action))
graph.add_node("reject_non_customer", RunnableLambda(reject_non_customer))
graph.add_node("reject_invalid_action", RunnableLambda(reject_invalid_action))

graph.set_entry_point("extract_fields")
graph.add_edge("extract_fields", "check_customer")

graph.add_conditional_edges("check_customer", lambda state: "validate_action" if state.get("customer_id") else "reject_non_customer")
graph.add_edge("validate_action", "execute_action")
graph.add_conditional_edges("validate_action", lambda state: "execute_action" if state.get("is_valid_action") else "reject_invalid_action")

graph.add_edge("execute_action", END)
graph.add_edge("reject_invalid_action", END)
graph.add_edge("reject_non_customer", END)

workflow = graph.compile()

def run_pdf_workflow(pdf_path: str):
    text = extract_text_from_pdf(pdf_path)
    return workflow.invoke({"ocr_text": text})
