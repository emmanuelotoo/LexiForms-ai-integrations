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
        
        # List available models first
        print("\nChecking available models...")
        await generator.list_available_models()
        
        # Sample form data for a tenancy agreement
        form_data = {
            "landlord_name": "John Doe",
            "tenant_name": "Jane Smith",
            "property_address": "123 Main Street, Anytown, CA 12345",
            "rent_amount": "$2,000 per month",
            "term": "12 months",
            "additional_terms": "Pets allowed with a $500 pet deposit"
        }
        
        print("\nValidating form data...")
        generator.validate_form_data("tenancy_agreement", form_data)
        
        print("\nGenerating tenancy agreement...")
        result = await generator.generate_contract("tenancy_agreement", form_data)
        
        print("\nGenerated Contract:")
        print("=" * 80)
        print(result["contract"])
        print("=" * 80)
        
        print("\nMetadata:")
        print(f"Contract Type: {result['metadata']['contract_type']}")
        print(f"Generated At: {result['metadata']['generated_at']}")
        print(f"Model: {result['metadata']['model']}")
        
    except ValueError as e:
        print(f"\nValidation Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nDetailed error information:")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 