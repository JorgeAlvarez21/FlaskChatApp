
from database import session_local

db_session = session_local()


# ----------------------------- CREATING ALERTS------------------------------------

class AlertFromUser:
    def __init__(self, from_userID, to_userID, alert_type, from_user_data, to_user_data, **kwargs):
        self.from_userID = from_userID
        self.to_userID = to_userID
        self.alert_type = alert_type
        self.from_user_data = from_user_data
        self.to_user_data = to_user_data

    def build(self):
        if self.alert_type == 'friendship_request':
            alert_name = 'Friend request'
            message = f'{self.from_user_data.get("fullname")}  wants to be your friend.'
            action_label = 'Accept Request'
            alert_sub_message = 'false'

            context = dict(from_user=self.from_userID, to_userID=self.to_userID, alert_type=self.alert_type,
                           alert_name=alert_name, alert_message=message, alert_sub_message=alert_sub_message,
                           button_action=action_label,  status='open', response='awaiting',
                           notify_receiver='true', from_username=self.from_user_data.get('username'))

            return context
        else:
            raise IndexError('Alert Type Not Found')









# ------------------------------POSTING ALERTS-------------------------------------








# ------------------------------OPENING ALERTS-------------------------------------









# ------------------------------CLOSING ALERTS-------------------------------------
