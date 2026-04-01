import os


def app_settings(request):

    app_defaults = {
        'app_name' : os.getenv("APP_NAME"),
        'domain_name' : os.getenv("DOMAIN_NAME"),
        'instagram_url' : os.getenv("INSTAGRAM_URL"),
        'tiktok_url' : os.getenv("TIKTOK_URL"),
        'whatsapp_url' : os.getenv("WHATSAPP_URL"),
        'app_google_address_link' : os.getenv("APP_GOOGLE_ADDRESS_LINK"),
        'app_address' : os.getenv("APP_ADDRESS"),
        'app_email' : os.getenv("APP_EMAIL"),
        'app_phone_number' : os.getenv("APP_PHONE_NUMBER"),
    }

    return {'app_config': app_defaults}