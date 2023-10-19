#!/usr/bin/env python3
#spotify connection
import requests
from dotenv import load_dotenv
import os
import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
import time
import random
from flask import Flask, jsonify

load_dotenv()

class spotify:
    def __init__(self):
        #.ENV varirables
        self.__clientID     = os.getenv("SPOTIPY_CLIENT_ID")
        self.__clientSecret = os.getenv("SPOTIPY_CLIENT_SECRET")
        self.__redirect     = os.getenv("SPOTIPY_REDIRECT_URL")
       
        self.__deviceID     = os.getenv("DESKTOP_ID")
        
        #spotify variables
        self.__access_token = self.__getAccessToken()
        self.__scope = "user-read-playback-state user-modify-playback-state playlist-modify-private playlist-modify-public"
        # self.__sp = spotipy.Spotify(auth=self.__access_token)

        self.__sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            scope=self.__scope,
            client_id=self.__clientID,
            client_secret=self.__clientSecret,
            redirect_uri=self.__redirect,
            open_browser=False
        ))

        self.__devices = self.__sp.devices()
        self.__loadDevice()

        #user variables
        self.liked_songs = []
        self.disliked_songs = []
        self.current_song = []


    def __loadDevice(self):
        for device in self.__sp.devices()['devices']:
            self.__deviceID = device['id']

    def __getAccessToken(self):
        sp_oauth = SpotifyOAuth(
            client_id=self.__clientID,
            client_secret=self.__clientSecret,
        )
        token_info = sp_oauth.get_access_token(as_dict=True)
        return token_info.get('access_token', '')
    
        
    #*--------------------SINGLE SONG METHODS--------------------
    #adding a song to the queue on device by name
    def queue_song(self, name):
        self.__sp.add_to_queue(device_id=self.__deviceID, uri=self.getSongs(name))

    #playing a song on device by name
    def play_song(self, name):
        self.__sp.start_playback(device_id=self.__deviceID, uris=[self.getSongs(name)])

    #pausing the song on the device
    def pause_song(self):
        self.__sp.pause_playback(device_id=self.__deviceID)

    #resuming the song on device
    def resume_song(self):
        self.__sp.start_playback(device_id=self.__deviceID)
    
    #going to the next song on device
    def skip_song(self):
        self.__sp.next_track(device_id=self.__deviceID)

    #raising or lowering the volume on device
    def adjust_volume(self, volume):
        self.__sp.volume(device_id=self.__deviceID, volume_percent=volume)

    def get_cover(self):
        if self.get_current_song():
            return {"cover_image_url":self.current_song["cover_image_url"]}
        else:
            return None


    #*----------PLAYLIST METHODS------------
    #!WORKING HERE
    #adding to a playlist
    def add_playlist(self, playlist_id, track_uris):
        self.__sp.playlist_add_items(playlist_id, [track_uris])
    
    #creating a new playlist if iis not made already
    def create_playlist(self, name="created by a bot"):
        #!SEE IF PLAYLIST EXITS ALREADY NEW PLAYLIST FOR EACH SESSION
        playlist_name = "created by a bot"

        self.__sp.user_playlist_create(self.__sp.me()["id"], playlist_name)
        results = self.__sp.search(q=playlist_name, type="playlist")

        # Extract the playlist ID from the search results
        if results and results["playlists"]["items"]:
            playlist_id = results["playlists"]["items"][0]["id"]
        
        return playlist_id

    #shuffling the playlist
    def shuffle_playlist(self, playlist_id):
        playlist_tracks = self.__sp.playlist_tracks(playlist_id)
        track_uris = [track['track']['uri'] for track in playlist_tracks['items']]
        random.shuffle(track_uris)
        self.__sp.playlist_replace_items(playlist_id, track_uris)

    #playing a playlist on the device by name
    def play_playlist(self, name):
        # print(self.__getPlaylist(name))
        self.__sp.start_playback(device_id=self.__deviceID, context_uri=self.__getPlaylist(name))
    
    def get_playlist(self, name):
        pass

    
    #*------------------helper methods------------------
    def get_current_song(self):
        current_playback = self.__sp.current_playback()

        if current_playback is None:
            return None

        track_name = current_playback['item']['name']
        artist_name = ", ".join([artist['name'] for artist in current_playback['item']['artists']])
        album_name = current_playback['item']['album']['name']
        cover_image_url = current_playback['item']['album']['images'][0]['url']  # Assuming you want the first image

        self.current_song =  {
            'track_name': track_name,
            'artist_name': artist_name,
            'cover_image_url': cover_image_url
        }

        return self.current_song


    def add_to_liked(self):
        self.get_current_song()
        self.liked_songs.append(self.current_song)
        
        #DEBUGGING
        # print("added to liked songs")
        # print(self.liked_songs)

    def add_to_disliked(self):
        self.get_current_song()
        self.disliked_songs.append(self.current_song)
        
        #DEBUGGING
        #print("added to disliked songs")
        #print(self.disliked_songs)

    def getSongs(self, name):
        results = self.__sp.search(name, 1, 0, "track")
        song_dict = results['tracks']
        song_items = song_dict['items']
        
        if not song_items:
            print(f"Track '{name}' not found.")
            return
        
        return song_items[0]['uri']

    def __getPlaylist(self, name):
        offset = 0
        limit = 50
        playlists = self.__sp.current_user_playlists(offset=offset, limit=limit)
        if playlists:
            print("Your playlists:")
            for playlist in playlists['items']:
                print(f"Playlist Name: {playlist['name']}")
                print(f"Playlist URI: {playlist['uri']}")
                print("---")
                if playlist['name'] == name:
                    uri = playlist['uri']
        
        else:
            print(f"Playlist '{name}' not found.")
            return None
        
        return uri