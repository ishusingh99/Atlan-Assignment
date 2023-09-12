# plugins/interfaces.py

class PluginInterface:
    def push_to_google_sheets(self, form_id, response_data):
        pass

    def send_sms(self, phone_number, message):
        pass
