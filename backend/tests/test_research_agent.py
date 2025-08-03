import pytest
from app.services.research_agent import DeepResearchAgent

class TestResearchAgent:
    def setup_method(self):
        self.agent = DeepResearchAgent()
    
    def test_extract_domain_from_email(self):
        assert self.agent.extract_domain_from_email("test@example.com") == "example.com"
        assert self.agent.extract_domain_from_email("user@company.org") == "company.org"
        assert self.agent.extract_domain_from_email("invalid-email") == ""
        assert self.agent.extract_domain_from_email("") == ""
    
    def test_clean_text(self):
        dirty_text = "  This   is    some  \n\n  messy    text  "
        cleaned = self.agent.clean_text(dirty_text)
        assert cleaned == "This is some messy text"
    
    def test_agent_replanning_edge_case(self):
        results = [
            {"title": "Test", "url": "http://test.com", "snippet": "No competitor information found"}
        ]
        missing_fields = ["key_competitors"]
        extracted = self.agent.extract_info_from_results(results, missing_fields)
        
        assert "key_competitors" not in extracted or not extracted.get("key_competitors")
    
    def test_extract_info_from_results(self):
        results = [
            {
                "title": "Company Overview",
                "url": "http://example.com/about",
                "snippet": "Our mission is to help businesses grow with innovative software solutions."
            },
            {
                "title": "Pricing Information", 
                "url": "http://example.com/pricing",
                "snippet": "Our pricing model is subscription based with monthly and annual plans."
            }
        ]
        missing_fields = ["company_value_prop", "pricing_model"]
        extracted = self.agent.extract_info_from_results(results, missing_fields)
        
        assert "company_value_prop" in extracted
        assert "pricing_model" in extracted
        assert "grow" in extracted["company_value_prop"].lower()
        assert "subscription" in extracted["pricing_model"].lower()