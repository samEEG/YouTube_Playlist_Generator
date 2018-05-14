#!/usr/bin/python

import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets



CLIENT_SECRETS_FILE = "client_secrets.json"
# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the {{ Cloud Console }}
{{ https://cloud.google.com/console }}

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
  message=MISSING_CLIENT_SECRETS_MESSAGE,
  scope=YOUTUBE_READ_WRITE_SCOPE)

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
  flags = argparser.parse_args()
  credentials = run_flow(flow, storage, flags)
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
  http=credentials.authorize(httplib2.Http()))

'''
Method Name:create_playlists ---- is a method that creates a playlist to your youtube channel 
Input: None 
Output: Playlist object ---- Refer to YouTube API so see what information is within
        the returned object 
'''
def create_playlist(): 
      playlists_insert_response = youtube.playlists().insert(
      part="snippet,status",
      body=dict(
        snippet=dict(
          title="Test Playlist",
          description="A private playlist created with the YouTube API v3"
        ),
        status=dict(
          privacyStatus="private"
        )
      )
     ).execute()
      return playlists_insert_response
'''
Method Name: add_video_to_playlist ---- is a method that adds youtube videos to your playlist 
Input: youtube - clientID, videoID- unique video id of YouTube video, playlistID - unique playlist id for 
      video you want to add to.
Output:video object that was inserted into specifc playlist. Refer to YouTube API to know specific information 
      within object  
'''
def add_video_to_playlist(youtube,videoID,playlistID):
    add_video_request=youtube.playlistItems().insert(
      part="snippet",
      body=dict(
            snippet=dict( 
               playlistId= playlistID, 
               resourceId= dict(
                       kind="youtube#video",
                       videoId=videoID
                )
            )
    )
     ).execute()
    return add_video_request
 
'''
Method Name: playlist_delete ---- deletes a playlist from your youtube channel
Input: youtube -client id, playlistID - unique playlist id for video you want to add to.
Output: None 
'''

def playlists_delete(youtube, playlistID):
  youtube.playlists().delete(id=playlistID).execute()


# Sample python code for playlistItems.list

def playlist_items_list_by_playlist_id(youtube, part, maxResults, playlistID):
  # See full sample for function
  playlistitems_request = youtube.playlistItems().list(
    part= part,
    playlistId=playlistID,
    maxResults=maxResults
  ).execute()
  description_list = []
  title_list = []
  while playlistitems_request:
    playlistitems_list_response = playlistitems_request
    
    # Insert titles and descriptions into respected lists 
    for playlist_item in playlistitems_list_response['items']:
      title_list.append(playlist_item['snippet']['title'])
      description_list.append(playlist_item['snippet']['description'])

    playlistitems_request = youtube.playlistItems().list_next(
      playlistitems_request, playlistitems_list_response)
  for x in description_list: 
    print(x.encode("utf-8"))
    print("\n")


playlist_items_list_by_playlist_id(youtube, 'snippet,contentDetails', 25, 'PLak0R99wjd8qZcH2XD8-xr9Zx36sO9FBV')





#playlists_insert_response = create_playlist()
#add_video_request = add_video_to_playlist(youtube,"AaGK-fj-BAM", "PLak0R99wjd8qlFHgV_qX9flC1s_84DjQB")
#playlists_delete(youtube, 'PLak0R99wjd8pLSiUpW2OfUKf709NXz_OH')
#print("New playlist id: {}".format(playlists_insert_response["id"]))
#print("New video inserted {}".format(add_video_request["snippet"]["title"]))

#what inside snippet 
#publishedAt, channelTitle, resourceId, playlistId, playlistId, description, title, thumbnails



# Sample python code for search.list



