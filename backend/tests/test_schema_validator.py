import pytest
from app.services.schema_validator import validate_research_payload, get_missing_fields

class TestSchemaValidator:
    def test_valid_payload(self):
        valid_payload = {
            "company_value_prop": "We help businesses grow",
            "product_names": ["Product A", "Product B"],
            "pricing_model": "Subscription based",
            "key_competitors": ["Competitor A", "Competitor B"],
            "company_domain": "example.com"
        }
        assert validate_research_payload(valid_payload) == True
    
    def test_missing_required_fields(self):
        invalid_payload = {
            "company_value_prop": "We help businesses grow",
            "product_names": ["Product A"]
        }
        assert validate_research_payload(invalid_payload) == False
    
    def test_get_missing_fields(self):
        partial_payload = {
            "company_value_prop": "We help businesses grow",
            "product_names": ["Product A"],
            "pricing_model": "",
            "key_competitors": [],
            "company_domain": "example.com"
        }
        missing = get_missing_fields(partial_payload)
        assert "pricing_model" in missing
        assert "key_competitors" in missing
        assert "company_value_prop" not in missing
        assert "company_domain" not in missing
    
    def test_empty_payload(self):
        empty_payload = {}
        missing = get_missing_fields(empty_payload)
        assert len(missing) == 5
        assert all(field in missing for field in [
            "company_value_prop", "product_names", "pricing_model", 
            "key_competitors", "company_domain"
        ])