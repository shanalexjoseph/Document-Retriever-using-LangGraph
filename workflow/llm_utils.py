import json, ast
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

CATEGORIES = ["freeze_funds", "release_funds"]
CATEGORY_EMBEDS = model.encode(CATEGORIES, convert_to_tensor=True)

def normalize_action(action_text):
    if not action_text:
        return "unknown"
    action_emb = model.encode(action_text, convert_to_tensor=True)
    sim_scores = util.pytorch_cos_sim(action_emb, CATEGORY_EMBEDS)[0]
    best_score, best_idx = sim_scores.max(0)
    return CATEGORIES[best_idx] if best_score >= 0.75 else "unknown"

def parse_output(output_text):
    data = None
    if isinstance(output_text, str):
        try:
            data = json.loads(output_text)
        except json.JSONDecodeError:
            try:
                data = ast.literal_eval(output_text)
            except Exception:
                return None, None
    elif isinstance(output_text, (dict, list, tuple)):
        data = output_text

    if isinstance(data, (list, tuple)) and len(data) > 0 and isinstance(data[0], dict):
        data = data[0]

    if not isinstance(data, dict):
        return None, None

    national_id = data.get("national_id", "")
    action = data.get("action", "")

    return national_id, action

def classify_action_from_output(output_text):
    national_id, action_text = parse_output(output_text)
    national_id = national_id.strip() if national_id else ""
    action_text = action_text.strip() if action_text else ""
    mapped_action = normalize_action(action_text)
    return {
        "national_id": national_id,
        "action": mapped_action
    }
