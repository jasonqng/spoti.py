spoti.py
========

Spotify Poetry

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
