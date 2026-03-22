from django.db.models import TextChoices


class ResponseMessages(TextChoices):
    # General
    insecure_password = (
        "Insecure password! Must contain minimum of 8 characters, an uppercase, a lowercase, a number, and a symbol"
    )
    email_already_exist = "Account with email already exists."
    user_email_already_verified = "Account email already verified."
    invalid_email = "Invalid Email."
    too_many_attempts_account_blocked = "Too many attempts. Account blocked"
    invalid_credentials = "Invalid Email/Password."
    reset_password_email_sent = "Instructions to reset your password have been sent to your email."
    verification_link_sent_to_email = "Instructions for verification has been sent to your email"
    incorrect_password = "Incorrect password."
    old_and_new_password_cannot_be_same = "Old and New password can't be the same."
    successful_password_change = "Password changed successfully."
    invalid_token_retry_login = "The token is invalid or expired. Please login again."
    user_not_recognized = "User not recognized"
    user_created_successfully = "User created successfully."
    user_updated_successfully = "User updated successfully."
    otp_sent_to_email = "An OTP has been sent to your email address."
    invalid_or_expired_otp = "Invalid/Expired OTP."
    valid_otp = "OTP verification was successful."
    password_mismatch = "Password mismatch."
    too_many_failed_otp_verification_attempts = "Too many failed OTP attempts. Request a new OTP."
    otp_already_verified = "OTP already verified."
    invalid_file = "A valid file is required"
    invalid_file_extension = "File extension not supported"
    file_too_large = "File too large"
    invalid_action = "Invalid action."
    invalid_input = "Invalid input."
    invalid_phone_number = "Invalid Phone Number."
    update_successful = "Update Successful."
    verification_successful = "Email Verification Successful. ✅"
    verification_unsuccessful = "Email Verification Unsuccessful. The token is invalid or expired. ❌"
    login_successful = "Login Successful."
    logout_successful = "Logout Successful."
    media_type_not_found = "Media Type not found."
    media_not_found = "Media not found."
    token_expired = "Not Authorized. Expired Token."
    user_not_found = "User not found."
    invalid_user_id = "Invalid user id."
    media_deleted_successfully = "Media deleted successfully."
    account_deleted_successfully = "Account deleted successfully."
    invalid_token = "Invalid token."
    possible_duplicate_error = "Possible duplicate error."
    message_received_successfully = "Message received successfully."
    username_is_required = "Username is required."
    phone_number_has_been_used = "Phone number has been used by another user"
    user_with_phone_number_not_found = "User with phone number not found."
    invalid_user_type = "Invalid user type."

    # account types descriptions
    account_type_buyer_description = "Account type for buyers of art works"
    account_type_artist_description = "Account type for artists/creators of art"
    account_type_validator_description = "Account type for validators of art works"


    # category
    category_created_successfully = "Category created successfully."
    category_updated_successfully = "Category updated successfully."
    category_deleted_successfully = "Category deleted successfully."

    # menu item
    menu_item_created_successfully = "Menu item created successfully."
    menu_item_updated_successfully = "Menu item updated successfully."
    menu_item_deleted_successfully = "Menu item deleted successfully."

    #cart
    item_added_to_cart = "Item added successfully."
    item_updated_cart = "Item updated successfully."
    item_deleted_from_cart = "Item deleted successfully."

    # orders
    order_placed_successfully = "Your Order has been submitted."


class ErrorMessages(TextChoices):
    internal_server_error = "Internal Server Error"
    something_went_wrong = "Something went wrong. Please try again."
    bad_request = "Bad Request"
    resource_not_found = "Resource Not Found"
    permission_denied = "You do not have the permission to perform this action."
    access_denied = "Access Denied."
    too_many_requests = "Permission denied. Too many requests."
    unprocessable_entity = "Unprocessable Entity"
    success = "Success"
    inactive_account = "Your account is inactive. Contact your administrator."
    session_expired = "Your session has expired. Please log in again."

    category_already_exists = "Category already exists."
    category_not_found = "Category not found."

    menu_item_already_exists = "Menu Item already exists."
    menu_item_not_found = "Menu Item not found."
    menu_item_with_that_name_already_exists = "Menu Item with that name already exists."

    no_items_in_cart = "No items in cart."
    invalid_qr_code = "Invalid QR Code"


