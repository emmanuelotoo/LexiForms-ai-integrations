# Contract Generation API Integration Documentation

## Overview
This document outlines the contract generation service's API integration requirements for the backend team. The service generates legal contracts using AI and needs to send the generated contracts to your backend for storage and processing.

## API Endpoint Requirements

### Contract Submission Endpoint
- **URL**: `[Your Backend URL]/contracts`
- **Method**: POST
- **Content-Type**: application/json
- **Authentication**: [Specify required authentication method]

## Request Format

### Headers
```json
{
  "Content-Type": "application/json",
  "Accept": "application/json",
  "Authorization": "[Your Auth Method]"
}
```

### Request Body
```json
{
  "contract": "Generated contract text with proper formatting",
  "metadata": {
    "contract_type": "tenancy_agreement|employment_contract|nda",
    "generated_at": "ISO 8601 timestamp",
    "model": "gemini-1.5-flash"
  },
  "status": "draft",
  "version": "1.0"
}
```

### Field Descriptions
- **contract**: The complete generated contract text
- **metadata.contract_type**: Type of contract generated
- **metadata.generated_at**: Timestamp of contract generation
- **metadata.model**: AI model used for generation
- **status**: Current status of the contract (always "draft" for new contracts)
- **version**: Version of the contract format

## Response Format

### Success Response (201 Created)
```json
{
  "id": "unique-contract-identifier",
  "status": "draft",
  "created_at": "ISO 8601 timestamp",
  "url": "URL to access the contract"
}
```

### Error Responses
```json
{
  "error": {
    "code": "error_code",
    "message": "Human-readable error message",
    "details": {
      "field": "specific field causing error",
      "reason": "detailed error reason"
    }
  }
}
```

## Error Codes
- **400**: Bad Request - Invalid input data
- **401**: Unauthorized - Authentication failed
- **403**: Forbidden - Insufficient permissions
- **404**: Not Found - Resource not found
- **409**: Conflict - Contract already exists
- **429**: Too Many Requests - Rate limit exceeded
- **500**: Internal Server Error - Server-side error

## Rate Limiting
- [Specify rate limits if applicable]
- [Specify rate limit headers if used]

## Security Requirements
- [Specify any specific security requirements]
- [Specify any data encryption requirements]

## Additional Notes
1. All timestamps should be in ISO 8601 format
2. Contract text should preserve exact input values
3. Error responses should include detailed error messages
4. The service expects a 201 status code for successful creation

## Questions for Backend Team
1. What is the exact endpoint URL?
2. What authentication method should be used?
3. Are there any additional fields required in the request?
4. What specific error codes and messages should be handled?
5. Are there any rate limiting requirements?
6. Are there any specific security requirements?
7. Should the contract be stored in any specific format?
8. Are there any specific validation requirements for the contract text?

## Example Usage
```python
# Example request
POST /contracts
{
  "contract": "This Agreement is made on [date] between [landlord] and [tenant]...",
  "metadata": {
    "contract_type": "tenancy_agreement",
    "generated_at": "2024-03-14T12:00:00Z",
    "model": "gemini-1.5-flash"
  },
  "status": "draft",
  "version": "1.0"
}

# Example success response
{
  "id": "contract-12345",
  "status": "draft",
  "created_at": "2024-03-14T12:00:01Z",
  "url": "https://api.example.com/contracts/contract-12345"
}
``` 