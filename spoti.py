# -*- coding: utf-8 -*-
import json
import urllib2
from pandas import DataFrame

def description():
    
    print('''
    
    Welcome to Spoti.py
    
    Spoti.py allows the user to convert a poem or any utf-8 string into a 
    Spotify playlist so that the track names spell out the poem. 
    
    The Spotify API search function is used to query song information. This is
    set to return maximum 100 hits per query. The algorithm used in this 
    script takes a brute force approach to solving this problem and returns the 
    optimal solution with fewest number of tracks. The optimising algorithm 
    goes about it by iteratively deleting the last word of the poem until a match 
    is made with a track name. The matching words are then deleted from the 
    original poem and the program loops through again with the slightly 
    shortened poem. This continues until the entire poem has been matched.
    
    This approach causes the run-time to be lengthy for large
    poems. The following shortcuts are introduced to cut down on runtime:
        
    (1) The method of iteratively deleting words until a match is made is 
    applied to 'bite size' chunks of the poem instead of the full size poem.
    The bite sizes are currently set at a length of six words (an assumed 
    maximum on track name length). 
    
    (2) Punctuation helps the script identify the end of a lingustic idea. This
    allows the analyzed bites to be meaningful and more likely to find a match 
    than an aribitrary six word phrase. Thus it is recommended to ADD punctuation 
    (if there is none) to your poem before it runs, in attempt to decrease run-time.
    
    Notes:
        -capitilization does not matter
        -works for any utf-8 string
        -run time shortened by punctuation and bite-method
        -optimizing algorithm finds shortest answer possible
        -Words that cannot be matched to track names are included in square 
         parentheses in the resulting playlist dataframe. 
        
    The visual playlist is contained in the 'playlist' dataframe variable, and 
    the desired url list of tracks is contained in the 'playlist_urls' list 
    variable.

    -Created by Joseph Stockermans 2013
    
    ''')


