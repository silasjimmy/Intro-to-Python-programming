# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Silas Jimmy
# Collaborators: None
# Time: 24hrs

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title.lower()
        self.description =description
        self.link = link
        self.pubdate = pubdate
        
    def get_guid(self):
        return self.guid
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase
        
    def is_phrase_in(self, text):
        return None

class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)
        
    def evaluate(self, story):
        title = story.get_title()
        
        for punctuation in string.punctuation:
            if punctuation in title:
                title = title.replace(punctuation, ' ')
                
        title = [word for word in title.split(sep=' ') if word != '']
        title = ' '.join(title)
        
        if (' ' + self.phrase.lower() + ' ') in (' ' + title.lower() + ' '):
            return True
        return False
        
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)
        
    def evaluate(self, story):
        description = story.get_description()
        
        for punctuation in string.punctuation:
            if punctuation in description:
                description = description.replace(punctuation, ' ')
                
        description = [word for word in description.split(sep=' ') if word != '']
        description = ' '.join(description)
        
        if (' ' + self.phrase.lower() + ' ') in (' ' + description.lower() + ' '):
            return True
        return False
        
class TimeTrigger(Trigger):
    def __init__(self, time):
        time = datetime.strptime(time, "%d %b %Y %H:%M:%S")
        time = time.replace(tzinfo=pytz.timezone("EST"))
        self.time = time
        
class BeforeTrigger(TimeTrigger):
    def __init__(self, time):
        TimeTrigger.__init__(self, time)
        
    def evaluate(self, story):
        pubdate = story.get_pubdate()
        # Convert to the timezone
        pubdate = pubdate.replace(tzinfo=pytz.timezone("EST"))
        
        if pubdate <= self.time:
            return True
        return False
    
class AfterTrigger(TimeTrigger):
    def __init__(self, time):
        TimeTrigger.__init__(self, time)
        
    def evaluate(self, story):
        pubdate = story.get_pubdate()
        # Convert to the timezone
        pubdate = pubdate.replace(tzinfo=pytz.timezone("EST"))
        
        if pubdate > self.time:
            return True
        return False

class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
        
    def evaluate(self, story):
        return not self.trigger.evaluate(story)

class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
        
    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)

class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
        
    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.
    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    filtered_stories = []
    
    for trigger in triggerlist:
        for story in stories:
            if trigger.evaluate(story):
                filtered_stories.append(story)
        
    return filtered_stories

def create_trigger_object(keyword, trigger):
    '''
    Creates a trigger object with one argument.
    keyword (str): The keyword to match with the type of trigger to create.
    trigger (str): The trigger phrase to use as argument in creating the trigger
    Returns: Trigger object
    '''
    if keyword == 'TITLE':
        return TitleTrigger(trigger)
    elif keyword == 'DESCRIPTION':
        return DescriptionTrigger(trigger)
    elif keyword == 'BEFORE':
        return BeforeTrigger(trigger)
    elif keyword == 'AFTER':
        return AfterTrigger(trigger)
    elif keyword == 'NOT':
        return NotTrigger(trigger)
    
def create_trigger_object_1(keyword, trigger1, trigger2):
    '''
    Creates a trigger object with two arguments.
    keyword (str): The keyword to match with the type of trigger to create.
    trigger1 (str): The first trigger argument.
    trigger2 (str): The second trigger argument.
    Returns: Trigger object
    '''
    if keyword == 'OR':
        return OrTrigger(trigger1, trigger2)
    elif keyword == 'AND':
        return AndTrigger(trigger1, trigger2)
    
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file
    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    trigger_file = open(filename, 'r')
    lines = []
    add_line = None
    
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            if line.startswith('ADD'):
                add_line = line
            else:
                lines.append(line)
    
    triggers = {}
    
    for line in lines:
        line = line.split(sep=',')
        if line[1] in ['AND', 'OR']:
            triggers[line[0]] = create_trigger_object_1(line[1], line[2], line[3])
        else:
            triggers[line[0]] = create_trigger_object(line[1], line[2])
            
    # Create the trigger list
    add_line = add_line.split(sep=',')
    add_line.remove('ADD')
    trigger_list = [triggers.get(trigger) for trigger in add_line]
            
    return trigger_list

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

