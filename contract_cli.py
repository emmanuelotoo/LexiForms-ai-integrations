import asyncio
from contract_generator import ContractGenerator
import os
from dotenv import load_dotenv
import sys
import traceback
from typing import Dict, Any

class ContractCLI:
    def __init__(self):
        self.generator = ContractGenerator()
        self.contract_types = {
            "1": "tenancy_agreement",
            "2": "employment_contract",
            "3": "nda",
            "4": "service_agreement",
            "5": "partnership_agreement",
            "6": "consulting_agreement",
            "7": "loan_agreement",
            "8": "software_license"
        }
        
    def display_menu(self):
        print("\nAvailable Contract Types:")
        print("1. Tenancy Agreement")
        print("2. Employment Contract")
        print("3. Non-Disclosure Agreement (NDA)")
        print("4. Service Agreement")
        print("5. Partnership Agreement")
        print("6. Consulting Agreement")
        print("7. Loan Agreement")
        print("8. Software License")
        print("0. Exit")
        
    def get_contract_type(self) -> str:
        while True:
            choice = input("\nSelect contract type (0-8): ")
            if choice == "0":
                sys.exit(0)
            if choice in self.contract_types:
                return self.contract_types[choice]
            print("Invalid choice. Please try again.")
            
    def get_tenancy_data(self) -> Dict[str, str]:
        print("\nEnter Tenancy Agreement Details:")
        return {
            "landlord_name": input("Landlord Name: "),
            "tenant_name": input("Tenant Name: "),
            "property_address": input("Property Address: "),
            "rent_amount": input("Rent Amount: "),
            "term": input("Term (e.g., 12 months): "),
            "additional_terms": input("Additional Terms (optional): ")
        }
        
    def get_employment_data(self) -> Dict[str, str]:
        print("\nEnter Employment Contract Details:")
        return {
            "employer_name": input("Employer Name: "),
            "employee_name": input("Employee Name: "),
            "position": input("Position: "),
            "salary": input("Salary: "),
            "benefits": input("Benefits: "),
            "term": input("Term (e.g., Full-time): "),
            "additional_terms": input("Additional Terms (optional): ")
        }
        
    def get_nda_data(self) -> Dict[str, str]:
        print("\nEnter NDA Details:")
        return {
            "disclosing_party": input("Disclosing Party: "),
            "receiving_party": input("Receiving Party: "),
            "purpose": input("Purpose: "),
            "term": input("Term (e.g., 5 years): "),
            "additional_terms": input("Additional Terms (optional): ")
        }
        
    def get_service_data(self) -> Dict[str, str]:
        print("\nEnter Service Agreement Details:")
        return {
            "service_provider": input("Service Provider: "),
            "client": input("Client: "),
            "service_description": input("Service Description: "),
            "scope": input("Scope: "),
            "payment_terms": input("Payment Terms: "),
            "term": input("Term: "),
            "additional_terms": input("Additional Terms (optional): ")
        }
        
    def get_partnership_data(self) -> Dict[str, str]:
        print("\nEnter Partnership Agreement Details:")
        return {
            "partner1_name": input("Partner 1 Name: "),
            "partner2_name": input("Partner 2 Name: "),
            "business_name": input("Business Name: "),
            "business_purpose": input("Business Purpose: "),
            "capital_contributions": input("Capital Contributions: "),
            "profit_sharing": input("Profit Sharing: "),
            "management_roles": input("Management Roles: "),
            "term": input("Term: "),
            "additional_terms": input("Additional Terms (optional): ")
        }
        
    def get_consulting_data(self) -> Dict[str, str]:
        print("\nEnter Consulting Agreement Details:")
        return {
            "consultant_name": input("Consultant Name: "),
            "client_name": input("Client Name: "),
            "consulting_services": input("Consulting Services: "),
            "deliverables": input("Deliverables: "),
            "payment_terms": input("Payment Terms: "),
            "term": input("Term: "),
            "additional_terms": input("Additional Terms (optional): ")
        }
        
    def get_loan_data(self) -> Dict[str, str]:
        print("\nEnter Loan Agreement Details:")
        return {
            "lender_name": input("Lender Name: "),
            "borrower_name": input("Borrower Name: "),
            "loan_amount": input("Loan Amount: "),
            "interest_rate": input("Interest Rate: "),
            "repayment_terms": input("Repayment Terms: "),
            "collateral": input("Collateral: "),
            "term": input("Term: "),
            "additional_terms": input("Additional Terms (optional): ")
        }
        
    def get_software_license_data(self) -> Dict[str, str]:
        print("\nEnter Software License Details:")
        return {
            "licensor_name": input("Licensor Name: "),
            "licensee_name": input("Licensee Name: "),
            "software_name": input("Software Name: "),
            "license_type": input("License Type: "),
            "number_of_users": input("Number of Users: "),
            "license_fee": input("License Fee: "),
            "term": input("Term: "),
            "additional_terms": input("Additional Terms (optional): ")
        }
        
    def get_form_data(self, contract_type: str) -> Dict[str, str]:
        data_getters = {
            "tenancy_agreement": self.get_tenancy_data,
            "employment_contract": self.get_employment_data,
            "nda": self.get_nda_data,
            "service_agreement": self.get_service_data,
            "partnership_agreement": self.get_partnership_data,
            "consulting_agreement": self.get_consulting_data,
            "loan_agreement": self.get_loan_data,
            "software_license": self.get_software_license_data
        }
        return data_getters[contract_type]()
        
    async def run(self):
        try:
            # Load environment variables
            load_dotenv()
            
            # Check if API key is set
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                print("Error: GOOGLE_API_KEY not found in .env file")
                sys.exit(1)
                
            while True:
                self.display_menu()
                contract_type = self.get_contract_type()
                form_data = self.get_form_data(contract_type)
                
                print("\nGenerating contract...")
                result = await self.generator.generate_contract(contract_type, form_data)
                
                print("\nGenerated Contract:")
                print("=" * 80)
                print(result["contract"])
                print("=" * 80)
                
                print("\nMetadata:")
                print(f"Contract Type: {result['metadata']['contract_type']}")
                print(f"Generated At: {result['metadata']['generated_at']}")
                print(f"Model: {result['metadata']['model']}")
                
                if input("\nGenerate another contract? (y/n): ").lower() != 'y':
                    break
                    
        except Exception as e:
            print(f"\nError: {str(e)}")
            print(traceback.format_exc())
            sys.exit(1)

if __name__ == "__main__":
    cli = ContractCLI()
    asyncio.run(cli.run()) 