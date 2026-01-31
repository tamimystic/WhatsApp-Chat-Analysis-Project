import streamlit as st
import matplotlib.pyplot as plt
import preprocessor,helper


st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    data = bytes_data.decode('utf-8')
    #st.text(data)

    df = preprocessor.preprocess(data)

    st.dataframe(df)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)

    if st.sidebar.button("Show Analysis"):
        
        # Stats Area
        num_messages, words, numOf_media_messages, numOf_links= helper.fetch_stats(selected_user,df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Media Shared")
            st.title(numOf_media_messages)

        with col4:
            st.header("Total Link Shared")
            st.title(numOf_links)

        # Finding the busiest user in the grooup(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            top5, percent_df = helper.fetch_busy_users(df)
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns([2.5,1.5])

            with col1:
                ax.bar(top5.index, top5.values, color='green')
                for i, value in enumerate(top5.values):
                    ax.text(i, value, str(value), ha='center', va='bottom')

                plt.ylabel("Number of messages")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            
            with col2:
                st.dataframe(percent_df)
        
        #Word Cloud
        st.title("Word Cloud")
        df_wc = helper.create_wordCloud(selected_user=selected_user,df=df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title("Most Used words")

        most_common_df = helper.most_commonWords(selected_user,df)

        fig , ax = plt.subplots()

        ax.bar(most_common_df[0], most_common_df[1])

        for i, value in enumerate(most_common_df[1]):
            ax.text(i, value, str(value), ha='center', va='bottom')

        plt.ylabel("Number of Words")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        

            