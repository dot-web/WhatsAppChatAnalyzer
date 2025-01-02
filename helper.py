from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter 
import emoji


extractor=URLExtract
def fetch_stats(selected_user,df):
    if selected_user!= 'Overall':
        df=df[df['user']==selected_user]
        #1 fetch numner of messages
    num_messages=df.shape[0]
        #2 Number of words
    words=[]
    for message in df['message']:
        words.extend(message.split())
        #3 Fetch number of media shared
        
    num_media_messages=df[df['message']=='<Media omitted>\n'].shape[0]

        #4 Fetch number of links shared
    extract=URLExtract()
    links=[]
    for message in df['message']:
         links.extend(extract.find_urls(message))

    return num_messages, len(words),num_media_messages,len(links)


def most_busy_users(df):

    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index':'name','user':'Percent'})
    return x,df

def create_wordcloud(selected_user,df):

    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    wc=WordCloud(width=500,height=500,min_font_size=10, background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=" "))

    return df_wc



def most_common_words(selected_user,df):
        if selected_user!='Overall':
             df=df[df['user']==selected_user]

        f=open('E:\CloudyML\Whatsappdataanalyser\Hinglish.txt')
        stop_words=f.read()

        temp=df[df['user']!='Group Notification']
        temp=temp[temp['message']!='<Media omitted>\n']

        words=[]

        for message in temp['message']:
            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)


                words.extend(message.split())


        most_common_df=pd.DataFrame(Counter(words).most_common(20))
        return most_common_df

def emoji_helper(selected_user,df):
    if selected_user!='Overall':
             df=df[df['user']==selected_user]

    emozis=[]

    for message in df['message']:
        emozis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    emoji_df=pd.DataFrame(Counter(emozis).most_common(len(Counter(emozis))))

    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
             df=df[df['user']==selected_user]


    timeline=df.groupby(['Year','month_num','Month']).count()['message'].reset_index()

    time=[]

    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i]+ "-" + str(timeline['Year'][i]))

    timeline['time']=time

    return timeline


def daily_timeline(selected_user,df):
     
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    daily_timeline=df.groupby('Only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
            
    return df['day_name'].value_counts()

def month_activity(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    return df['Month'].value_counts()    

def activity_heatmap(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    activity_heatmap=df.pivot_table(index='day_name',columns='Period',values='message',aggfunc='count').fillna(0)

    return activity_heatmap


    

     
     
     




             
     
     