class Query():
    
    def __init__(self,qstring):
        
        #delimiters are used by several methods so make a list
        #of them into instance variable
        self.delim_list = [',', '.', '?', '!', ';', ':',] 
        
        #create instance variable qstring
        self.qstring = qstring.lower()
        
        #remove in-line quotes
        self.qstring = self.qstring.replace("''", '"')
        self.qstring = self.qstring.replace('"', '')
        self.qstring = self.qstring.replace('”', '')
        self.qstring = self.qstring.replace('’', "'")
        
        #/ to space
        self.qstring = self.qstring.replace('/', ' ')
        
        #... to space
        self.qstring = self.qstring.replace('...', ' ')
        
        #delim list giving problems so change everything to commas
        for delim in self.delim_list:
            self.qstring = self.qstring.replace(delim, ',')
        
        #remove any delimimeters and end of poem.
        if self.qstring[len(self.qstring) - 1:] == ',':
            self.qstring = self.qstring[:len(self.qstring) - 1]
  
        #double spaces to single spaces
        self.qstring = self.qstring.replace('  ', ' ')
        
        #remove any spaces and end of poem.
        if self.qstring[len(self.qstring) - 1:] == ' ':
            self.qstring = self.qstring[:len(self.qstring) - 1]
        
        #utf-8 apostrophes are troublesome so change them manually to ascii
        #change utf-8 to ascii
        self.qstring = self.qstring.decode('utf-8')
        self.qstring = self.qstring.encode('ascii', 'ignore')     
        
        #create an original version of the poem
        self.orig_string = self.qstring.lower()
        
        #define further instance variables to be used
        self.used_string = ''
        self.artist_list = [] 
        self.track_list = []
        self.album_list = []
        self.href_list = []
        self.result_dic = {}
        self.result_frame = DataFrame()
        self.unmatched_string = ''
    
    def space_to_plus(self):
        '''takes the instance var qstring
        replaces ' ' with '+' 
        -----------------------
        returns nothing'''
        
        self.qstring = self.qstring.replace(' ', '+')         
    
    def plus_to_space(self):
        '''takes the instance var qstring
        replaces '+' with ' ' 
        -----------------------
        returns nothing'''
        
        self.qstring = self.qstring.replace('+', ' ')   


    def string_to_bites(self):
        '''takes the instance var qstring and
        updates it to only a chunk (bite) of it,
        the size of which is determined by the 'bite size'.
        --------------------------------------------
        returns the the delimiter used in the current
        bite (if any), else it returns None'''
        
        #define 'bite' size
        bite = 6
        
        #make sure paces are pluses
        self.space_to_plus()
        
        #split string up into list and only add
        #first 5 elements to string my_string.
        
        #we do this by breaking up our instance variable into a list
        #and putting it back together using only the first 5 elements
        #into the local variable my_string
        string_list = self.qstring.split('+', bite)
        string_length = len(string_list)
        my_string = ''
        
        #if the string list length is greater than the bite size,
        #chew it up. Else, if its smaller, just add it all to the current bite
        count = 0
        if string_length >= bite:
            while count < bite:
                my_string = my_string + string_list[count] + '+'
                count += 1
        else:
            while count < string_length:
                my_string = my_string + string_list[count] + '+'
                count += 1
        
        #take off the last '+' and save results back into the local variable
        #qstring
        my_string = my_string.rsplit('+', 1)[0]
        self.qstring = my_string
        
        #delim list changed to just comma
        if ',' in my_string:
            my_string = my_string.split(',', 1)[0]
            self.qstring = my_string
            return ',' + ' '
        
        #if no delimiters, return None
        self.qstring = my_string
        return None


    def search(self):
        '''takes the instance var qstring, calls the api
        and searches spotify for tracks that match qstring
        ------------------------------------------------
        returns a list containing the first result found'''
        
        #make sure spaces are pluses
        self.space_to_plus()
        
        #api stuff
        url = 'http://ws.spotify.com/search/1/track.json?q=' + self.qstring
        data = urllib2.urlopen(url)
        js = json.load(data)
        
        #loop through all results on first page
        results_list = []
        count = 0
        while count < len((js['tracks'])):
            
            #get information we want
            artist_name = js['tracks'][count]['artists'][0]['name'].lower()
            track_name = js['tracks'][count]['name'].lower()
            album_name = js['tracks'][count]['album']['name'].lower()
            
            href_name = js['tracks'][count]['href']
            href_name = href_name.replace('spotify:track:', 'http://open.spotify.com/track/')
            
            #change poem back to spaces to compare against track name
            self.plus_to_space() 
            
            #take the first result that matches exactly
            if self.qstring == track_name:
                
                #results list is needed to show whether the query found something
                current_result = [artist_name, track_name, album_name, href_name]
                results_list.append(current_result)
                
                #individual lists are needed to record data for the DataFrame
                self.artist_list.append(artist_name)
                self.album_list.append(album_name)
                self.href_list.append(href_name)
                
                if self.unmatched_string == '':
                    self.track_list.append(track_name)
                else:
                    self.track_list.append('[' + self.unmatched_string + '] ' + track_name)
                    self.unmatched_string = ''
                
                #break out of loop once the first result is found
                break
            
            count += 1
            
            #change spaces back to pluses
            self.space_to_plus() 
        
        #return results_list to indicate whether a result was found
        return results_list
            
    def search_loop(self):
        '''First calls the string_to_bite method to put qstring
        into a manageable size. Then iteratively calls the search method and deletes
        the final word from qstring if the search method
        returns an empty list. Once a result is found, it updates
        a used_string instance variable to keep track of how much
        of the poem we have turned into track names, and updates
        qstring to what is left to orig_string instance variable
        net of used_string. The loop starts again with the next bite
        and this continues until use_string is equal
        to orig_string.
        --------------------------------------------------
        returns nothing'''
        
        #loop until we've used up the entire original poem
        #space at the end because used string has space at end
        while self.used_string != self.orig_string + ' ':
        
            punctuation = self.string_to_bites()
        
            #keep calling search method while deleting the
            #last word of the poem
            while self.search() == []:
                
                #print('current bite: %s ' %self.qstring)
                
                #control for single words (no plus sign case)
                if '+' in self.qstring:
                    self.qstring = self.qstring.rsplit('+', 1)[0]
                else:
                    
                    #build up unmatched strings in case several are in a row
                    self.unmatched_string = self.unmatched_string + ' ' + self.qstring
                    if self.unmatched_string[:1] == ' ':
                        self.unmatched_string = self.unmatched_string[1:]

                    break
                
            #update strings to prepare for next loop iteration
            if punctuation == None:
                self.qstring = self.qstring + ' '
                self.used_string = self.used_string + self.qstring
            else:
                if self.qstring + punctuation in self.orig_string:
                    self.used_string = self.used_string + self.qstring + punctuation
                else:
                    #this case is for if punctuation existed in the original bite
                    #in which case the punctuation local variable will not be None
                    #but punctuation did not come directly after the current qstring
                    self.qstring = self.qstring + ' '
                    self.used_string = self.used_string + self.qstring
            
            print('poem progress: %s' %self.qstring)
            
            #update qstring to orig_string net of used_string
            #we want to replace only the FIRST instance; since repeated
            #phrases will ALL be deleted. This method screws up at the last
            #word so we need a different method at the last word of the poem
            
            if self.used_string == self.orig_string + ' ':
                self.qstring = self.orig_string.replace(self.used_string, '')
            else:
                self.qstring = self.orig_string.split(self.used_string, 1)[1]
                
            #if unmatched string is the last word in the poem
            #we need to add it at the end as the search function
            #where tracks are appended to track_list won't be called
            #anymore
            if self.used_string == self.orig_string + ' ' and self.unmatched_string != '':
                self.track_list[-1] = self.track_list[-1] + ' [' + self.unmatched_string + ']'
            
            #print('poem progress: %s' %self.used_string)
            #print('orig: %s' %self.orig_string)
            #print('q %s' %self.qstring)
            
    def dic_to_frame(self):
        '''creates a dictionary from artist_list,
        track_list, and album_list instance variables
        and then creates a DataFrame out of that dictionary.
        Prints this dataframe and the associated URLs
        -----------------------------------------------
        returns nothing'''
        
        #create dictionary to be used for the DataFrame
        self.result_dic = {'track': self.track_list, 'artist': self.artist_list, 'album': self.album_list}    
        
        #create DataFrame
        self.result_frame = DataFrame(self.result_dic, columns=['track', 'artist', 'album'])

        return self.result_frame, self.href_list

