import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import requests
from datetime import datetime
import json

class ContractGenerator:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # Google API endpoint and configuration
        self.api_url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
        self.model = "gemini-1.5-flash"
        
        # Define prompt templates for different contract types
        self.prompt_templates = {
            "nda": """
            Generate a professional non-disclosure agreement with the following details:
            Disclosing Party: {disclosing_party} (use this exact name as provided)
            Receiving Party: {receiving_party} (use this exact name as provided)
            Purpose: {purpose} (use this exact text as provided)
            Term: {term} (use this exact text as provided)
            Additional Terms: {additional_terms} (use this exact text as provided)
            
            Include standard legal clauses for:
            - Definition of confidential information
            - Obligations of receiving party
            - Exclusions from confidentiality
            - Term and termination
            - Remedies for breach
            
            Format the output as a professional legal document with proper sections and formatting.
            IMPORTANT: Use all provided information exactly as entered without any modifications or corrections.
            """,
            
            "tenancy_agreement": """
            Generate a professional tenancy agreement with the following details:
            Landlord: {landlord_name} (use this exact name as provided)
            Tenant: {tenant_name} (use this exact name as provided)
            Property Address: {property_address} (use this exact address as provided)
            Rent Amount: {rent_amount} (use this exact amount as provided)
            Term: {term} (use this exact text as provided)
            Additional Terms: {additional_terms} (use this exact text as provided)
            
            Include standard legal clauses for:
            - Rent payment terms
            - Security deposit
            - Maintenance responsibilities
            - Termination conditions
            - Property use restrictions
            
            Format the output as a professional legal document with proper sections and formatting.
            IMPORTANT: Use all provided information exactly as entered without any modifications or corrections.
            """,
            
            "employment_contract": """
            Generate a professional employment contract with the following details:
            Employer: {employer_name} (use this exact name as provided)
            Employee: {employee_name} (use this exact name as provided)
            Position: {position} (use this exact title as provided)
            Salary: {salary} (use this exact amount as provided)
            Benefits: {benefits} (use this exact text as provided)
            Term: {term} (use this exact text as provided)
            Additional Terms: {additional_terms} (use this exact text as provided)
            
            Include standard legal clauses for:
            - Job responsibilities
            - Compensation and benefits
            - Confidentiality
            - Intellectual property
            - Termination conditions
            
            Format the output as a professional legal document with proper sections and formatting.
            IMPORTANT: Use all provided information exactly as entered without any modifications or corrections.
            """
        }
        
        # Define required fields for each contract type
        self.required_fields = {
            "nda": ["disclosing_party", "receiving_party", "purpose", "term"],
            "tenancy_agreement": ["landlord_name", "tenant_name", "property_address", "rent_amount", "term"],
            "employment_contract": ["employer_name", "employee_name", "position", "salary", "term"]
        }

    def validate_form_data(self, contract_type: str, form_data: Dict[str, str]) -> None:
        """Validate that all required fields are present in the form data."""
        required_fields = self.required_fields.get(contract_type, [])
        missing_fields = [field for field in required_fields if field not in form_data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

    async def generate_contract(self, contract_type: str, form_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Generate a contract using the specified template and form data.
        
        Args:
            contract_type: Type of contract to generate
            form_data: Dictionary containing the form data
            
        Returns:
            Dictionary containing the generated contract and metadata
        """
        try:
            # Validate form data
            self.validate_form_data(contract_type, form_data)
            
            # Get the appropriate prompt template
            prompt_template = self.prompt_templates.get(contract_type)
            if not prompt_template:
                raise ValueError(f"Invalid contract type: {contract_type}")
            
            # Format the prompt with the form data
            prompt = prompt_template.format(**form_data)
            
            # Prepare the request headers and data
            headers = {
                "Content-Type": "application/json"
            }
            
            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.0,
                    "maxOutputTokens": 2000
                }
            }
            
            # Make the API request
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                headers=headers,
                json=data
            )
            
            # Check for specific error responses
            if response.status_code == 400:
                error_msg = response.json().get("error", {}).get("message", "Unknown error")
                raise Exception(f"Bad request: {error_msg}")
            elif response.status_code == 401:
                raise Exception("Unauthorized. Please check your API key.")
            elif response.status_code == 403:
                raise Exception("Forbidden. Please check your API permissions.")
            elif response.status_code == 404:
                error_msg = response.json().get("error", {}).get("message", "Unknown error")
                raise Exception(f"Model not found: {error_msg}")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded. Please try again later.")
            elif response.status_code != 200:
                error_msg = response.json().get("error", {}).get("message", "Unknown error")
                raise Exception(f"API request failed: {error_msg}")
            
            # Extract the generated contract
            result = response.json()
            if "candidates" not in result or not result["candidates"]:
                raise Exception("No response from the model")
                
            contract = result["candidates"][0]["content"]["parts"][0]["text"]
            
            # Return the contract with metadata
            return {
                "contract": contract,
                "metadata": {
                    "contract_type": contract_type,
                    "generated_at": datetime.now().isoformat(),
                    "model": self.model
                }
            }
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Error generating contract: {str(e)}")

    async def send_contract_draft(self, contract_data: Dict[str, Any], backend_url: str) -> Dict[str, Any]:
        """
        Send the generated contract draft to the backend for storage and processing.
        
        Args:
            contract_data: Dictionary containing the contract and metadata
            backend_url: URL of the backend API endpoint
            
        Returns:
            Dictionary containing the backend response
        """
        try:
            # Prepare the request headers
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            # Prepare the request payload
            payload = {
                "contract": contract_data["contract"],
                "metadata": contract_data["metadata"],
                "status": "draft",
                "version": "1.0"
            }
            
            # Make the request to the backend
            response = requests.post(
                backend_url,
                headers=headers,
                json=payload
            )
            
            # Check for successful response
            if response.status_code == 201:
                return {
                    "success": True,
                    "message": "Contract draft successfully sent to backend",
                    "data": response.json()
                }
            else:
                error_msg = response.json().get("error", {}).get("message", "Unknown error")
                raise Exception(f"Backend request failed: {error_msg}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to send contract to backend: {str(e)}")
        except Exception as e:
            raise Exception(f"Error sending contract draft: {str(e)}") 