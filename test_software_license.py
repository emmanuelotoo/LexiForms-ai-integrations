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
        
        # Example data for software license
        form_data = {
            "licensor_name": "TechSoft Solutions Inc",
            "licensee_name": "Enterprise Systems Corp",
            "software_name": "Enterprise Resource Planning Suite",
            "license_type": "Enterprise License",
            "number_of_users": "500 concurrent users",
            "license_fee": "$100,000 per year",
            "term": "3 years",
            "additional_terms": "Includes technical support and updates"
        }
        
        print("\nGenerating Software License Agreement...")
        result = await generator.generate_contract("software_license", form_data)
        
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