# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import re, requests

class Sites(object):
    _instance = None
    first     = False

    sources = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Sites, cls).__new__(cls, *args, **kwargs)

        return cls._instance

    def add(self, identifier, oembed, icon='fa-star', name=''):
        if not self.first:
            self.first = True

        self.sources[identifier] = (oembed, icon, name)

    def get(self, url):
        for key in self.sources:
            if re.match(key, url):
                return self.sources[key]
        return False

class FyOembed(object):
    sites = None

    def get(self, url):
        oembed_url = self.sites.get(url)
        if oembed_url:
            data = {'format': 'json', 'url': url}
            try:
                r = requests.get(oembed_url[0], params=data)
                result = r.json()
            except:
                return False

            if result.has_key('error'):
                return False



            result['fa'] = oembed_url[1]
            result['service'] = oembed_url[2]
               
            return  result
        else: 
            return False

    def __init__(self):
        self.sites = Sites()

        if self.sites.first == False:
            # Dailymotion
            regex = (
                'http://.*\\.dailymotion\\.com/video/.*',
                'http://.*\\.dailymotion\\.com/.*/video/.*',
                'http://dai.ly/*'
            )
            for r in regex:
                self.sites.add(r, 'https://www.dailymotion.com/services/oembed', 'fa-video-camera', 'Dailymotion')

            # Youtube
            regex = (         
                'https?://youtu\\.be/.*',
                'https?://www\\.youtube\\.com/embed/.*',
                'https?://youtube\\.fr/.*',
                'https?://www\\.youtube\\.com/attribution_link.*',
                'https?://youtube\\.com/attribution_link.*',
                'https?://www\\.youtube\\.com/gif.*',
                'https?://youtube\\.com/gif.*',
                'https?://youtube\\.nl/.*',
                'https?://youtube\\.com\\.br/.*',
                'https?://youtube\\.ca/.*',
                'https?://.*\\.youtube\\.com/playlist.*',
                'https?://it\\.youtube\\.com/.*',
                'https?://youtube\\.jp/.*',
                'https?://youtube\\.es/.*',
                'https?://.*\\.youtube\\.com/v/.*',
                'https?://youtube\\.co\\.uk/.*',
                'https?://youtube\\.ie/.*',
                'https?://youtube\\.pl/.*',
                'https?://.*youtube\\.com/watch.*'
            )
            for r in regex:
                self.sites.add(r, 'https://www.youtube.com/oembed?scheme=https&', 'fa-youtube', 'Youtube')

            # Vimeo
            regex = (
                'https?://vimeo\\.com/.*',
                'https?://player\\.vimeo\\.com/.*',
                'https?://www\\.vimeo\\.com/.*'
            )
            for r in regex:
                self.sites.add(r, 'https://vimeo.com/api/oembed.json', 'fa-vimeo', 'vimeo')

            # Instagram
            self.sites.add('https?://www\\.instagram\\.com/p/.*', 'https://api.instagram.com/oembed/', 'fa-instagram', 'Instagram')

            # imgur
            self.sites.add('https?://.*imgur\\.com/.*', 'https://api.imgur.com/oembed', 'fa-file-image-o', 'imgur')

            # Flickr
            regex = (
                'http://www\\.flickr\\.com/photos/.*',
                'http://flic\\.kr/.*'
            )
            for r in regex:
                self.sites.add(r, 'https://www.flickr.com/services/oembed/', 'fa-flickr', 'Flickr')

            # Mixcloud
            self.sites.add('https?://www\\.mixcloud\\.com/.*/.*/', 'https://www.mixcloud.com/oembed', 'fa-mixcloud', 'Mixcloud')

            # Soundcloud
            regex = (
                'https?://soundcloud\\.com/groups/.*',
                'https?://soundcloud\\.com/.*',
                'https?://soundcloud\\.com/.*/.*',
                'https?://soundcloud\\.com/.*/sets/.*'
            )
            for r in regex:
                self.sites.add(r, 'https://soundcloud.com/oembed', 'fa-soundcloud', 'Soundcloud')

            # Spotify
            regex = (
                "^http(?:s)?://open\\.spotify\\.com/.+$",
                "^http(?:s)?://spoti\\.fi/.+$"
            )
            for r in regex:
                self.sites.add(r, 'https://embed.spotify.com/oembed/', 'fa-spotify', 'Spotify')

            # Twitter
            self.sites.add('https?://(www\.)?twitter.com/\S+/status(es)?/\S+', 'https://api.twitter.com/1/statuses/oembed.json', 'fa-twitter', 'Twitter')

            # Scribd
            regex = (
                'http://scribd\\.com/doc/.*',
                'http://www\\.scribd\\.com/doc/.*',
                'http://scribd\\.com/mobile/documents/.*',
                'http://www\\.scribd\\.com/mobile/documents/.*'
            )
            for r in regex:
                self.sites.add('https?://(www\.)?scribd\.com/\S*', 'http://www.scribd.com/services/oembed', 'fa-scribd', 'Scibd')