import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import  seaborn as sns

st. set_page_config(layout="wide")
st.sidebar.title(":green[WhatsApp Chat Analyser]")


uploaded_file = st.sidebar.file_uploader("Choose a chat file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')  #Convert in a stream
    # st.text(data) #See the stream value
    df = preprocessor.preprocess(data)

    # st.dataframe(df) #show the dataframe

    #fetch unique user
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis with Respect To", user_list)

    if st.sidebar.button("Show Analysis"):

       num_messages, words, num_media_massages, num_links_shared = helper.fetch_stats(selected_user, df)
       st.title(":blue[Top Statistics]")
       st.text("")
       st.text("")
       st.text("")

       col1, col2, col3, col4 = st.columns(4)

       with col1:
           st.header("Total Messages")
           st.title(num_messages)
           st.text("")
           st.text("")
           st.text("")

       with col2:
           st.header("Total Words")
           st.title(words)
           st.text("")
           st.text("")
           st.text("")

       with col3:
           st.header("Total Media Shared")
           st.title(num_media_massages)
           st.write("")
           st.text("")

       with col4:
            st.header("Total Shared Links")
            st.title(num_links_shared)
            st.write("")
            st.text("")


       #Find the busiest users in the group(Group Level)
       if selected_user == 'Overall':

           x, new_df = helper.most_busy_users(df)
           st.title(":blue[Busy User]")

           col11, col22 = st.columns([1,1])

           with col11:
              st.subheader("Overall busier percentage")
              st.dataframe(new_df, width=700, height=500)
              st.text("")
              st.text("")
              st.text("")

           with col22:
               fig, ax = plt.subplots()

               st.subheader(':blue[Top] Most busy user  :sunglasses:')
               colors = sns.color_palette('Set2')
               ax.bar(x.index, x.values, color=colors)
               ax.set_xlabel('User')
               ax.set_ylabel('Message')
               plt.xticks(rotation='vertical')
               st.pyplot(fig)
               st.text("")
               st.text("")
               st.text("")

       #Word Cloud
       st.title(":blue[Word Cloud]")
       df_wc = helper.create_wordcloud(selected_user, df)
       fig, ax = plt.subplots()
       ax.imshow(df_wc)
       st.pyplot(fig)
       st.text("")
       st.text("")
       st.text("")

       #Most common words
       most_common_df = helper.most_common_words(selected_user, df)

       fig, ax = plt.subplots()

       colors = sns.color_palette('Set2')
       ax.bar(most_common_df[0], most_common_df[1], color=colors)

       plt.xticks(rotation = 'vertical')

       st.title(":blue[Most Common Words]")
       ax.set_xlabel('Common Word')
       ax.set_ylabel('Count')
       st.pyplot(fig)
       st.text("")
       st.text("")
       st.text("")


       # Emoji Analysis
       emoji_df = helper.emoji_helper(selected_user, df)
       st.title(":blue[Emoji Analysis]")

       col1, col2 = st.columns(2)

       with col1:
           st.subheader("All Emojis' Counting")
           st.dataframe(emoji_df,  width=700, height=400)

       with col2:
           fig, ax = plt.subplots()

           colors = sns.color_palette('Set2')
           explode = [0.05, 0.05, 0.05, 0.05, 0.05]

           # ax.pie(emoji_df['Count'].head(), labels=emoji_df['Emoji'].head(), colors=colors, autopct="%0.2f", explode= explode)
           ax.set_xlabel('Top - 5 Emoji')
           ax.set_ylabel('Total Count')
           ax.plot(emoji_df['Emoji'].head(), emoji_df['Count'].head(), marker='$\U0001F601$', ms=20, c='green')

           st.subheader("Top - 5 Emojis' Graphical Representation")
           st.pyplot(fig)
           st.text("")
           st.text("")
           st.text("")

       #Monthly Timeline
       timeline = helper.monthly_timeline(selected_user, df)

       st.title(":blue[Monthly Timeline]")

       fig, ax = plt.subplots()

       ax.set_xlabel('Month')
       ax.set_ylabel('Message Count')
       ax.plot(timeline['time'], timeline['message'], marker='$\U0001F601$', ms=1.5, c='green')
       plt.xticks(rotation=90)
       st.pyplot(fig)
       st.text("")
       st.text("")
       st.text("")

       #Daily Timeline
       daily_timeline = helper.daily_timeline(selected_user, df)

       st.title(":blue[Daily Timeline]")

       fig, ax = plt.subplots()

       ax.set_xlabel('Day')
       ax.set_ylabel('Message Count')
       ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
       plt.xticks(rotation=90)
       st.pyplot(fig)
       st.text("")
       st.text("")
       st.text("")

       #Weekly Activity Map
       weekly_activity_map = helper.weekly_activity_map(selected_user, df)

       monthly_activity_map = helper.monthly_activity_map(selected_user, df)

       st.title(":blue[Activity Map]")

       col111, col222 = st.columns(2)


       with col111:
           fig, ax = plt.subplots()

           colors = sns.color_palette('Set1')
           st.subheader("Most Busy Day")
           ax.set_xlabel('Week')
           ax.set_ylabel('Message Count')
           ax.bar(weekly_activity_map.index, weekly_activity_map.values, color = colors)
           plt.xticks(rotation=90)
           st.pyplot(fig)

           st.text("")
           st.text("")
           st.text("")

       with col222:
           fig, ax = plt.subplots()

           colors = sns.color_palette('Set2')

           st.subheader("Most Busy Month")
           ax.set_xlabel('Month')
           ax.set_ylabel('Message Count')
           ax.bar(monthly_activity_map.index, monthly_activity_map.values, color=colors)
           plt.xticks(rotation=90)
           st.pyplot(fig)

           st.text("")
           st.text("")
           st.text("")

        #Heatmap
       st.title("Most Talkative Time period in Week")
       user_heatmap = helper.activity_heatmap(selected_user, df)

       fig, ax = plt.subplots()
       ax = sns.heatmap(user_heatmap)
       ax.set_xlabel('Time Period')
       ax.set_ylabel('Day')
       st.pyplot(fig)




