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
        
        # Example data for employment contract
        form_data = {
            "employer_name": "Tech Solutions Inc",
            "employee_name": "Alex Johnson",
            "position": "Senior Software Engineer",
            "salary": "$120,000 per year",
            "benefits": "Health insurance, 401k, 4 weeks vacation",
            "term": "Full-time",
            "additional_terms": "Remote work allowed, flexible hours"
        }
        
        print("\nGenerating Employment Contract...")
        result = await generator.generate_contract("employment_contract", form_data)
        
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