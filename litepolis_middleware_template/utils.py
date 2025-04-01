from litepolis_database_example import DatabaseActor

DEFAULT_CONFIG = {}

def verify_user_credentials(email: str, password: str) -> bool:
    """
    Verifies if a user exists with the given email and password.

    Args:
        email: The email address to check.
        password: The password to verify.

    Returns:
        True if a user with the matching email and password exists, False otherwise.

    Note:
        This function currently performs a direct password comparison
        because the underlying DatabaseActor and User model appear to store
        passwords in plain text [cite: uploaded:litepolis_database_example/Users.py].
        This is insecure. Implement password hashing for production systems.
    """
    try:
        # Get all users from the database using the inherited method
        all_users: list[User] = DatabaseActor.read_users()

        # Iterate through the users to find a match
        for user in all_users:
            # Check if the email matches
            if user.email == email:
                # If email matches, check if the password matches (direct comparison)
                if user.password == password:
                    # Found a user with matching email and password
                    return True
                # Email matched, but password did not. No need to check further for this email.
                return False

        # If the loop completes without finding the email, the user does not exist
        return False

    except Exception as e:
        # Handle potential exceptions during database interaction
        print(f"An error occurred during credential verification: {e}")
        return False
