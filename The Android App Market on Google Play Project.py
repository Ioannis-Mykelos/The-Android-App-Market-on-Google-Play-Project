#!/usr/bin/env python
# coding: utf-8

# In[109]:


import pandas as pd
import matplotlib.pyplot as plt
import plotly
plotly.offline.init_notebook_mode(connected=True)
import plotly.graph_objs as go
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
sns.set_style("darkgrid")
import warnings
warnings.filterwarnings("ignore")


# In[110]:


# 1. Import the data, drop duplicate rows, and inspect the data.

# Read in dataset
apps_with_duplicates = pd.read_csv("googleplaystore.csv")

# Drop duplicates from apps_with_duplicates
apps = apps_with_duplicates.drop_duplicates()

# Print the total number of apps
print('Total number of apps in the dataset = ', len(apps))

# Print a summary of apps dataframe
print(apps.info())

# Have a look at a random sample of 5 rows
n = 5
print(apps.sample(n))


# In[111]:


# 2. Data cleaning
#    The four features that we will be working with most frequently henceforth are Installs, Size, Rating and Price. 
#    The info() function (from the previous task) tells us that Installs and Price columns are of type object 
#    and not int or float as we would expect. This is because the column contains some characters more than just [0,9] digits. 
#    Ideally, we would want these columns to be purely numeric as their name suggests.

# List of characters to remove
chars_to_remove = ['+', ',', '$']
# List of column names to clean
cols_to_clean = ['Installs', 'Price']

# Loop for each column in cols_to_clean
for col in cols_to_clean:
    # Loop for each char in chars_to_remove
    for char in chars_to_remove:
        # Replace the character with an empty string
        apps[col] = apps[col].apply(lambda x: str(x).replace(char, ''))
    apps[col]=pd.to_numeric(apps[col],errors='coerce')


# In[112]:


# 3. Exploring app categories
#    With more than 1 billion active users in 190 countries around the world, Google Play continues to be an important 
#    distribution platform to build a global audience. For businesses to get their apps in front of users, it's important 
#    to make them more quickly and easily discoverable on Google Play. To improve the overall search experience, Google 
#    has introduced the concept of grouping apps into categories.

#    This brings us to the following questions:

#   3.1 Which category has the highest share of (active) apps in the market?
#   3.2 Is any specific category dominating the market?
#   3.3 Which categories have the fewest number of apps?
#   3.4 We will see that there are 33 unique app categories present in our dataset. Family and Game apps have the 
#       highest market prevalence. Interestingly, Tools, Business and Medical apps are also at the top.

# Print the total number of unique categories
num_categories = len(apps['Category'].unique())
print('Number of categories = ', num_categories)

# Count the number of apps in each 'Category' and sort them in descending order
num_apps_in_category = apps['Category'].value_counts().sort_values(ascending = False)


plt.bar(apps['Category'].unique(), num_apps_in_category)
plt.xticks(rotation=90)
plt.title('Apps Category vs number of Apps')
plt.xlabel('Apps Category')
plt.ylabel('# of Apps')
plt.show()



# Print the total number of unique categories
num_categories = len(apps['Category'].unique())
print('Number of categories = ', num_categories)

# Count the number of apps in each 'Category' and sort them in descending order
num_apps_in_category = apps['Category'].value_counts().sort_values(ascending = False)

data = [go.Bar(
        x = num_apps_in_category.index, # index = category name
        y = num_apps_in_category.values, # value = count
)]

plotly.offline.iplot(data)


# In[113]:


# 4. Distribution of app ratings
#    After having witnessed the market share for each category of apps, let's see how all these apps perform on an average. 
#    App ratings (on a scale of 1 to 5) impact the discoverability, conversion of apps as well as the company's overall 
#    brand image. Ratings are a key performance indicator of an app.

#    From our research, we found that the average volume of ratings across all app categories is 4.17. 
#    The histogram plot is skewed to the left indicating that the majority of the apps are highly rated with only a 
#    few exceptions in the low-rated apps.

# Average rating of apps
avg_app_rating = apps['Rating'].mean()
print('Average app rating = ', avg_app_rating)


