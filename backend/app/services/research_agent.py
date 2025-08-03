import re
from uuid import UUID
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Person, Company, ContextSnippet, SearchLog
from app.services.search_provider import get_search_provider
from app.services.schema_validator import validate_research_payload, get_missing_fields

class DeepResearchAgent:
    def __init__(self):
        self.search_provider = get_search_provider()
        self.max_iterations = 3
        
    def extract_domain_from_email(self, email: str) -> str:
        if "@" in email:
            return email.split("@")[1]
        return ""
    
    def clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    
    def extract_info_from_results(self, results: List[Dict], missing_fields: List[str]) -> Dict[str, Any]:
        extracted = {}
        
        for result in results:
            snippet = result.get("snippet", "").lower()
            title = result.get("title", "").lower()
            
            if "company_value_prop" in missing_fields:
                if any(keyword in snippet for keyword in ["mission", "value", "proposition", "helps", "provides"]):
                    extracted["company_value_prop"] = self.clean_text(result.get("snippet", ""))
            
            if "product_names" in missing_fields:
                if any(keyword in snippet for keyword in ["product", "software", "platform", "solution"]):
                    products = re.findall(r'\b[A-Z][a-zA-Z]{2,}\b', result.get("snippet", ""))
                    if products:
                        extracted["product_names"] = list(set(products[:3]))
            
            if "pricing_model" in missing_fields:
                if any(keyword in snippet for keyword in ["pricing", "price", "cost", "subscription", "free"]):
                    extracted["pricing_model"] = self.clean_text(result.get("snippet", ""))
            
            if "key_competitors" in missing_fields:
                if any(keyword in snippet for keyword in ["competitor", "alternative", "vs", "compared"]):
                    competitors = re.findall(r'\b[A-Z][a-zA-Z]{2,}\b', result.get("snippet", ""))
                    if competitors:
                        extracted["key_competitors"] = list(set(competitors[:3]))
        
        return extracted
    
    def generate_search_query(self, person: Person, company: Company, missing_fields: List[str], iteration: int) -> str:
        base_query = f"{company.name or ''} {company.domain or ''}"
        
        if iteration == 1:
            return f"{base_query} company overview"
        elif iteration == 2:
            if "pricing_model" in missing_fields:
                return f"{base_query} pricing plans cost"
            elif "key_competitors" in missing_fields:
                return f"{base_query} competitors alternatives"
            else:
                return f"{base_query} products services"
        else:
            field_specific = missing_fields[0] if missing_fields else "information"
            return f"{base_query} {field_specific}"
    
    def enrich_person(self, person_id: UUID) -> Dict[str, Any]:
        db = SessionLocal()
        try:
            person = db.query(Person).filter(Person.id == person_id).first()
            if not person:
                return {"error": "Person not found"}
            
            company = db.query(Company).filter(Company.id == person.company_id).first()
            if not company:
                return {"error": "Company not found"}
            
            if not company.domain and person.email:
                company.domain = self.extract_domain_from_email(person.email)
                db.commit()
            
            research_data = {
                "company_value_prop": "",
                "product_names": [],
                "pricing_model": "",
                "key_competitors": [],
                "company_domain": company.domain or ""
            }
            
            context_snippet = ContextSnippet(
                entity_type="company",
                entity_id=company.id,
                snippet_type="research",
                payload=research_data,
                source_urls=[]
            )
            db.add(context_snippet)
            db.commit()
            db.refresh(context_snippet)
            
            all_source_urls = []
            
            for iteration in range(1, self.max_iterations + 1):
                print(f"Starting iteration {iteration} for person {person_id}")
                
                missing_fields = get_missing_fields(research_data)
                if not missing_fields:
                    break
                
                query = self.generate_search_query(person, company, missing_fields, iteration)
                print(f"Search query: {query}")
                
                results = self.search_provider.search(query)
                
                search_log = SearchLog(
                    context_snippet_id=context_snippet.id,
                    iteration=iteration,
                    query=query,
                    top_results={"results": results}
                )
                db.add(search_log)
                
                source_urls = [r.get("url", "") for r in results]
                all_source_urls.extend(source_urls)
                
                extracted_info = self.extract_info_from_results(results, missing_fields)
                
                for key, value in extracted_info.items():
                    if value and not research_data[key]:
                        research_data[key] = value
                
                db.commit()
            
            research_data["company_domain"] = company.domain or ""
            context_snippet.payload = research_data
            context_snippet.source_urls = list(set(all_source_urls))
            
            if validate_research_payload(research_data):
                print("Research data validation passed")
            else:
                print("Research data validation failed")
            
            db.commit()
            
            return {
                "success": True,
                "person_id": str(person_id),
                "company_id": str(company.id),
                "snippet_id": str(context_snippet.id),
                "research_data": research_data
            }
            
        except Exception as e:
            db.rollback()
            print(f"Error in research agent: {e}")
            return {"error": str(e)}
        finally:
            db.close()

def enrich_person(person_id: UUID):
    agent = DeepResearchAgent()
    return agent.enrich_person(person_id)