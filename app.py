import streamlit as st # type: ignore
import os
import utils as ut
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# common methods

# load data
data = ut.load_data()
df = ut.get_sent_analysis()
df = pd.DataFrame(df)
# create a directory if doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# save uploaded file to data directory
def save_uploaded_file(uploaded_file):
    with open(os.path.join("data", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return st.success(f"File '{uploaded_file.name}' uploaded successfully")


# display category list
def display_categories():
    categories = ut.category_reviews()
    boxes_html = ""
    for cat, count in categories.items():
        box_html = f"""
        <div style="border: 2px solid black; padding: 20px; border-radius: 5px; margin-right: 10px; display: inline-block;">
            <div style="font-size: 1.5em; font-weight: bold;">{cat}</div>
            <div style="font-size: 1.2em;">{count} Reviews</div>
        </div>
        """
        boxes_html += box_html
    st.markdown(boxes_html, unsafe_allow_html=True)

    

# display total reviews
def display_total():
    total_reviews = ut.get_total_reviews()
    total_reviews_box_html = f"""
    <div style="border: 2px solid black; padding: 20px; border-radius: 5px; margin-right: 10px; display: inline-block;">
        <div style="font-size: 1.5em; font-weight: bold;">Total Reviews</div>
        <div style="font-size: 1.2em;">{total_reviews} Reviews</div>
    </div>
    """
    st.markdown(total_reviews_box_html, unsafe_allow_html=True)


# Streamlit app
def main():

    st.set_page_config(layout="wide")

    # Sidebar
    st.sidebar.title("File Uploader")

    # file uploader widget
    uploaded_file = st.sidebar.file_uploader("Upload a file", type=["csv", "txt"])

    if uploaded_file is not None:
        save_uploaded_file(uploaded_file)

    st.title("Customer Satisfaction Analysis")

    #---------------------------SECTION 1-----------------
    # Create two columns with widths of 80% and 20%
    col1, col2 = st.columns([1, 4])

    # Output in the first column (80% width)
    with col1:
        st.subheader('Reviews Outlook')
        display_total()
        
    # Output in the second column (20% width)
    with col2:
        # display product category details
        st.subheader('Product Categories')
        display_categories()

    st.write("")
    #---------------SECTION 2 -------------------------
    # Create three columns with ratios of 40%, 30%, and 30%
    col1, col2, col3 = st.columns([3, 3, 4])

    # Add content to each column
    with col1:
        st.subheader('Satisfaction (%)')
        colors = {'neutral': 'lightblue', 'positive': 'lightgreen', 'negative': 'lightcoral'}
        df['color'] = df['sentiment'].map(colors)
        
        sentiment_counts = df.groupby('sentiment')['counts'].sum()

        # Plot pie chart using Matplotlib
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=sentiment_counts.index.map(colors))

        # Display pie chart using Streamlit's st.pyplot()
        st.pyplot(fig)

    with col2:
        st.subheader('Priority Level')

        negative_df = df[df['sentiment'] == 'negative']

        # Group DataFrame by product category and calculate total counts for each category
        category_counts = negative_df.groupby('product_category')['counts'].sum()

        # Plot bar chart using Matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))
        category_counts.plot(kind='bar', color='lightcoral', ax=ax)
        ax.set_xlabel('Product Category')
        ax.set_ylabel('Counts')
        ax.tick_params(axis='x', rotation=45, labelrotation=45)  # Use labelrotation instead of rotation
        ax.tick_params(axis='x', which='major', pad=15)  # Add padding between tick labels and axis

        # Display bar chart using Streamlit's st.pyplot()
        st.pyplot(fig)

    with col3:
        st.subheader('All Reviews')
        # Set Seaborn style
        sns.set_style("whitegrid")

        # Plot using Seaborn
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x="product_category", y="counts", hue="sentiment", palette="Set2")

        # Add title and labels
        plt.xlabel('Product Category')
        plt.ylabel('Counts')

        # Rotate x-axis labels
        plt.xticks(rotation=45)

        # Show plot
        st.pyplot(plt)


    #------------------SECTION 3------------------
    # Create five columns with equal size
    col1, col2, col3, col4, col5 = st.columns(5)

    # Add content to each column
    with col1:
        st.subheader('Bottoms')
        # Filter DataFrame for the "" category
        dresses_df = df[df['product_category'] == 'Bottoms']

        # Get counts for each sentiment
        sentiments = ['negative', 'positive', 'neutral']
        counts = dresses_df.groupby('sentiment')['counts'].sum()

        # Define colors for each sentiment
        color_map = {
            'negative': 'lightcoral',
            'positive': 'lightgreen',
            'neutral': 'lightblue'
        }

        # Plot grouped bar graph
        fig, ax = plt.subplots(figsize=(8, 6))
        for sentiment in sentiments:
            ax.bar(sentiment, counts.get(sentiment, 0), color=color_map.get(sentiment, 'gray'))
        ax.set_xlabel('Sentiment')
        ax.set_ylabel('Counts')
        ax.set_xticklabels(sentiments, rotation=45)
        st.pyplot(fig)

    with col2:
        st.subheader('Dresses')
                # Filter DataFrame for the "Dresses" category
        dresses_df = df[df['product_category'] == 'Dresses']

                        # Get counts for each sentiment
        sentiments = ['negative', 'positive', 'neutral']
        counts = dresses_df.groupby('sentiment')['counts'].sum()

        # Define colors for each sentiment
        color_map = {
            'negative': 'lightcoral',
            'positive': 'lightgreen',
            'neutral': 'lightblue'
        }

        # Plot grouped bar graph
        fig, ax = plt.subplots(figsize=(8, 6))
        for sentiment in sentiments:
            ax.bar(sentiment, counts.get(sentiment, 0), color=color_map.get(sentiment, 'gray'))
        ax.set_xlabel('Sentiment')
        ax.set_ylabel('Counts')
        ax.set_xticklabels(sentiments, rotation=45)
        st.pyplot(fig)

    with col3:
        st.subheader('Tops')
                # Filter DataFrame for the "Dresses" category
        dresses_df = df[df['product_category'] == 'Tops']

                        # Get counts for each sentiment
        sentiments = ['negative', 'positive', 'neutral']
        counts = dresses_df.groupby('sentiment')['counts'].sum()

        # Define colors for each sentiment
        color_map = {
            'negative': 'lightcoral',
            'positive': 'lightgreen',
            'neutral': 'lightblue'
        }

        # Plot grouped bar graph
        fig, ax = plt.subplots(figsize=(8, 6))
        for sentiment in sentiments:
            ax.bar(sentiment, counts.get(sentiment, 0), color=color_map.get(sentiment, 'gray'))
        ax.set_xlabel('Sentiment')
        ax.set_ylabel('Counts')
        ax.set_xticklabels(sentiments, rotation=45)
        st.pyplot(fig)

    with col4:
        st.subheader('Jackets')
                # Filter DataFrame for the "Dresses" category
        dresses_df = df[df['product_category'] == 'Jackets']

                        # Get counts for each sentiment
        sentiments = ['negative', 'positive', 'neutral']
        counts = dresses_df.groupby('sentiment')['counts'].sum()

        # Define colors for each sentiment
        color_map = {
            'negative': 'lightcoral',
            'positive': 'lightgreen',
            'neutral': 'lightblue'
        }

        # Plot grouped bar graph
        fig, ax = plt.subplots(figsize=(8, 6))
        for sentiment in sentiments:
            ax.bar(sentiment, counts.get(sentiment, 0), color=color_map.get(sentiment, 'gray'))
        ax.set_xlabel('Sentiment')
        ax.set_ylabel('Counts')
        ax.set_xticklabels(sentiments, rotation=45)
        st.pyplot(fig)

    with col5:
        st.subheader('Intimate')
        dresses_df = df[df['product_category'] == 'Intimate']

                        # Get counts for each sentiment
        sentiments = ['negative', 'positive', 'neutral']
        counts = dresses_df.groupby('sentiment')['counts'].sum()

        # Define colors for each sentiment
        color_map = {
            'negative': 'lightcoral',
            'positive': 'lightgreen',
            'neutral': 'lightblue'
        }

        # Plot grouped bar graph
        fig, ax = plt.subplots(figsize=(8, 6))
        for sentiment in sentiments:
            ax.bar(sentiment, counts.get(sentiment, 0), color=color_map.get(sentiment, 'gray'))
        ax.set_xlabel('Sentiment')
        ax.set_ylabel('Counts')
        ax.set_xticklabels(sentiments, rotation=45)
        st.pyplot(fig)

    st.write("")
    

if __name__ == "__main__":
    main()
