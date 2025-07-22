from typing import TypedDict, Optional

class CourtOrderState(TypedDict):
    ocr_text: str
    national_id: Optional[str]
    action: Optional[str]
    customer_id: Optional[str]
    is_valid_action: Optional[bool]
    result: Optional[str]
