import asyncio
from contract_generator import ContractGenerator
import os
from dotenv import load_dotenv
import sys
import traceback

async def main():
    try:
        # Load environment variables
        load_dotenv()
        
        # Check if API key is set
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("Error: GOOGLE_API_KEY not found in .env file")
            sys.exit(1)
            
        print("Initializing contract generator...")
        generator = ContractGenerator()
        
        # Example data for loan agreement
        form_data = {
            "lender_name": "Capital Funding LLC",
            "borrower_name": "Startup Ventures Inc",
            "loan_amount": "$500,000",
            "interest_rate": "8% per annum",
            "repayment_terms": "Monthly installments over 5 years",
            "collateral": "Company assets and intellectual property",
            "term": "5 years",
            "additional_terms": "Early repayment allowed without penalty"
        }
        
        print("\nGenerating Loan Agreement...")
        result = await generator.generate_contract("loan_agreement", form_data)
        
        print("\nGenerated Contract:")
        print("=" * 80)
        print(result["contract"])
        print("=" * 80)
        
        print("\nMetadata:")
        print(f"Contract Type: {result['metadata']['contract_type']}")
        print(f"Generated At: {result['metadata']['generated_at']}")
        print(f"Model: {result['metadata']['model']}")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 