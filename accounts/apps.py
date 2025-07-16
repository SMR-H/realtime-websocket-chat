from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    # label = 'my_custom_account'  # this to a unique label
    # verbose_name = 'Account'