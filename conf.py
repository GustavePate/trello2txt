
from collections import OrderedDict
############ CONFIGURATION ############

#appkey and token (see trello api doc to get yours)

# CHANGE THIS !!!!! (otherwise you will see my fantastic TodoList)
appkey=u'64842214ed17777bee8742f8db14a6b'
token=u'4f5feb695a661b3296789ce6a5fa3565b6cd6eb021f27e2ac6c1514befe65b1'

#Board to monitor id (see Trello url)
# CHANGE THIS !!!!!
board=u'GKubRtoN'

#Possible behaviour
BY_COLOR=0
BY_NUMBER=1

# list here the name of  lists to be monitored and the desired behaviour for each list
# list all = BY_COLOR with no color filter specified
# CHANGE THIS !!!!!
toanalyse = OrderedDict()
toanalyse[u'List1_name']=BY_COLOR
toanalyse[u'List2_name']=BY_COLOR
toanalyse[u'List3_name']=BY_NUMBER

#IF you choose a by number behaviour, the number of cards to retrieve
BY_NUMBER_COUNT=10

# color filter
# List the card colors you wan't to display
# the dic value is a prefix added to the card text in the rendered list
# set an empty dic to display all cards
COLOR_TO_DISPLAY={}
COLOR_TO_DISPLAY['red']='!'
COLOR_TO_DISPLAY['orange']=""
#COLOR_TO_DISPLAY[u'yellow']=""
#COLOR_TO_DISPLAY[u'green']=""


############ END OF CONFIGURATION ############
