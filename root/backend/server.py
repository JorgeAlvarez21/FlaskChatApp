from flask import Flask, request, jsonify
from sqlalchemy import text, or_
from root import settings
import sys
import path
import alerts

sys.path.append(path.Path(__file__).abspath().parent)
from database import session_local, engine
import models
import time

app = Flask(__name__)

db_session = session_local()

models.db_base.metadata.create_all(bind=engine)


# ***********************************        USER AUTH       ****************************************

@app.route('/user/register', methods=['POST'])
def user_register():
    user_data = request.get_json()
    fullname = user_data['fullname']
    username = user_data['username']
    email = user_data['email']
    password = user_data['password']
    try:
        user = models.User(fullname=fullname, email=email, username=username, password_hash=password)
        db_session.add(user)
        db_session.commit()
    except Exception as e:
        context = {'message': 'registration error', 'code': 400}

    loaded_user = db_session.query(models.User).filter_by(username=username).first()
    get_userID = loaded_user.userID
    # Create User Preferences Entry
    preferences_model = models.UserPreferences(userID=get_userID)
    db_session.add(preferences_model)
    db_session.commit()
    db_session.close()
    return 'User registered', 200

@app.route('/user/login', methods=['POST'])
def user_login():
    user_data = request.get_json()
    username = user_data['username']
    password = user_data['password']
    verify_user = db_session.query(models.User).filter_by(username=username, password_hash=password).first()
    if verify_user:
        return 'ok', 200
    else:
        'Credentials Do Not Match DB Records', 400

@app.route('/user/status', methods=['PUT', 'GET'])
def user_status_update():
    if request.method == 'PUT':
        userID = request.get_json()['userID']
        status = request.get_json()['status']
        query = db_session.query(models.User).filter_by(userID=userID).first()
        query.status = status
        db_session.merge(query)
        db_session.commit()
        db_session.close()
        return 'ok', 200

    elif request.method == 'GET':
        query = db_session.query(models.User).filter_by(userID=userID).first()
        get_status = query.status
        db_session.close()
        return {"status":get_status}, 201


# **********************************************FIND USER*****************************************************

@app.route('/data/find_user')
def find_user():
    if request.method == 'GET':
        search_pattern = request.get_json()['input']
        query = db_session.query(models.User).filter(
            or_(models.User.username == search_pattern, models.User.email == search_pattern,
                models.User.fullname == search_pattern))
        result = {}
        user_number = 0
        if len(query.all()) > 0:
            for user in query.all():
                user_number += 1
                result['fullname' + str(user_number)] = user.fullname
                result['username' + str(user_number)] = user.username
                result['userID' + str(user_number)] = user.userID

        return jsonify(result), 201


# ***************************************        GET USER DATA       ********************************************
@app.route('/data/user/get_data', methods=['GET'])
def get_user_data():
    if request.method == 'GET':
        context = {}
        data = request.get_json()
        try:
            try:
                get_username = data['username']
            except:
                get_username = None
            try:
                get_userID = data['userID']
            except:
                get_userID = None
        except Exception as e:
            raise ValueError('Invalid input: should be username or userID')

        if get_userID:
            user_query = db_session.query(models.User).filter_by(userID=get_userID).first()
            if user_query:
                context['userID'] = get_userID
                context['fullname'] = user_query.fullname
                context['username'] = user_query.username
                context['email'] = user_query.email

                return context, 201
            else:
                db_session.close()
                return 'User Does Not Exist', 400
                raise LookupError('User does not exist in DB')

        elif get_username:
            user_query = db_session.query(models.User).filter_by(username=get_username).first()
            if user_query:
                context['userID'] = user_query.userID
                context['fullname'] = user_query.fullname
                context['username'] = get_username
                context['email'] = user_query.email

                return context, 201
            else:
                db_session.close()
                return 'User Does Not Exist', 400
                raise LookupError('User does not exist in DB')


# ***************************************        ADD/REMOVE USER      **********************************************