#print description
description()

#write poem
example = '''if i can't, let it go, out of my mind, i'm scared, my stupid heart, my stupid mouth, will try, finding a way home, home to you, letting you know, all the ways, i want the world to stop, with you'''
tanikawa = '''mother why is the river laughing why because the sun is tickling the river Martians on a little globe Are probably doing something I don't know what'''
fitzgerald = '''So we beat on, boats against the current, borne back ceaselessly into the past.'''
nordine = '''as an intellectual vibration, smack dab in the middle of the spectrum, green can be a problem. That's because there's so many different greens inside of green'''
fuchs = '''I’ve held others before, But it was never like this, Where my body inhales you And quivers with bliss, Where my senses are reeling From the strength of desire, And if I can’t have you soon, I’ll be consumed by the fire.'''
zaqtan = '''Father, father, wake up your sons! Stop leaning out the window! Shake off your sadness!'''
undhr = '''All human beings are born free and equal in dignity and rights. They are endowed with reason and conscience and should act towards one another in a spirit of brotherhood.'''
jouvon = '''Best morning taxi driver yet...He lived in Germany studying Hotel Management for 5 years so cheezy radio off, conversation ON. Canada is his favourite country because "...I haven't been there yet!'' and we talked about bad luck and fate while passing the dying fields ...hm, this taxi habit/addiction to taxi roulette may be why I'm getting poor...'''

#choose poem
poem = example

#create a Query object and initialize it with poem
a_query = Query(poem)

#get results
a_query.search_loop()

#put results in a DataFrame
playlist, playlist_urls = a_query.dic_to_frame()


print(playlist)

for each_url in playlist_urls:
    print(each_url)
    

#{u'album': {u'released': u'2002', u'href': u'spotify:album:2TIp2qGorHvqyaiAb82Awe', u'name': u'One By One', u'availability': {u'territories': u'CA HK MX MY SG US'}},
#u'name': u'Times Like These',
#u'popularity': u'0.43',
#u'external-ids': [{u'type': u'isrc', u'id': u'USRW30200005'}],
#u'length': 265.946,
#u'href': u'spotify:track:2ql32BJPN3hnyboml4JfER',
#u'artists': [{u'href': u'spotify:artist:7jy3rLJdDQY21OgRLCZ9sD',u'name': u'Foo Fighters'}], u'track-number': u'4'}]
