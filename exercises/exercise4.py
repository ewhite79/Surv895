#store file name
filename = "RomeoJuliet.txt"

#Open file
Romeo = open("RomeoJuliet.txt","r")

#LINE COUNT
#create empty list
line_list = []

#loop over Romeo
for current_line in Romeo:

	#put each line into list "line_list"
    line_list.append(current_line)

#end loop

#count lines and print
print "Number of lines:", len(line_list)

#WORD COUNT  
#create empty list for words
word_list = []

#loop over lines
for line in line_list:

    #create temp variable to hold list of words
    words = line.split()

    #add individual words into word list
    word_list.extend (words) 

#end loop

#print out word count
print "Number of words:", len(word_list) 

#CHARACTER COUNT
#create variable for character count
char_count=0	

#loop over lines 
for line in line_list:

	#count characters for each line
    char_count += len(line)

#end loop

#print character count
print "Number of characters:", char_count

#CREATE DICTIONARY
#create empty dictionary. 
shakes_dictionary = {}

#loop through word by word
for word in word_list:

	#if word already there, add one to value
    if word in shakes_dictionary:

        shakes_dictionary[word]+=1

    #if word is new, set value to one
    else:

        shakes_dictionary[word]=1

    #end check to see if name is in dictionary

#end dictionary-creation loop

# print the dictionary
print "Shakespeare dictionary:", shakes_dictionary