@app.route('/requests/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        data = request.get_json()
        this_userID = data['this_userID']
        to_userID = data['other_userID']
        is_contact = db_session.query(models.Contacts).filter_by(userID=this_userID, contact_userID=to_userID).first()
        alert_exists = db_session.query(models.UserAlerts).filter_by(from_userID=this_userID,
                                                                     to_userID=to_userID).first()
        if alert_exists and alert_exists.status == 'open':
            return 'Request Already Sent', 400

        if not all([is_contact, alert_exists]):

            this_user_data = get_user_data_ss(this_userID)
            to_user_data = get_user_data_ss(to_userID)

            alert = alerts.AlertFromUser(from_userID=this_userID, to_userID=to_userID, alert_type='friendship_request',
                                         from_user_data=this_user_data, to_user_data=to_user_data)

            alert = alert.build()
            post_alert = write_user_alert(alert)

            if post_alert == 201:
                # Create contact
                write_new_contact(this_userID, to_userID)
            else:
                db_session.close()

            query = db_session.query(models.Contacts).filter_by(userID=this_userID, contact_userID=to_userID).first()
            status = query.friendship_status
            if status == 'pending':
                db_session.close()
                return 'Success', 201
            else:
                db_session.close()
                raise BufferError('Failed to Query Contact')
        else:
            query = db_session.query(models.Contacts).filter_by(userID=this_userID, contact_userID=to_userID).first()
            status = query.friendship_status
            if status == 'pending':
                db_session.close()
                return 'Request Already Sent', 400
            elif status == 'friends':
                raise ValueError('Users are already friends')


@app.route('/request/remove_user', methods=['DELETE'])
def remove_user():
    if request.method == 'DELETE':
        data = request.get_json()
        userID_one = data['userID']
        userID_two = data['contact_userID']

        user_one = db_session.query(models.Contacts).filter_by(userID=userID_one, contact_userID=userID_two).first()
        user_two = db_session.query(models.Contacts).filter_by(userID=userID_two, contact_userID=userID_one).first()

        if all([user_one, user_two]):
            db_session.delete(user_one)
            db_session.delete(user_two)
            db_session.commit()
            db_session.close()
            return 'OK', 200
        else:
            db_session.close()
            return 'Already Removed', 400


@app.route('/requests/undo_add_user', methods=['PUT'])
def undo_add_request():
    if request.method == 'PUT':
        data = request.get_json()
        from_userID = data['userID']
        to_userID = data['contact_userID']

        user_one = db_session.query(models.Contacts).filter_by(userID=from_userID, contact_userID=to_userID).first()
        user_two = db_session.query(models.Contacts).filter_by(userID=to_userID, contact_userID=from_userID).first()

        sent_alert = db_session.query(models.UserAlerts).filter_by(from_userID=from_userID, to_userID=to_userID,
                                                                   status='open').first()
        if sent_alert and all([user_one, user_two]):
            db_session.delete(sent_alert)
            db_session.delete(user_one)
            db_session.delete(user_two)
            db_session.commit()

            return 'ok', 200

        else:
            'Alert Not Deleted', 400


# ****************************************       Fetch Contacts       **********************************************

@app.route('/data/user/get_contacts', methods=['GET'])
def get_user_contacts():
    if request.method == 'GET':
        get_userID = request.get_json()['userID']
        query = db_session.query(models.Contacts).filter_by(userID=get_userID)
        contacts = query.all()
        context = {}

        if len(contacts) > 0:
            for i, contact in enumerate(contacts):
                contacts_dict = {}
                contacts_dict['contact_userID'] = contact.contact_userID
                contacts_dict['status'] = contact.friendship_status
                context["contact_" + str(i)] = contacts_dict
        else:
            db_session.close()
            return context, 400

        if len(context.keys()) < 1:
            return 'No contacts for this user', 400
        db_session.close()
        return context, 201


# ******************************************     Processing Alert Responses     **************************************

@app.route('/responses/friendship-status', methods=['PUT'])
def process_friend_status():
    if request.method == 'PUT':
        data = request.get_json()
        response = data['response']
        alertID = data['alertID']

    query_alert = db_session.query(models.UserAlerts).filter_by(alertID=alertID).first()
    if not query_alert:
        raise IndexError('Alert not found by alertID')
    else:
        if query_alert.status == 'open':
            userID_one = query_alert.from_userID
            userID_two = query_alert.to_userID

            user_one = db_session.query(models.Contacts).filter_by(userID=userID_one, contact_userID=userID_two).first()
            user_two = db_session.query(models.Contacts).filter_by(userID=userID_two, contact_userID=userID_one).first()

            if response == 'APPROVE':
                # Updating alert
                query_alert.response = 'approved'
                query_alert.notify_receiver = 'false'
                query_alert.status = 'closed'
                db_session.merge(query_alert)

                # Updating Contacts.users status
                user_one.friendship_status = 'friends'
                db_session.merge(user_one)
                user_two.friendship_status = 'friends'
                db_session.merge(user_two)

                # Create chat group here
                user_one_query = db_session.query(models.Contacts).filter_by(userID=userID_one,
                                                                             contact_userID=userID_two).first()
                groupID = user_one_query.groupID
                new_inbox = models.Inbox(groupID=groupID, userID_one=userID_one, userID_two=userID_two)
                db_session.add(new_inbox)

                db_session.commit()
                return 'Response Processed', 200


            elif response == 'DENY':
                # Updating alert
                query_alert.response = 'denied'
                query_alert.notify_receiver = 'false'
                query_alert.status = 'closed'
                db_session.merge(query_alert)

                # Removing temporary Contact entry on each user
                db_session.delete(user_one)
                db_session.delete(user_two)
                db_session.commit()
                return 'Response Processed', 200

    # Update on both ends if add user request is approved


# ***************************************      Fetch Alerts      *************************************************

@app.route('/alerts/fetch_by_user', methods=['GET'])
def fetch_user_alerts():
    if request.method == 'GET':
        data = request.get_json()
        userID = data['userID']
        user_alerts = db_session.query(models.UserAlerts).filter_by(to_userID=userID).all()

        if len(user_alerts) > 0:
            context = {}
            for i, alert in enumerate(user_alerts):
                if alert.status == 'closed':
                    continue
                else:
                    dict_alert = {}
                    dict_alert['alertID'] = alert.alertID
                    dict_alert['to_userID'] = alert.to_userID
                    dict_alert['from_userID'] = alert.from_userID
                    dict_alert['type'] = alert.type
                    dict_alert['name'] = alert.name
                    dict_alert['message'] = alert.message
                    dict_alert['sub_message'] = alert.sub_message
                    dict_alert['action_label'] = alert.action_label
                    dict_alert['status'] = alert.status
                    dict_alert['response'] = alert.response
                    dict_alert['notify_receiver'] = alert.notify_receiver
                    dict_alert['timestamp'] = alert.timestamp
                    context['alert_' + str(i)] = dict_alert
            db_session.close()
            return jsonify(context), 201
        else:
            db_session.close()
            return 'No new alerts', 400
        return 'No New Alerts Founds', 400


# ***************************************      Inbox      *************************************************



@app.route('/inbox/data/fetch_all', methods=['GET'])
def fetch_inbox_data():
    if request.method == 'GET':
        data = request.get_json()
        userID = data['userID']
        contact_userID = data['contact_userID']

        contact_query = db_session.query(models.Contacts).filter_by(userID=userID, contact_userID=contact_userID).first()
        if contact_query:
            if contact_query.friendship_status == 'friends':
                groupID = contact_query.groupID
                group_query = db_session.query(models.Inbox).filter_by(groupID=groupID).all()
                inbox = []
                for entry in group_query:
                    context = {}
                    context['groupID'] = entry.groupID
                    context['userID_one'] = entry.userID_one
                    context['userID_two'] = entry.userID_two
                    context['sent_by_one'] = entry.sent_by_one
                    context['msg_content'] = entry.msg_content
                    context['timestamp_sent'] = entry.timestamp_sent
                    inbox.append(context)
                return inbox, 201
                
            return [], 400
        else:
            return 'User Requested not in contacts', 400
        
        
@app.route('/inbox/messages/send', methods=['POST'])
def inbox_send_msg():
    if request.method == 'POST':
        data = request.get_json()
        groupID = data['groupID']
        sender_userID = data['this_userID']
        contact_userID = data['other_userID']
        message = data['message']
        group_query = db_session.query(models.Inbox).filter_by(groupID=groupID).first()

        if group_query.userID_one == sender_userID:
            sent_by_one = 'true'
            user_one = sender_userID
            user_two = contact_userID
            
        else:
            sent_by_one = 'false'
            user_one = contact_userID
            user_two = sender_userID

        instance = models.Inbox(groupID=groupID, userID_one=user_one, userID_two=user_two, sent_by_one=sent_by_one,
                               msg_content=message)
        
        db_session.add(instance)
        db_session.commit()
        db_session.close()
        
        return 'ok', 201


# *************************************       SERVER SIDE FUNCS         ********************************************


def get_user_data_ss(userID):
    user_query = db_session.query(models.User).filter_by(userID=userID).first()
    if user_query:
        context = {}
        context = {}
        context['userID'] = userID
        context['fullname'] = user_query.fullname
        context['username'] = user_query.username
        context['email'] = user_query.email
        return context
    else:
        raise LookupError('User does not exist in DB')


def write_user_alert(alert):
    new_alert = models.UserAlerts(to_userID=alert.get('to_userID'), from_userID=alert.get('from_user'),
                                  type=alert.get('alert_type'), name=alert.get('alert_name'),
                                  message=alert.get('alert_message'),
                                  sub_message=alert.get('alert_sub_message'), action_label=alert.get('button_action'),
                                  status=alert.get('status'), response=alert.get('response'),
                                  notify_receiver=alert.get('notify_receiver'), from_username=alert.get('from_username'))

    db_session.add(new_alert)
    db_session.commit()
    
    return 201


def write_new_contact(user_one, user_two, **kwargs):
    # Creating on first user, this defaults to a new groupID which is then used to auto-create a new inbox
    contact_one = models.Contacts(userID=user_one, contact_userID=user_two)
    db_session.add(contact_one)
    db_session.commit()

    contact_one_query = db_session.query(models.Contacts).filter_by(userID=user_one, contact_userID=user_two).first()
    groupID = contact_one_query.groupID

    contact_two = models.Contacts(userID=user_two, contact_userID=user_one, groupID=groupID)
    db_session.add(contact_two)
    db_session.commit()
    


if __name__ == '__main__':
    app.run(debug=settings.DEBUG)
