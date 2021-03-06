# ----------------------------------- OVERVIEW -----------------------------------

#           Goal: Create a program to download a YouTube videos
#           Objective: Create a progra that downloads a YouTube video from a URL as mp3/mp4 format

# ----------------------------------- TO DO -----------------------------------

# Add option to log into yt so you can download private playlists
# Add functionality to switch between Windows & Mac OS

#bin adnan$ -----> sudo pip3 install pytube3

# I have fixed this issue by changing a few lines in extract.py

# cipher_url = [
#                 parse_qs(formats[i]["cipher"]) for i, data in enumerate(formats)
#             ]
# cipher_url = [
#                 parse_qs(formats[i]["signatureCipher"]) for i, data in enumerate(formats)
#             ]

# https://webkit.org/blog/6900/webdriver-support-in-safari-10/

# ----------------------------------- SOURCE CODE -----------------------------------
from datetime import datetime
from pytube import YouTube
from pytube import Playlist
import re
import os
import getpass
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def menu():

    username = getpass.getuser()
    global directory_path
    # Default dir is the folder
    directory_path = 'downloads'

    print("\n------------------------------------------------------------------------------------------ ")
    print("----------------------------------    Hello, " + username + "     ----------------------------------- ")
    print("------------------------------------------------------------------------------------------\n")


    while True:
        userInput = input("Do you want to (c)lear existing files, download a (p)laylist, (m)usic or (e)xit: ").lower()
        if userInput == 'p':
            playlist()
        elif userInput == 'm':
            music()
        elif userInput == "c":
            clear()
        elif userInput == 'e':
            os._exit(0)

def playlist():
    playlist=[]
    url = input("Enter URL of the PLAYLIST: ")

    driver = webdriver.Safari()
    driver.get(url)
    links = driver.find_elements_by_xpath("//a[@href]")
    for link in links:
        href = link.get_attribute("href")
        if href.startswith('https://www.youtube.com/watch?v='):
            playlist.append(href)
    driver.close()

    #Gets rid of duplicate links
    playlist = list(dict.fromkeys(playlist))
    print("Length of playlist: " + str((len(playlist) - 2)))

    # First link will be a duplicate with a different URL, because thats how YouTube playlists work
    # The algorithm of collecting a playlist is abstract, the beginning of every scrape there are 2 links that are songs,
    # but not actually indexed to the playlist, so we start from the third link, which is the beginning of the playlist

    name_pref = input("Do you want to rename these files? (y/n): ")
    if name_pref == 'y':
        for l in range(2, len(playlist)):
                youtube = YouTube(playlist[l])
                print(youtube.title)
                video = youtube.streams.filter(only_audio=True).first()
                file_download = video.download(directory_path)
                new_file_name = input("New file name: ")
                print((new_file_name  + '.mp3'))
                # changes file to mp3
                os.rename(file_download, ('downloads' + '/' + new_file_name  + '.mp3'))
                try:
                    os.remove(file_download)
                except:
                    pass
    elif name_pref == 'n':
        for l in range(2, len(playlist)):
                youtube = YouTube(playlist[l])
                # print(youtube.title + ' - ' + playlist[l])
                print(youtube.title)
                video = youtube.streams.filter(only_audio=True).first()
                file_download = video.download(directory_path)
                # changes file to mp3
                os.rename(file_download, file_download[0:-4]  + '.mp3')
    print("Playlist downloaded successfully")

def clear():
    dirpath = directory_path
    try:
        for filename in os.listdir(dirpath):
            filepath = os.path.join(dirpath, filename)
            try:
                shutil.rmtree(filepath)
            except OSError:
                os.remove(filepath)
    except:
        print("No files are in the folder.")

def music():
    while True:
        try:
            url = input("Enter the URL or (e)xit: ")
            if url == 'e':
                break
            else:
                youtube = YouTube(url)
                print(youtube.title)

                video = youtube.streams.filter(only_audio=True).first()
                file_download = video.download(directory_path)

                name_pref = input("Do you want to rename this files (y/n): ")
                if name_pref == 'y':
                    new_file_name = input("New file name: ")
                    print((new_file_name  + '.mp3'))
                    os.rename(file_download, ('downloads' + '/' + new_file_name  + '.mp3'))
                elif name_pref == 'n':
                    os.rename(file_download, file_download[0:-4]  + '.mp3')
        except:
            print("An error has occurred.")
            break


if __name__ == '__main__':
    menu()