from email_validator import validate_email, EmailNotValidError

try:
    # Validate email
    valid = validate_email("test@example.com")
    print("Email is valid:", valid.email)
except EmailNotValidError as e:
    print("Invalid email:", str(e))
