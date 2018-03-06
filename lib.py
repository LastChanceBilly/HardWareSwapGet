import urllib
import time
import urllib2


def getPosts(url, url_to_find, num_of_pages, limit_config):
    limit = int(limit_config)
    #Where the content of the page will be stored
    page = ' '
    #Viewing area for each while cycle
    view = ' '
    #List containing all the post's titles
    titles = []
    links = []
    current_page = 1
    current_link = url
    #Try to connect to the page
    while(current_page < num_of_pages + 1):
        page = ' '
        request = 0
        tries = 0
        while(page == ' ' and tries < limit):
            try:
                request = urllib2.Request(current_link)
                page = urllib2.urlopen(request).read()
            #If you can't, tell me why
            except:
                print("Can't retrieve content, attempt no.{0}".format(tries))
            tries += 1
            if(page == ' '):
                time.sleep(1)
        titles.append("--Page no. {0}--".format(current_page))
        links.append("--Page no. {0}--".format(current_page))
        index = 0
        while(page.find(url_to_find, index) > 0):
            #Find the post's link, and save it's possition to the index
            index = page.find(url_to_find, index)
            #Get the post's link
            link = page[index: page.find(" ", index) -1]
            #Get the post's name from the link
            content = link[link.find("/", 49) +1:]
            #Eliminate the / and the _ from it
            content = content.replace("_"," ")
            content = content.replace("/", " ")
            if(index > 0):
                index += 1
            titles.append(content)
            links.append(link)
        index = page.find('<span class="next-button">', index)
        current_link = page[page.find("https", index): page.find('" ', index)]
        print(current_link)
        current_page += 1
    return(titles, links)
def formatFixer(title):
    #Get the country and state from the title, and make it uppercase
    country = title[:title.find(" ")].upper()
    #Now add the brackets
    country = "[" + country  + "]"
    #Add [[COUNTRY]-[STATE]]
    if(country.find("USA") > 0):
        country = country.replace("USA", "USA-")
    elif(country.find("CA") > 0):
        country = country.replace("CA", "CA-")
    rest = title[title.find(" ") -1: ]
    #Have
    H = ' '
    if(rest.find(" h ", ) > 0):
        rest = rest.replace(" h ", "[H] ")
        have_beggining = rest.find(" [H] ") + 5
        if(rest.find(" w ") > 0):
            H = rest[have_beggining: rest.find(" w ") -1]
        else:
            H = rest[have_beggining: ]
    elif(country.find("H]") > 0):
        country = country.replace("H]", "][H]")
    elif(rest.find("h") > 0):
        rest = rest.replace("h","[H] ", 1)
    #Want
    W = ' '
    if(rest.find(" w ")):
        rest = rest.replace(" w ", " [W] ")
        want_beggining = rest.find(" [W] ") + 5
        if(rest.find(" [H] ") > 0):
            W = rest[want_beggining: rest.find(" [H] ") -1]
        else:
            W = rest[want_beggining: ]
    elif(country.find("W]")> 0):
        country = country.replace("W]", " ][W] ")
    elif(rest.find("w") > 0):
        rest = rest.replace("w", "[W]", 1)
    return(country + rest[1:])
