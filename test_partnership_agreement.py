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
        
        # Example data for partnership agreement
        form_data = {
            "partner1_name": "Tech Innovations LLC",
            "partner2_name": "Digital Ventures Inc",
            "business_name": "TechVent Solutions",
            "business_purpose": "Development and marketing of AI-powered business solutions",
            "capital_contributions": "Partner 1: $100,000, Partner 2: $100,000",
            "profit_sharing": "50/50 split",
            "management_roles": "Partner 1: Technical Director, Partner 2: Business Director",
            "term": "5 years",
            "additional_terms": "Annual review of partnership terms"
        }
        
        print("\nGenerating Partnership Agreement...")
        result = await generator.generate_contract("partnership_agreement", form_data)
        
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