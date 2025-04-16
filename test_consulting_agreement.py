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
        
        # Example data for consulting agreement
        form_data = {
            "consultant_name": "Strategic Solutions Group",
            "client_name": "Enterprise Systems Inc",
            "consulting_services": "Digital transformation strategy and implementation",
            "deliverables": "Strategic roadmap, implementation plan, progress reports",
            "payment_terms": "$200 per hour, not to exceed $50,000 per month",
            "term": "6 months",
            "additional_terms": "Weekly status meetings, monthly executive summaries"
        }
        
        print("\nGenerating Consulting Agreement...")
        result = await generator.generate_contract("consulting_agreement", form_data)
        
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