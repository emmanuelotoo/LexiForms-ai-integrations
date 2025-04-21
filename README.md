# AI Contract Generation System

This system provides AI-powered contract generation capabilities, supporting various types of legal documents including tenancy agreements, employment contracts, NDAs, and more.

## Features

- Dynamic contract generation based on user input
- Support for multiple contract types:
  - Non-Disclosure Agreement (NDA)
  - Tenancy Agreement
  - Employment Contract
  - Service Agreement
  - Software License
  - Partnership Agreement
  - Loan Agreement
  - Consulting Agreement
- Built-in validation of form data
- Retry mechanism for API stability
- Configurable model parameters
- Command-line interface for easy usage
- Comprehensive test suite

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root with:
```
GOOGLE_API_KEY='your-api-key-here'
```

## Usage

### Python API

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

### Command Line Interface

The system includes a CLI for easy contract generation:

```bash
python contract_cli.py --type tenancy_agreement --data '{"landlord_name": "John Doe", "tenant_name": "Jane Smith"}'
```

## Testing

The project includes a comprehensive test suite. Run all tests with:

```bash
python test_all_contracts.py
```

Individual contract tests can be run separately:
- `test_tenancy_agreement.py`
- `test_employment_contract.py`
- `test_nda.py`
- `test_service_agreement.py`
- `test_software_license.py`
- `test_partnership_agreement.py`
- `test_loan_agreement.py`
- `test_consulting_agreement.py`

## Model Configuration

The system uses Google's Gemini 1.5 Flash model with the following default parameters:
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
- Detailed logging for debugging

## Documentation

For detailed API documentation, see `backend_api_documentation.md`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 