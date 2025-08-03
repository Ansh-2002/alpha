import jsonschema
from typing import Dict, Any

RESEARCH_SCHEMA = {
    "type": "object",
    "properties": {
        "company_value_prop": {"type": "string"},
        "product_names": {
            "type": "array",
            "items": {"type": "string"}
        },
        "pricing_model": {"type": "string"},
        "key_competitors": {
            "type": "array", 
            "items": {"type": "string"}
        },
        "company_domain": {"type": "string"}
    },
    "required": [
        "company_value_prop",
        "product_names", 
        "pricing_model",
        "key_competitors",
        "company_domain"
    ],
    "additionalProperties": True
}

def validate_research_payload(payload: Dict[str, Any]) -> bool:
    try:
        jsonschema.validate(payload, RESEARCH_SCHEMA)
        return True
    except jsonschema.ValidationError as e:
        print(f"Schema validation error: {e}")
        return False

def get_missing_fields(payload: Dict[str, Any]) -> list:
    missing_fields = []
    required_fields = RESEARCH_SCHEMA["required"]
    
    for field in required_fields:
        if field not in payload or not payload[field]:
            missing_fields.append(field)
    
    return missing_fields