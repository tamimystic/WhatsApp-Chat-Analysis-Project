from urlextract import URLExtract
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

        