plt.hist(x = apps['Rating'],bins=100)
plt.xlim(0, 6)
plt.xlabel("Rating")
plt.ylabel('# of Apps')
plt.title('Distribution of rating among the Apps')
plt.show()


# Average rating of apps
avg_app_rating = apps['Rating'].mean()
print('Average app rating = ', avg_app_rating)

# Distribution of apps according to their ratings
data = [go.Histogram(x = apps['Rating'])]

# Vertical dashed line to indicate the average app rating
layout = {'shapes': [{'type' :'line', 'x0': avg_app_rating, 'y0': 0, 'x1': avg_app_rating, 'y1': 1000, 
                      'line': { 'dash': 'dashdot'} }]}

plotly.offline.iplot({'data': data, 'layout': layout})


# In[114]:


# 5. Size and price of an app
#    Let's now examine app size and app price. For size, if the mobile app is too large, it may be difficult and/or 
#    expensive for users to download. Lengthy download times could turn users off before they even experience your mobile app. 
#    Plus, each user's device has a finite amount of disk space. For price, some users expect their apps to be free or 
#    inexpensive. These problems compound if the developing world is part of your target market; especially due to internet 
#    speeds, earning power and exchange rates.

#    How can we effectively come up with strategies to size and price our app?

#    Does the size of an app affect its rating?
#    Do users really care about system-heavy apps or do they prefer light-weighted apps?
#    Does the price of an app affect its rating?
#    Do users always prefer free apps over paid apps?
#    We find that the majority of top rated apps (rating over 4) range from 2 MB to 20 MB. 
#    We also find that the vast majority of apps price themselves under $10



# Select rows where both 'Rating' and 'Size' values are present (ie. the two values are not null)
apps_with_size_and_rating_present = apps[(~apps['Rating'].isnull()) & (~apps['Size'].isnull())]

# Subset for categories with at least 250 apps
large_categories = apps_with_size_and_rating_present.groupby(['Category']).filter(lambda x: len(x) >= 250)

# Plot size vs. rating
plt1 = sns.jointplot(x = large_categories['Size'], y = large_categories['Rating'])

# Select apps whose 'Type' is 'Paid'
paid_apps = apps_with_size_and_rating_present[apps_with_size_and_rating_present['Type'] == 'Paid']

# Plot price vs. rating
plt2 = sns.jointplot(x = paid_apps['Price'], y = paid_apps['Rating'])


# In[115]:


# 6. Relation between app category and app price
#    So now comes the hard part. How are companies and developers supposed to make ends meet? What monetization strategies 
#    can companies use to maximize profit? The costs of apps are largely based on features, complexity, and platform.

#    There are many factors to consider when selecting the right pricing strategy for your mobile app. It is important to 
#    consider the willingness of your customer to pay for your app. A wrong price could break the deal before the download 
#    even happens. Potential customers could be turned off by what they perceive to be a shocking cost, or they might delete 
#    an app they???ve downloaded after receiving too many ads or simply not getting their money's worth.

#    Different categories demand different price ranges. Some apps that are simple and used daily, like the calculator app, 
#    should probably be kept free. However, it would make sense to charge for a highly-specialized medical app that diagnoses 
#    diabetic patients. Below, we see that Medical and Family apps are the most expensive. Some medical apps extend even up 
#    to $80! All game apps are reasonably priced below $20.

fig, ax = plt.subplots()
fig.set_size_inches(15, 8)

# Select a few popular app categories
popular_app_cats = apps[apps.Category.isin(['GAME', 'FAMILY', 'PHOTOGRAPHY',
                                            'MEDICAL', 'TOOLS', 'FINANCE',
                                            'LIFESTYLE','BUSINESS'])]

# Examine the price trend by plotting Price vs Category
ax = sns.stripplot(x = popular_app_cats['Price'], y = popular_app_cats['Category'], jitter=True, linewidth=1)
ax.set_title('App pricing trend across categories')

