import re
import pandas as pd
def preprocess(data):
    pattern='\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s-\s'    
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)

    df=pd.DataFrame({'user_messages':messages,'message_dates':dates})

    df['message_dates']=pd.to_datetime(df['message_dates'],format='%m/%d/%y, %H:%M - ')

    df=df.rename(columns={'message_dates': 'Dates'})


    #seperate users and messages
    user=[]
    message=[]
    for messages in df['user_messages']:
        entry=re.split('([\w\W]+?):\s',messages)
        if entry[1:]:
            user.append(entry[1])
            message.append(entry[2])
        else:
            user.append('Group Notification')
            message.append(entry[0])
    df['user']=user
    df['message']=message

    df.drop(['user_messages'],axis=1,inplace=True)

    df['Year']=df['Dates'].dt.year

    df['Only_date']=df['Dates'].dt.date

    df['month_num']=df['Dates'].dt.month

    df['Month']=df['Dates'].dt.month_name()

    df['Day']=df['Dates'].dt.day

    df['day_name']=df['Dates'].dt.day_name()

    df['Hour']=df['Dates'].dt.hour

    df['Minutes']=df['Dates'].dt.minute


    period=[]
    for Hour in df[['day_name','Hour']]['Hour']:
        if Hour==23:
            period.append(str(Hour)+ "-" + str('00'))
        elif Hour==0:
            period.append(str('00')+ "-" + str(Hour+1))
        else:
            period.append(str(Hour)+ "-" +str(Hour+1))

    df['Period']=period
    
    




    return df

    

    

