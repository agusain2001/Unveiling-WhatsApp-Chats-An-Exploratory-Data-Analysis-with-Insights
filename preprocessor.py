import re
import pandas as pd
def preprocess(data): 
    messages = []
    dates =[]
        # print(data)
        # Iterate through each line in the file
    for line in data.split('\n'):
        # Split the line by '-'
        parts = re.split(r'\s-\s', line.strip(), maxsplit=1)
        
        # Check if the split resulted in two parts
        if len(parts) >= 2:
            # Extract the second part and append to the messages list
            messages.append(parts[1])
            dates.append(parts[0])
    # Display the messages
    new_date =[]
    for date in dates:
        d=date.replace("\u202fpm","")
        new_date.append(d)
    

    df = pd.DataFrame({'user_mesage': messages, 'message_date': new_date})


    possible_formats = ["%d/%m/%y, %H:%M -", "%d/%m/%y, %I:%M%p", "%d/%m/%y, %I:%M %p"]

    for fmt in possible_formats:
        try:
            df['message_date'] = pd.to_datetime(df['message_date'].str.replace(' -', ''), format=fmt)
            break  
        except ValueError:
            pass  

    df.rename(columns={'message_date': 'date'}, inplace=True)

    

    users = []
    messages = []
    for message in df['user_mesage']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_mesage'], inplace=True)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df

