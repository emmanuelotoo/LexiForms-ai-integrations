# AI Contract Generation System

This system provides AI-powered contract generation capabilities, supporting various types of legal documents including tenancy agreements, employment contracts, and NDAs.

## Features

- Dynamic contract generation based on user input
- Support for multiple contract types
- Built-in validation of form data
- Retry mechanism for API stability
- Configurable model parameters

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export GOOGLE_API_KEY='your-api-key-here'
```

## Usage

```python
from contract_generator import ContractGenerator

# Initialize the generator
generator = ContractGenerator()

# Example form data for a tenancy agreement
form_data = {
    "landlord_name": "John Doe",
    "tenant_name": "Jane Smith",
    "property_address": "123 Main St, City, Country",
    "rent_amount": "$1500/month",
    "term": "12 months",
    "additional_terms": "Pets allowed with additional deposit"
}

# Generate the contract
try:
    result = await generator.generate_contract("tenancy_agreement", form_data)
    print(result["contract"])
except Exception as e:
    print(f"Error: {str(e)}")
```

## Contract Types

The system currently supports the following contract types:
- Tenancy Agreement
- Employment Contract
- Non-Disclosure Agreement (NDA)

## Model Configuration

The system uses Google's Gemini Pro model with the following default parameters:
- Temperature: 0.3
- Max Output Tokens: 2000
- Top P: 0.9
- Top K: 40

These parameters can be adjusted in the `ContractGenerator` class initialization.

## Error Handling

The system includes:
- Automatic retry mechanism for API calls
- Form data validation
- Comprehensive error messages
- Exception handling for API errors 