import re

def generate_tenancy_agreement(template_path, output_path, placeholders):
    """
    Generate a tenancy agreement by replacing placeholders in the template.

    :param template_path: Path to the template file.
    :param output_path: Path to save the generated agreement.
    :param placeholders: Dictionary of placeholder values.
    """
    try:
        # Read the template file
        with open(template_path, 'r') as template_file:
            content = template_file.read()

        # Replace placeholders with provided values
        for placeholder, value in placeholders.items():
            content = re.sub(rf"\[{placeholder}\]", value, content)

        # Write the generated agreement to the output file
        with open(output_path, 'w') as output_file:
            output_file.write(content)

        print(f"Tenancy agreement generated successfully: {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Example usage
    template_path = r"c:\Users\eotoo\projects\legal--ai-ai-integrations-\tenancy_agreement\sample3.txt"
    output_path = r"c:\Users\eotoo\projects\legal--ai-ai-integrations-\tenancy_agreement\generated_agreement.txt"

    # Replace these with actual values
    placeholders = {
        "Day": "12",
        "Month": "April",
        "Year": "2025",
        "Landlord's Full Name": "John Doe",
        "Landlord's Address": "123 Main Street, Accra",
        "Tenant's Full Name": "Jane Smith",
        "Tenant's Address": "456 Elm Street, Kumasi",
        "Property Address": "789 Pine Avenue, Tema",
        "Number": "3",
        "Start Date": "April 15, 2025",
        "End Date": "April 15, 2026",
        "Rent Amount in Figures": "1500",
        "Rent Amount in Words": "One Thousand Five Hundred",
        "Deposit Amount in Figures": "3000",
        "Deposit Amount in Words": "Three Thousand",
        "Payment Address": "Landlord's Bank Account",
        "Method of Payment": "Bank Transfer",
        "Notice Period": "30",
        "Other Utilities": "Internet"
    }

    generate_tenancy_agreement(template_path, output_path, placeholders)