# Apps whose Price is greater than 200
apps_above_200 = popular_app_cats[popular_app_cats['Price'] > 200]
apps_above_200[['Category', 'App', 'Price']]


# In[116]:


# 7. Filter out "junk" apps
#    It looks like a bunch of the really expensive apps are "junk" apps. That is, apps that don't really have a purpose. 
#    Some app developer may create an app called I Am Rich Premium or most expensive app (H) just for a joke or to test 
#    their app development skills. Some developers even do this with malicious intent and try to make money by hoping people 
#    accidentally click purchase on their app in the store.

#    Let's filter out these junk apps and re-do our visualization.

# Select apps priced below $100
apps_under_100 = popular_app_cats[popular_app_cats['Price'] < 100]

fig, ax = plt.subplots()
fig.set_size_inches(15, 8)

# Examine price vs category with the authentic apps (apps_under_100)
ax = sns.stripplot(x = 'Price', y = 'Category', data = apps_under_100, jitter = True, linewidth = 1)
ax.set_title('App pricing trend across categories after filtering for junk apps')


# In[117]:


# 8. Popularity of paid apps vs free apps
#    For apps in the Play Store today, there are five types of pricing strategies: free, freemium, paid, paymium, and 
#     subscription. Let's focus on free and paid apps only. Some characteristics of free apps are:

#    Free to download.
#    Main source of income often comes from advertisements.
#    Often created by companies that have other products and the app serves as an extension of those products.
#    Can serve as a tool for customer retention, communication, and customer service.
#    Some characteristics of paid apps are:

#    Users are asked to pay once for the app to download and use it.
#    The user can't really get a feel for the app before buying it.
#    Are paid apps installed as much as free apps? It turns out that paid apps have a relatively lower number of installs 
#    than free apps, though the difference is not as stark as I would have expected!


trace0 = go.Box(
    # Data for paid apps
    y = apps[apps['Type'] == 'Paid']['Installs'],
    name = 'Paid'
)

trace1 = go.Box(
    # Data for free apps
    y = apps[apps['Type'] == 'Free']['Installs'],
    name = 'Free'
)

layout = go.Layout(
    title = "Number of downloads of paid apps vs. free apps",
    yaxis = dict(title = "Log number of downloads",
                type = 'log',
                autorange = True)
)

# Add trace0 and trace1 to a list
data = [trace0, trace1]
plotly.offline.iplot({'data': data, 'layout': layout})


# In[118]:


#9. Sentiment analysis of user reviews
#   Mining user review data to determine how people feel about your product, brand, or service can be done using a technique 
#   called sentiment analysis. User reviews for apps can be analyzed to identify if the mood is positive, negative or neutral 
#   about that app. For example, positive words in an app review might include words such as 'amazing', 'friendly', 'good', 
#   'great', and 'love'. Negative words might be words like 'malware', 'hate', 'problem', 'refund', and 'incompetent'.

#   By plotting sentiment polarity scores of user reviews for paid and free apps, we observe that free apps receive a lot of 
#   harsh comments, as indicated by the outliers on the negative y-axis. Reviews for paid apps appear never to be extremely 1
#   negative. This may indicate something about app quality, i.e., paid apps being of higher quality than free apps on average. 
#   The median polarity score for paid apps is a little higher than free apps, thereby syncing with our previous observation.

#   In this notebook, we analyzed over ten thousand apps from the Google Play Store. We can use our findings to inform our 
#   decisions should we ever wish to create an app ourselves.

# Load user_reviews.csv
reviews_df = pd.read_csv('googleplaystore_user_reviews.csv')

# Join the two dataframes
merged_df = pd.merge(apps, reviews_df, on = "App")

# Drop NA values from Sentiment and Review columns
merged_df = merged_df.dropna(subset = ['Sentiment', 'Translated_Review'])

sns.set_style('ticks')
fig, ax = plt.subplots()
fig.set_size_inches(11, 8)

# User review sentiment polarity for paid vs. free apps
ax = sns.boxplot(x = 'Type', y = 'Sentiment_Polarity', data = merged_df)
ax.set_title('Sentiment Polarity Distribution')


# In[ ]:




