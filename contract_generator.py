import os
from typing import Dict, Any, Optional
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.api_core import exceptions as google_exceptions
import json
from datetime import datetime

class ContractGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the contract generator with Google Gemini API key."""
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key is required")
        
        try:
            genai.configure(api_key=self.api_key)
            # Initialize the model with the correct model name
            self.model = genai.GenerativeModel('models/gemini-1.5-pro')
        except Exception as e:
            raise ValueError(f"Failed to initialize Gemini model: {str(e)}")
        
        # Model configuration
        self.model_config = {
            "temperature": 0.3,  # Lower temperature for more consistent output
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 2000,
        }
        
        # Load prompt templates
        self.prompt_templates = self._load_prompt_templates()

    def _load_prompt_templates(self) -> Dict[str, str]:
        """Load prompt templates for different contract types."""
        return {
            "tenancy_agreement": """
            Generate a legally sound tenancy agreement with the following details:
            - Landlord: {landlord_name}
            - Tenant: {tenant_name}
            - Property Address: {property_address}
            - Rent Amount: {rent_amount}
            - Term: {term}
            - Additional Terms: {additional_terms}
            
            Please ensure the agreement includes:
            1. Standard tenancy clauses
            2. Rent payment terms
            3. Property maintenance responsibilities
            4. Termination conditions
            5. Any additional terms specified
            
            Format the output in clear, professional language suitable for legal documents.
            """,
            "employment_contract": """
            Generate a comprehensive employment contract with the following details:
            - Employer: {employer_name}
            - Employee: {employee_name}
            - Position: {position}
            - Salary: {salary}
            - Benefits: {benefits}
            - Term: {term}
            - Additional Terms: {additional_terms}
            
            Please ensure the contract includes:
            1. Job responsibilities
            2. Compensation and benefits
            3. Working hours
            4. Confidentiality clauses
            5. Termination conditions
            6. Any additional terms specified
            
            Format the output in clear, professional language suitable for legal documents.
            """,
            "nda": """
            Generate a non-disclosure agreement with the following details:
            - Disclosing Party: {disclosing_party}
            - Receiving Party: {receiving_party}
            - Purpose: {purpose}
            - Term: {term}
            - Additional Terms: {additional_terms}
            
            Please ensure the NDA includes:
            1. Definition of confidential information
            2. Obligations of the receiving party
            3. Exclusions from confidentiality
            4. Term and termination
            5. Any additional terms specified
            
            Format the output in clear, professional language suitable for legal documents.
            """,
            "service_agreement": """
            Generate a professional service agreement with the following details:
            - Service Provider: {provider_name}
            - Client: {client_name}
            - Services: {services}
            - Payment Terms: {payment_terms}
            - Term: {term}
            - Additional Terms: {additional_terms}
            
            Please ensure the agreement includes:
            1. Scope of services
            2. Payment schedule and terms
            3. Service delivery timeline
            4. Quality standards
            5. Termination conditions
            6. Any additional terms specified
            
            Format the output in clear, professional language suitable for legal documents.
            """,
            "partnership_agreement": """
            Generate a comprehensive partnership agreement with the following details:
            - Partner 1: {partner1_name}
            - Partner 2: {partner2_name}
            - Business Name: {business_name}
            - Capital Contributions: {capital_contributions}
            - Profit Sharing: {profit_sharing}
            - Additional Terms: {additional_terms}
            
            Please ensure the agreement includes:
            1. Business purpose and structure
            2. Capital contributions and profit sharing
            3. Management and decision-making
            4. Partner responsibilities
            5. Dispute resolution
            6. Any additional terms specified
            
            Format the output in clear, professional language suitable for legal documents.
            """,
            "consulting_agreement": """
            Generate a consulting agreement with the following details:
            - Consultant: {consultant_name}
            - Client: {client_name}
            - Services: {services}
            - Compensation: {compensation}
            - Term: {term}
            - Additional Terms: {additional_terms}
            
            Please ensure the agreement includes:
            1. Scope of consulting services
            2. Compensation and payment terms
            3. Deliverables and timelines
            4. Confidentiality provisions
            5. Intellectual property rights
            6. Any additional terms specified
            
            Format the output in clear, professional language suitable for legal documents.
            """,
            "loan_agreement": """
            Generate a loan agreement with the following details:
            - Lender: {lender_name}
            - Borrower: {borrower_name}
            - Loan Amount: {loan_amount}
            - Interest Rate: {interest_rate}
            - Repayment Terms: {repayment_terms}
            - Additional Terms: {additional_terms}
            
            Please ensure the agreement includes:
            1. Loan amount and purpose
            2. Interest rate and calculation
            3. Repayment schedule
            4. Default conditions
            5. Security/collateral details
            6. Any additional terms specified
            
            Format the output in clear, professional language suitable for legal documents.
            """,
            "software_license": """
            Generate a software license agreement with the following details:
            - Licensor: {licensor_name}
            - Licensee: {licensee_name}
            - Software: {software_name}
            - License Type: {license_type}
            - Term: {term}
            - Additional Terms: {additional_terms}
            
            Please ensure the agreement includes:
            1. License grant and restrictions
            2. Usage rights and limitations
            3. Maintenance and support
            4. Intellectual property rights
            5. Termination conditions
            6. Any additional terms specified
            
            Format the output in clear, professional language suitable for legal documents.
            """
        }

    async def list_available_models(self):
        """List all available models and their supported methods."""
        try:
            models = genai.list_models()
            print("\nAvailable Models:")
            for model in models:
                print(f"\nModel: {model.name}")
                print(f"Supported Methods: {model.supported_generation_methods}")
        except Exception as e:
            print(f"Error listing models: {str(e)}")

    def _should_retry(self, exception):
        """Determine if the exception should trigger a retry."""
        return isinstance(exception, (google_exceptions.ResourceExhausted, 
                                   google_exceptions.ServiceUnavailable,
                                   google_exceptions.DeadlineExceeded))

    @retry(stop=stop_after_attempt(3), 
           wait=wait_exponential(multiplier=1, min=4, max=10),
           retry=retry_if_exception_type((google_exceptions.ResourceExhausted, 
                                        google_exceptions.ServiceUnavailable,
                                        google_exceptions.DeadlineExceeded)))
    async def generate_contract(self, contract_type: str, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a contract based on the contract type and form data.
        
        Args:
            contract_type: Type of contract to generate (e.g., 'tenancy_agreement', 'employment_contract', 'nda')
            form_data: Dictionary containing the form data to populate the contract
            
        Returns:
            Dictionary containing the generated contract and metadata
        """
        try:
            if contract_type not in self.prompt_templates:
                raise ValueError(f"Unsupported contract type: {contract_type}")

            # Build the prompt
            prompt = self.prompt_templates[contract_type].format(**form_data)
            
            # Generate the contract
            response = await self.model.generate_content_async(
                prompt,
                generation_config=genai.types.GenerationConfig(**self.model_config)
            )
            
            if not response.text:
                raise ValueError("Empty response from Gemini model")
                
            # Extract the generated contract
            generated_contract = response.text
            
            return {
                "contract": generated_contract,
                "metadata": {
                    "contract_type": contract_type,
                    "generated_at": datetime.utcnow().isoformat(),
                    "model": "models/gemini-1.5-pro",
                    "parameters": self.model_config
                }
            }
            
        except google_exceptions.PermissionDenied:
            raise Exception("API key is invalid or unauthorized. Please check your API key.")
        except google_exceptions.ResourceExhausted:
            raise Exception("API quota exceeded. Please try again later or check your quota limits.")
        except google_exceptions.ServiceUnavailable:
            raise Exception("Service temporarily unavailable. Please try again later.")
        except google_exceptions.DeadlineExceeded:
            raise Exception("Request timed out. Please try again.")
        except google_exceptions.InvalidArgument as e:
            raise Exception(f"Invalid request: {str(e)}")
        except Exception as e:
            raise Exception(f"Error generating contract: {str(e)}")

    def validate_form_data(self, contract_type: str, form_data: Dict[str, Any]) -> bool:
        """
        Validate the form data for the specified contract type.
        
        Args:
            contract_type: Type of contract
            form_data: Form data to validate
            
        Returns:
            True if valid, raises ValueError if invalid
        """
        required_fields = {
            "tenancy_agreement": ["landlord_name", "tenant_name", "property_address", "rent_amount", "term"],
            "employment_contract": ["employer_name", "employee_name", "position", "salary", "term"],
            "nda": ["disclosing_party", "receiving_party", "purpose", "term"],
            "service_agreement": ["provider_name", "client_name", "services", "payment_terms", "term"],
            "partnership_agreement": ["partner1_name", "partner2_name", "business_name", "capital_contributions", "profit_sharing"],
            "consulting_agreement": ["consultant_name", "client_name", "services", "compensation", "term"],
            "loan_agreement": ["lender_name", "borrower_name", "loan_amount", "interest_rate", "repayment_terms"],
            "software_license": ["licensor_name", "licensee_name", "software_name", "license_type", "term"]
        }
        
        if contract_type not in required_fields:
            raise ValueError(f"Unsupported contract type: {contract_type}")
            
        missing_fields = [field for field in required_fields[contract_type] if field not in form_data]
        if missing_fields:
            raise ValueError(f"Missing required fields for {contract_type}: {', '.join(missing_fields)}")
            
        return True 