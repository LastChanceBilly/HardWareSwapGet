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
