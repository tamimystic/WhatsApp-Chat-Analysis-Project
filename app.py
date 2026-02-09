import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor, helper

# PAGE CONFIG
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    layout="wide"
)

# SIDEBAR
st.sidebar.title("📊 WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("📂 Upload WhatsApp Chat (.txt)")

# MAIN TITLE
st.markdown(
    "<h1 style='text-align: center;'>📊 WhatsApp Chat Analyzer</h1>",
    unsafe_allow_html=True
)
st.markdown("---")

# DATA LOAD
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')

    df = preprocessor.preprocess(data)

    # User list
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox(
        "Show analysis with respect to",
        user_list
    )

    if st.sidebar.button("🚀 Show Analysis"):

        # TOP STATS
        num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)

        st.subheader("📌 Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Messages", num_messages)
        col2.metric("Total Words", words)
        col3.metric("Media Shared", num_media)
        col4.metric("Links Shared", num_links)

        st.markdown("---")

        # MONTHLY TIMELINE
        st.subheader("📅 Messages by Month & Year")
        monthly_timeline = helper.monthly_timeline(selected_user, df)

        fig, ax = plt.subplots(figsize=(14,5))
        ax.bar(monthly_timeline['time'], monthly_timeline['message'], color="#4C72B0")

        for i, v in enumerate(monthly_timeline['message']):
            ax.text(i, v, str(v), ha='center', va='bottom', fontsize=8)

        ax.set_xlabel("Month-Year")
        ax.set_ylabel("Messages")
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # DAILY TIMELINE
        st.subheader("📆 Daily Message Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)

        fig, ax = plt.subplots(figsize=(14,5))
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color="green")

        ax.set_xlabel("Date")
        ax.set_ylabel("Messages")
        plt.xticks(rotation=90)
        st.pyplot(fig)

        st.markdown("---")

        # ACTIVITY MAP
        st.subheader("🔥 Activity Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)

            fig, ax = plt.subplots(figsize=(6,4))
            ax.bar(busy_day.index, busy_day.values, color="#55A868")

            for i, v in enumerate(busy_day.values):
                ax.text(i, v, str(v), ha='center', va='bottom')

            plt.xticks(rotation=45)
            st.pyplot(fig)

        with col2:
            st.markdown("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)

            fig, ax = plt.subplots(figsize=(6,4))
            ax.bar(busy_month.index, busy_month.values, color="#DD8452")

            for i, v in enumerate(busy_month.values):
                ax.text(i, v, str(v), ha='center', va='bottom')

            plt.xticks(rotation=45)
            st.pyplot(fig)

        # HEATMAP
        st.subheader("🗓 Weekly Activity Heatmap")
        heatmap_data = helper.activity_heatmap(selected_user, df)

        if heatmap_data.empty:
            st.info("Not enough activity data to show heatmap.")
        else:
            fig, ax = plt.subplots(figsize=(10,4))
            sns.heatmap(
                heatmap_data,
                cmap="rocket",
                annot=False,
                linewidths=0.2,
                linecolor="#222",
                cbar_kws={"label": "Message Intensity"},
                ax=ax
            )
            st.pyplot(fig)

        st.markdown("---")

        # BUSY USERS
        if selected_user == "Overall":
            st.subheader("👥 Most Busy Users")
            top_users, percent_df = helper.fetch_busy_users(df)

            col1, col2 = st.columns([2,1])

            with col1:
                fig, ax = plt.subplots(figsize=(6,4))
                ax.bar(top_users.index, top_users.values, color="purple")

                for i, v in enumerate(top_users.values):
                    ax.text(i, v, str(v), ha='center', va='bottom')

                plt.xticks(rotation=45)
                st.pyplot(fig)

            with col2:
                st.dataframe(percent_df, use_container_width=True)

        st.markdown("---")

        # WORD CLOUD
        st.subheader("☁ Word Cloud")
        try:
            wc = helper.create_wordCloud(selected_user, df)

            if wc.words_:
                fig, ax = plt.subplots(figsize=(6,6))
                ax.imshow(wc)
                ax.axis("off")
                st.pyplot(fig)
            else:
                st.info("No words available to generate Word Cloud.")

        except:
            st.warning("Word Cloud could not be generated for this user.")


        # MOST COMMON WORDS
        st.subheader("📝 Most Used Words")
        common_words = helper.most_commonWords(selected_user, df)

        if common_words.empty:
            st.info("No significant words found.")
        else:
            fig, ax = plt.subplots(figsize=(10,4))
            ax.bar(common_words[0], common_words[1])

            for i, v in enumerate(common_words[1]):
                ax.text(i, v, str(v), ha='center', va='bottom')

            plt.xticks(rotation=45)
            st.pyplot(fig)

        st.markdown("---")

        # EMOJI ANALYSIS
        st.subheader("😄 Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)

        if emoji_df.empty:
                st.info("No emojis found for this user.")
        else:
            col1, col2 = st.columns([2,3])

            with col1:
                st.dataframe(emoji_df, use_container_width=True)

            with col2:
                    fig, ax = plt.subplots(figsize=(5,5))
                    ax.pie( emoji_df[1], labels=emoji_df[0], autopct="%0.1f%%", startangle=90 )
                    ax.axis("equal")
                    st.pyplot(fig)
