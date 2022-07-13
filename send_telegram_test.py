import traceback
import imdb
import requests
import tweepy


# Function to send message
def send_message(user_id, text):
    # This comes from BotFather
    bf_token = '5449582238:AAHv4yiMigTYUSZ7fcJUaVRr2jFuTSQf3xA' 
    url = f"https://api.telegram.org/bot{bf_token}/sendMessage"
    
    params = {
      "chat_id": user_id,
      "text": text,
    }
    resp = requests.get(url, params=params)
    # Throw an exception if Telegram API fails
    resp.raise_for_status()
   
  
def get_twitter_authentication():
  consumer_key = "Y1tJOTDMwwTfikgeq3oCzm32S"
  consumer_secret = "Qwp8Vfxba8HqFVOPkXn5v6A2Aqsm9nnGKc3uNRp7YdgRfojvGD"
  access_token = "3009962708-BnPNM3OW0iAKIiThMhvaWA8wGSFNUl9Yfs7rifA"
  access_token_secret = "ZtOXKhQHHOqa2Sx8L9QaItF1XnGn5plJtXJVk6qEXhvLe"

  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  return auth

def call_twitter_api(auth):
  api = tweepy.API(auth)
  topic_to_search = "#SocialKondattam"
  search_tweets = api.search_tweets(q=topic_to_search, count=10)
  return search_tweets

if __name__ == '__main__':
  kiwin_user_id = 675500009   # My ID
  aaron_user_id = 890387539   # Aaron's ID
  #send_message(UserIDofPerson, 'GVM sucks !')
  
  auth = get_twitter_authentication()
  tweets = call_twitter_api(auth)

  text_list = []
  for tweet in tweets:
    #if (not tweet.retweeted):
    #acc_name = tweet._json['entities']['user_mentions'][0]['name']
    #if acc_name == "K TV":
    text_list.append((tweet.text, tweet._json['created_at']))
  
  #print(text_list)

  movie_list = []

  for text_time in text_list:
    text = text_time[0]
    word_list = text.split(" ")
    for ind, word in enumerate(word_list):
      if ind < len(word_list)-2:
        if word_list[ind+1] == 'today' or word_list[ind+1] == 'tonight':
          if word_list[ind+2] == 'at':
            if word_list[ind+3].isnumeric():
              if word_list[ind+4] == 'PM'or word_list[ind+4] == 'AM':
                movie_name = word.replace('#', '').split('\n')[-1]
                #created_time_str = 
                movie_date = " ".join(text_time[1].split(" ")[:3])
                movie_time = f"{word_list[ind+3]} {word_list[ind+4]}"
                movie_list.append((movie_name, movie_date, movie_time))

  unique_movies_list = set(movie_list)
  print(unique_movies_list)

  director_list = ['Mani Ratnam', 'Hari', 'Shankar']
  actor_list = ['Ajith Kumar', 'Rajinikanth', 'Vishal', 'Vijay']
  

  ia = imdb.Cinemagoer()
  for movie in unique_movies_list:

    try:
      db_movies = ia.search_movie(movie[0])
      if not db_movies:
        continue
      db_movie_id = db_movies[0].movieID
      db_real_movie = ia.get_movie(db_movie_id)
      db_actor_list = [actor['name'].replace('_', '') for actor in db_real_movie['actors']]
      db_director_list = [director['name'].replace('_', '') for director in db_real_movie['directors']]
      db_rating = db_real_movie['rating']

      sent_flag = 0

      if db_rating > 6:
        msg = f"Watch {movie[0]} on KTV at {movie[1]} {movie[2]}. IMDB Rating is {db_rating}"
        send_message(kiwin_user_id, msg)
        send_message(aaron_user_id, msg)
        print(f"MESSAGE SENT - {movie[0]}")
        sent_flag = 1

      actor_flag = 0
      main_actor = "No one"
      for actor in db_actor_list:
        if actor in actor_list:
          main_actor = actor
          actor_flag = 1
          break

      director_flag = 0
      main_director = "None"
      for director in db_director_list:
        if director in director_list:
          main_director = director
          director_flag = 1
          break
      
      if actor_flag and sent_flag == 0:
        msg = f"Watch {movie[0]} on KTV at {movie[1]} {movie[2]}. YOur favourite actor {main_actor} is starring"
        send_message(kiwin_user_id, msg)
        send_message(aaron_user_id, msg)
        print(f"MESSAGE SENT - {movie[0]}")
        sent_flag = 1
      
      if director_flag and sent_flag == 0:
        msg = f"Watch {movie[0]} on KTV at {movie[1]} {movie[2]}. YOur favourite director {main_actor}'s film"
        send_message(kiwin_user_id, msg)
        send_message(aaron_user_id, msg)
        print(f"MESSAGE SENT - {movie[0]}")
        sent_flag = 1
    except Exception as e:
      print(e)
      print(traceback.format_exc())
