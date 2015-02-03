#create empty list
line_list = []
#store file name
filename = "RomeoJuliet.txt"
#Open file
Romeo = open("RomeoJuliet.txt", "r")
#loop over Romeo
for current_line in Romeo:
	#put each line into list "line_list"
    line_list.append( current_line )
	#end loop
#count lines and print
print "Number of lines:", len(line_list)
#create variable for word count
word_count=0
#loop over lines
for line in line_list:
    #create temp variable to hold list of words
    words = line.split()
    #add number of words to word count
    word_count += len(words)
	#end loop
#print out word count
print "Number of words:", word_count 
#create variable for character count
char_count=0	
#loop over lines nad count characters
for line in line_list:
    char_count += len(line)
	#end loop
#print character count
print "Number of characters:", char_count
#make one list of all words. create empty list
word_list = []
#loop though by line, split, and put words into one list
for line in line_list:
    wordsagain = line.split()
    word_list.extend (wordsagain) 
    #end loop
#test if I got it right
print "Number of words take 2:", len(word_list)
#make dictionary. create empty dictionary. 
dictionary = {}
#loop through word by word
for word in word_list:
	#if word already there, add one to value
    if word in dictionary:
        dictionary[word]+=1
    #if word is new, set value to one
    else:
        dictionary[word]=1
    #end loop
print(dictionary)
