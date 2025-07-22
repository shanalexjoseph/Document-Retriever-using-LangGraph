import pandas as pd
from workflow.llm_utils import classify_action_from_output
from workflow.ocr_utils import extract_text_from_pdf
from workflow.state_def import CourtOrderState
import os


from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(token=HF_TOKEN)


actions_df = pd.read_csv(os.path.join("data", "actions.csv"))
valid_actions = {
    "freeze_funds": lambda cid: f"Freeze all funds in the customer account {cid}",
    "release_funds": lambda cid: f"Release all held or restricted funds back to the customer account {cid}."
}

def extract_fields(state: CourtOrderState) -> CourtOrderState:
    document_text = state['ocr_text']
    prompt = f"""
    You are a document parser. From the following text, extract:
    1. The 12-digit National ID, if available.
    2. The Action, which must be one of the following: "freeze_funds", "release_funds"

    Return only this JSON format:
    {{
      "national_id": "<12-digit National ID or null>",
      "action": "freeze_funds" or "release_funds"
    }}

    Do not invent new actions. Only use "freeze_funds" or "release_funds".

    Document:
    \"\"\"{document_text}\"\"\"
    """
    completion = client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.3",
        messages=[{"role": "user", "content": prompt}]
    )
    extracted = classify_action_from_output(completion.choices[0].message.content)
    return {**state, **extracted}

def check_customer(state: CourtOrderState) -> CourtOrderState:
    customers = pd.read_csv(os.path.join("data", "customers.csv"))
    national_id = state.get("national_id")
    customers["national_id"] = customers["national_id"].astype(str).str.strip()
    match = customers[customers["national_id"] == national_id]
    return {**state, "customer_id": match.iloc[0]["customer_id"] if not match.empty else None}

def validate_action(state: CourtOrderState) -> CourtOrderState:
    return {**state, "is_valid_action": state["action"] in valid_actions}

def execute_action(state: CourtOrderState) -> CourtOrderState:
    result = valid_actions[state["action"]](state["customer_id"])
    return {**state, "result": result}

def reject_non_customer(state: CourtOrderState) -> CourtOrderState:
    return {**state, "result": "Rejected: Not a valid bank customer."}

def reject_invalid_action(state: CourtOrderState) -> CourtOrderState:
    return {**state, "result": f"Rejected: Unknown action '{state['action']}'"}
