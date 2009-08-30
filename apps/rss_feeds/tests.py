from utils.json import decode
from django.test.client import Client
from django.test import TestCase
from django.core import management

class FeedTest(TestCase):
    fixtures = ['rss_feeds.json']
    
    def setUp(self):
        self.client = Client()

    def test_load_feeds__gawker(self):
        self.client.login(userame='conesus', password='test')
        
        management.call_command('loaddata', 'gawker1.json', verbosity=0)
        response = self.client.get('/reader/refresh_feed', { "feed_id": 1, "force": True })
        
        management.call_command('loaddata', 'gawker2.json', verbosity=0)
        response = self.client.get('/reader/refresh_feed', { "feed_id": 1, "force": True })
        
        response = self.client.get('/reader/load_single_feed', { "feed_id": 1 })
        
        # print [c['story_title'] for c in json.loads(response.content)]
        stories = decode(response.content)
        
        # Test: 1 changed char in content
        self.assertEquals(len(stories), 38)
        
    def test_load_feeds__gothamist(self):
        self.client.login(userame='conesus', password='test')
        
        management.call_command('loaddata', 'gothamist1.json', verbosity=0)
        response = self.client.get('/reader/refresh_feed', { "feed_id": 4, "force": True })
        
        management.call_command('loaddata', 'gothamist2.json', verbosity=0)
        response = self.client.get('/reader/refresh_feed', { "feed_id": 4, "force": True })
        
        response = self.client.get('/reader/load_single_feed', { "feed_id": 4 })
        
        # print [c['story_title'] for c in json.loads(response.content)]
        stories = decode(response.content)
        
        # Test: 1 changed char in title
        self.assertEquals(len(stories), 42)