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
    invalid_option = "Invalid option."
    role_already_exists = "Role '{}' already exists."
    invalid_user_type = "Invalid user type."
    role_not_found = "Role not found."
    role_is_required = "Role is required."
    no_permission_to_assign_role = "You do not have the permission to act on the role '{}'."
    record_fetched_successfully = "Record(s) fetched successfully."
    profile_updated_successfully = "Profile updated successfully."
    user_acted_on_successfully = "User {} successfully."
    category_not_found = "Category not found."
    art_style_not_found = "Art Style not found."
    medium_not_found = "Art Medium not found."
    region_not_found = "Region not found."
    country_not_found = "Country not found."
    invalid_account_type = "Invalid account type."

    # account types descriptions
    account_type_buyer_description = "Account type for buyers of art works"
    account_type_artist_description = "Account type for artists/creators of art"
    account_type_validator_description = "Account type for validators of art works"

    # collection created
    collection_created = "Collection created successfully."
    collection_not_found = "Collection not found."
    collection_deleted = "Collection deleted successfully."

    # review created
    review_created = "Review created successfully."
    review_not_found = "Review not found."
    review_deleted = "Review deleted successfully."
    review_updated = "Review updated successfully."

    # fetch
    fetch_successful = "{} fetched successfully."

    # artwork
    artwork_added_successfully = "Art Work added successfully."
    artwork_added_to_collection = "Artwork was successfully added to collection."
    artwork_visibility_changed = "Artwork visibility changed successfully."

    # artist
    artist_profile_created = "Artist profile created successfully."
    artist_profile_not_found = "Artist profile not found."

    user_profile_not_found = "User profile not found."

    validation_center_not_found = "Validation center not found."

    # Curators
    curator_removed_successfully = "Curator removed successfully"
    curator_added_successfully = "Curator added successfully"

    successful_follow_unfollow = "You've successfully {}ed this artist."

    verification_request_created_successfully = "Verification request created successfully."
    failed_to_verify_nin = "Failed to verify NIN."
    verification_callback_success = "Verification callback response received successful"
    message_sent_successfully = "Message sent successfully."

    # orders
    order_created_success = "Order created successfully"
    order_not_found = "Order not found"
    order_item_added = "Order item added successfully"
    order_item_removed = "Order item removed successfully"
    order_item_not_found = "Order item not found"
    order_deleted = "Order deleted successfully"
    cannot_add_items_to_confirmed_order = "Cannot add items to a confirmed order"
    cannot_remove_items_from_confirmed_order = "Cannot remove items from a confirmed order"
    order_not_paid = "Order is not paid"
    cannot_update_pending_order_item = "Cannot update status of a pending order item"
    cannot_order_multiple_originals = "Cannot order multiple originals"
    cannot_delete_non_pending_order = "Cannot delete a non-pending order"

    # offers
    offer_created = "Offer created successfully"
    offer_updated = "Offer updated successfully"
    offer_cancelled = "Offer cancelled successfully"

    # category
    category_created_successfully = "Category created successfully."
    category_updated_successfully = "Category updated successfully."
    category_deleted_successfully = "Category deleted successfully."

    # transactions
    transaction_not_found = "Transaction not found"
    transaction_already_processed = "Transaction already processed"
    transaction_callback_successful = "Transaction callback successful"

    # newsletter
    newsletter_subscription_successful = "Newsletter subscription successful."
    newsletter_unsubscribe_successful = "Successfully unsubscribed from newsletter"
    newsletter_subscription_already_exists = "Newsletter subscription already exists."

    # shipping addresses
    shipping_address_created = "Shipping address created successfully."
    shipping_address_not_found = "Shipping address not found."
    shipping_address_deleted = "Shipping address deleted successfully."

    # shipping
    shipping_created = "Shipping created successfully."

    # verification
    id_verification_not_found = "ID verification not found."

    # bank accounts
    bank_account_deleted = "Bank account deleted successfully."


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

    user_must_be_an_artist = "Only artists can access this"
    user_must_be_an_buyer = "Only buyers can access this"
    field_required = "{} is required"
    selected_resource_not_found = "{} not found"
    unverified_email = "Please Verify your Email."
    template_not_provided = "Template not provided."

    # App Specific
    artwork_not_found = "Artwork not found"
    artwork_validation_not_found = "Artwork validation not found"
    print_option_not_found = "Print option not found"
    artwork_print_not_found = "Artwork print not found"
    offer_not_found = "Offer not found"
    invalid_object_type = "Invalid object type."
    invalid_object_id = "Invalid object id."
    message_not_found = "Message not found."
    collection_not_found = "Collection not found."

    app_notification_not_found = "App notification not found."
    subscriber_not_found = "Email not found in subscriber list"

    year_not_valid = "Year must be between 1900 and 2100"

    user_must_be_an_artist_or_buyer = "Only artists and buyers can access this"
    user_must_be_a_validator = "Only Validators can access this"
    city_id_state_id_not_provided = "City or state id not provided."
    center_not_found = "Validation Center not found."
