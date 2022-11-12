import requests
import json
import urllib
import pandas as pd

api_key = "b7dce8bf8dc00c64e0db222551017544"

def problematic(id):
    api_url = "https://api.themoviedb.org/3/movie/{}/credits?api_key={}&language=en-US".format(str(id), api_key)
    response = requests.get(api_url)
    array = response.json()
    sheet = pd.read_csv("prob.csv")
    flag = False
    prob_people = []
    for i in array['cast']:
        for j in range(len(sheet['ID'])):
            if (i['id'] == sheet['ID'][j]) and (i['id'] not in prob_people):
                if not flag:
                    flag = True
                    print("This movie is problematic.")
                prob_people.append(i['id'])
                print("{} has been accused of {}. Read more about it here: {}".format(sheet['Name'][j], sheet['Crime'][j], sheet['Link'][j]))
                break
        else:
            continue 
    for i in array['crew']:
        for j in range(len(sheet['ID'])):
            if i['id'] == sheet['ID'][j] and (i['id'] not in prob_people):
                if not flag:
                    flag = True
                    print("This movie is problematic.")
                prob_people.append(i['id'])
                print("{} has been accused of {}. Read more about it here: {}".format(sheet['Name'][j], sheet['Crime'][j], sheet['Link'][j]))
                break
        else:
            continue 
    if not flag:
        print("This movie is not problematic.")
    

while(True):
    text = input("Type in a movie title: ") # Get input 
    text = urllib.parse.quote(text) # Turn input into URL-friendly input
    api_url = "https://api.themoviedb.org/3/search/movie?api_key=b7dce8bf8dc00c64e0db222551017544&language=en-US&query=" + text + "&page=1&include_adult=false"
    response = requests.get(api_url)
    array = response.json()
    try:
        if len(array['results']) < 10: # If there are less than ten results, show all of them
            iter_results = len(array['results'])
        else: # Otherwise, just show ten
            iter_results = 10
        for i in range(iter_results): # Go through each entry, print title, year, synopsis
            print("{}: {} ({})".format(i + 1, array['results'][i]['original_title'], array['results'][i]['release_date'].split("-")[0]))
            print("Synopsis:", array['results'][i]['overview'])
            print("")
        movie_number = int(input("Which movie were you looking for? "))
        problematic(array['results'][movie_number - 1]['id']) # Send selected movie to problematic()
    except IndexError: # If results page has zero entries (name couldn't be found)
        print("Sorry, but we couldn't find the film you were looking for.")

