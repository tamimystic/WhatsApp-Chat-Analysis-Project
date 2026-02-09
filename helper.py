import pandas as pd
from wordcloud import WordCloud
from collections import Counter
from urlextract import URLExtract
import matplotlib.pyplot as plt
import emoji

extractor = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch number of messages
    numOf_messages = df.shape[0]

    # fetch number of words
    words = []
    for message in df['message']:
        #print(message.split())
        words.extend(message.split())

    # fetch number of media messages
    numOf_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of link shared
    links = []
    for message in df.message:
        links.extend(extractor.find_urls(message))

    return numOf_messages, len(words), numOf_media_messages, len(links)

def fetch_busy_users(df):
    x = df['user'].value_counts().head()
    y = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'user': 'name', 'count': 'percent'})
    return x,y

def create_wordCloud(selected_user,df):

    f = open('stopwords.txt','r')
    banglish_stopwords = set(f.read().split())

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    if temp.empty:
        return WordCloud(background_color='white',width=500,height=500).generate("")

    def remove_stopWords(message):
        y = []
        for word in message.lower().split():
            if word not in banglish_stopwords:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')

    temp['message'] = temp['message'].apply(remove_stopWords)

    if temp['message'].str.strip().eq("").all():
        return WordCloud(background_color='white', width=500, height=500).generate("")

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc

def most_commonWords(selected_user, df):

    f = open('stopwords.txt','r')
    banglish_stopwords = set(f.read().split())

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in banglish_stopwords:
                words.append(word)

    if len(words) == 0:
        return pd.DataFrame()

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []

    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    
    if len(emojis) == 0:
        return pd.DataFrame()
    
    most_common_emoji = pd.DataFrame(Counter(emojis).most_common(10))

    return most_common_emoji

def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    
    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    user_heatmap = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)

    return user_heatmap
    