import re
import pandas as pd

def preprocess(data):
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?[ap]m)?)\s-\s'

    messages = re.split(pattern, data)[1:]

    dates = messages[0::2]
    texts = messages[1::2]

    df = pd.DataFrame({
    'message_date': dates,
    'user_message': texts
    })

    df['message_date'] = pd.to_datetime(
    df['message_date'],
    format='%d/%m/%y, %I:%M %p'
    )

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    msgs = []

    for msg in df['user_message']:
        entry = re.split(r':\s', msg, maxsplit=1)
        if len(entry) == 2:
            users.append(entry[0])
            msgs.append(entry[1])
        else:
            users.append('group_notification')
            msgs.append(entry[0])

    df['user'] = users
    df['message'] = msgs

    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
