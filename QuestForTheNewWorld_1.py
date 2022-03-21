#Import pygame and sys module
import pygame, sys

#Import useful constants
from pygame.locals import *
import math

#GAME ENGINE CONSTANTS - GAME CONSTANTS LOCATED IN DEFINES FILE
FPS = 60 # frames per second to update the screen
WINDOWWIDTH = 1000  # width of the program's window, in pixels
WINDOWHEIGHT = 750 # height in pixels

BGTEXTURE = pygame.image.load('gfx/background_texture.png') #texture is 40x40


#Margin and spacing of objects
XMARGIN = 40
XSPACING = 40
YMARGIN = 40
YSPACING = 40
#Size of useable interface
XINTERFACESIZE = WINDOWWIDTH - 2 * XMARGIN #effective length bounded by border
XUSERBARSIZE = XINTERFACESIZE + XMARGIN #width of user info bar and menu

YUSERBARSIZE = 50 #height of user info bar and menu
YINTERFACESIZE = WINDOWHEIGHT - 2 * YSPACING - YUSERBARSIZE #effective height bounded by border
#USERBAR
UBTEXTURE = pygame.image.load('gfx/userbar_texture.png') #texture is 10x10  
UBHOVERTEXTURE = pygame.image.load('gfx/userbar_button_texture_hover.png') #texture is 10x10


BORDERWIDTH = 5 #Default width of outside border

#Colours
PURPLE    = (255,   0, 255)
BEIGE     = (255, 204, 128)
BLUE      = (  0,   0, 255)
RED       = (255, 100, 100)
YELLOW    = (255, 255,   0)
BLACK     = (  0,   0,   0)
BROWN     = ( 85,  65,   0)
WHITE     = (255, 255, 255)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 128,   0)
LIGHTGREY = (205, 205, 205)
DARKGREY  = (105, 105, 105)

HIGHLIGHTCOLOUR = PURPLE # colour of the highlighted event optionsr
BGCOLOUR = BEIGE # background colour on the screen
BORDERCOLOUR = BLACK #colour of border line
EVENTTITLECOLOUR = WHITE # colour of the text for the event title
EVENTTEXTCOLOUR = WHITE # colour for event description text
EVENTOPTIONCOLOUR = WHITE # colour for event description text
EVENTTITLESIZE = 20 #Font size of event headings
EVENTTEXTSIZE = 16 #Font size of event descriptions and options
EVENTOPTTEXTSIZE = 12 #Font size of event option text
USERBARFONTSIZE = 12 #Font size for main text in the userbar
POPUPBOXSMALL = 10 #font size for small popup box text
JOURNALHEADING = 16 #Font size for header items in the journal
JOURNALBODY = 12 #font size for main text of the journal
EVENTPICTUREDEFAULT = pygame.image.load('gfx/events/image_not_found.png') #default event picture if none found
EVENTPICTURESIZE = (400, 200) #picture is 300x200 by default

LINESPACING = 0 #spacing between lines. <0 is smaller spacing

#Event display
#HEADER
XHEADERSIZE = XINTERFACESIZE #length of header text box (one line of text only)
YHEADERSIZE = EVENTTITLESIZE + 5 #height of header text box (one line of text only)
#DESCRIPTION
XDESCRIPTIONSIZE = XINTERFACESIZE #width of event description text box (multi-lines)
YDESCRIPTIONSIZE = int(YINTERFACESIZE/2) #Height of event description text box
#OPTION
XOPTIONSIZE = int(XINTERFACESIZE/2) #length of event option text box
YOPTIONSIZE = EVENTOPTTEXTSIZE + 5 #height of event option text box
#FOOTER
XFOOTERSIZE = XINTERFACESIZE #length of footer box (one line of text only)
YFOOTERSIZE = EVENTTITLESIZE + 5 #same height as header box (one line of text only)


POPUPBOXHEIGHT = int(WINDOWHEIGHT/12) #default height of a popup box
POPUPBOXWIDTH = int(WINDOWWIDTH/4) #default width of a popup box
XPOPUPOFFSET = 5 #offset of popup box from cursor in X direction
YPOPUPOFFSET = 5 #offset of popup box from cursor in Y direction

JOURNALINTERFACESIZE = [int(WINDOWWIDTH/1.5), int(WINDOWHEIGHT/1.5)] #jorunal interface - to be centered
JOURNALBORDERCOLOUR = BEIGE

#misc constants
ALLEVENTS = 'All Events'
RANDEVENTCOND = 'Random Event Conditions'
RANDEVENTDATA = 'Random Event Data'
MAXOPTIONS = 8 #maximum number of allowed displayed options

#SHIP DEFINES
#to be moved into script to allow custom boat selection
DISTANCE_COVERED = 1000 #km - to be moved into event database by defining a latitude and longitude for events and then calculating the distance between them
#MIN_SPEED = 10 #km/day - superceded
#MAX_SPEED = 130 #km/day - superceded
#SPEED_RANGE = MAX_SPEED - MIN_SPEED #km/day - superceded
#RECOMMENDED_SPEED = MIN_SPEED + 0.75 * SPEED_RANGE #km/day - typically should be around 100. - currently no use
#RECOMMENDED_CREW = 100 #crew - superceded
DAILY_FOOD_CONSUMPTION = 0.1 #per crew member

BASE_DEATH_CHANCE = 0.1 #percent per person per day

#ICONS
FOODICON = pygame.image.load('gfx/food_icon.png') #food icon
#CREWICON = pygame.image.load('gfx/crew_icon.png') #crew icon
GOLDICON = pygame.image.load('gfx/gold_icon.png') #gold icon
TREASUREICON = pygame.image.load('gfx/treasure_icon.png') #treasure icon

BUTTONICON = pygame.image.load('gfx/dummy_button.png') #test icon for buttons




###IDEAS###
#Replayability: score/100 is awarded in gold (to the family of the hero) which the player can use in their next attempt to buy more supplies or a better ship
#add weightings to random events and random rolls


def main():
    global FPSCLOCK, DISPLAYSURF, GAMESOUNDS, FONTBOOK
    #Initilise Pygame
    pygame.init()
    FPSCLOCK = pygame.time.Clock() #NOT SURE YET HOW THIS WORKS
    #New drawing surface (window) 1000 x 600 px (w x h)
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) #full drawing surface
    
    GAMENAME = 'Quest for the New World'
    pygame.display.set_caption(GAMENAME)
    FONTBOOK = {
        'Event Title' : pygame.font.Font('freesansbold.ttf', EVENTTITLESIZE),
        'Event Description' : pygame.font.Font('freesansbold.ttf', EVENTTEXTSIZE),
        'Event Option' : pygame.font.Font('freesansbold.ttf', EVENTOPTTEXTSIZE),
        'User Bar' : pygame.font.Font('freesansbold.ttf', USERBARFONTSIZE),
        'Popup Box Small' : pygame.font.Font('freesansbold.ttf', POPUPBOXSMALL),
        'Journal Heading' : pygame.font.Font('freesansbold.ttf', JOURNALHEADING),
        'Journal Body' : pygame.font.Font('freesansbold.ttf', JOURNALBODY),
    }

      
    
    
    #MAIN loop (this loop allows for restarting)
    while True:
        loadGame()
        runGame()
        
     
def loadGame():
    global ROOT, ALLEVENTDATA, event_history, event_choices_excl_randoms, current_event,OPTIONHANDLES,BUTTONHANDLES,event_history_actual
    #Load game defines
    current_event = 'help.0' #always start at game help, followed by startup event 0    
    event_history = ['startup.0'] #tracking which events the player has: game starts on startup event 0, which is called after the help event (the help event calls the previous event)
    event_choices_excl_randoms = [] #for tracking actual progress and not random events/startup
    event_history_actual = [current_event] #tracks actual events displayed to the player
    #LOAD DEFINEs
    ROOT = loadDefines('setup/defines.txt')
    
    
    
    #INTERNAL DEFINES
    ROOT['SYSTEM']['is_journal_open'] = False
    ROOT['SYSTEM']['days_passed_tracker'] = []
     
    print

    if ROOT['SYSTEM']['is_game_test']:
        print('<<<GAME TESTING>>>')
        print('ROOT->SYSTEM->is_game_test is set to TRUE.\n')
        print(ROOT['SYSTEM']['event_index_test_file'])
        EVENTLIST, RANDOMEVENTCONDITIONS, RANDOMEVENTLIST = loadEvents(ROOT['SYSTEM']['event_index_test_file']) #append '_test' to filename for testing things
    else:
        EVENTLIST, RANDOMEVENTCONDITIONS, RANDOMEVENTLIST = loadEvents(ROOT['SYSTEM']['event_index_base_file'])  #CHANGE INDEX FILE TO POINT TO DIRECTORY RATH THAN INDIVIDUAL FILES (once namespaces are added)
    
    ALLEVENTDATA = {
        ALLEVENTS : EVENTLIST,
        RANDEVENTCOND : RANDOMEVENTCONDITIONS,
        RANDEVENTDATA : RANDOMEVENTLIST
        } 
    
    print
    print('Setup complete.\n')
    
    #chosen_name = input('>>>Enter Name: ') #User-inputted name
    chosen_name = 'Frodo'
    ROOT['PLAYER'].update({'name': chosen_name})

    print
    print('Welcome, '+chosen_name+'...')
    print

    
    OPTIONHANDLES = [] #Storage list for object handles for the option buttons
    for ii in range (0,MAXOPTIONS):
        OPTIONHANDLES.append(None)  
        
    BUTTONHANDLES = {} #storage dictionary for all UI buttons

        
def runGame():
    global optnum
    #Main game engine loop
    while True:
        #get all events from user
        for event in pygame.event.get():
            #If user wants to quit... (escape key)
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                print('###QUITTING GAME###\nThanks for playing :)')
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_BACKSPACE:
                print('###RESTARTING GAME###')
                return # start a new game (backspace key)
            
            #check if an event option was pressed
            optnum = 1
            for option in OPTIONHANDLES:
                if option is not None:
                    option.check_event(event)
                    
                optnum += 1
                
            #check if any other button was pressed
            for button in BUTTONHANDLES.values():
                if button is not None:
                    button.check_event(event)                 
            
              
              
        
        
        #Update the interface
        updateUserInterface()
        
        #ADD HERE GAME STATE CHECKS. E.G. IS IT A NEW DAY? If so, compute resource changes, etc.
        checkDailyEvents() #seperate game-over check from daily event function?
        if ROOT['SYSTEM']['is_game_over']:
            #crude game over thing for now
                    
            #updateUserInterface()
            will_play_again = input("Play again? ")
            if will_play_again == 'yes':
                break
            else:
                print('###QUITTING GAME###\nThanks for playing :)')
                pygame.quit()
                sys.exit()                
            
   
def checkDailyEvents():
    #Does "Daily stuff". One day being each event that occurrs.
    #Things such as:
    #Resources and score
    #loosing/winning conditions
    global current_event, ALLEVENTDATA
    from random import uniform
    
    #GET BASE DATA
    SYSTEM = ROOT['SYSTEM']
    PLAYER = ROOT['PLAYER']
    ALLSHIPS = ROOT['SHIPS']
    SHIP = ALLSHIPS['$'+ROOT['PLAYER']['current_ship']] #"$" before shipname accesses data for the ship, rather than the ship value itself.  
    if EVENTDATA.isFreshEvent: #new event of any kind
        #COMPUTE storage space remaining
        PLAYER['total_storage_space'] = int(int(float(SHIP['storage_space']) + PLAYER['extra_storage_space']) * PLAYER['storage_space_modifier'])
        food_storage = 2.0 * PLAYER['food_amount']
        gold_storage = 1.0 * PLAYER['gold_amount']
        crew_storage = 5.0 * PLAYER['crew_amount']
        treasure_storage = 3.0 * PLAYER['treasure_amount']
        
        storage_used = food_storage + gold_storage + crew_storage + treasure_storage
        PLAYER['storage_used'] = storage_used
        
        PLAYER['remaining_storage_space'] = PLAYER['total_storage_space'] - storage_used  
        
        if PLAYER['remaining_storage_space'] < 0: #overstorage negatively affects sailing speed, food consumption, death chance and prestige
            overstorage_modifier = 1 - PLAYER['remaining_storage_space']/1000
        else: overstorage_modifier = 1    
        
    
    
    if EVENTDATA.isFreshEvent and not EVENTDATA.isStartupEvent and not EVENTDATA.isHelpEvent:
        #progressing of time throughout game. Time passed between events depends on speed of boat and amount of crew
        #random events progress at 1/10 the time.
        #crew eat food and prestige decays. Crew members may die...
        #print('This is a fresh event.')
   
        ###RESOURCE UPKEEP###
        #If the player is not in a startup or random event:
        #apply daily food and prestige upkeep
        #Compute day passage and food consumption based on distance covered and boat speed
        #ALL events in the startup namespace do not cost food upkeep
        
        
    

        #sailing speed and food intake
        speed_range = float(SHIP['max_speed']) - float(SHIP['min_speed'])
        crew_ratio_actual = PLAYER['crew_amount'] / float(SHIP['recommended_crew']) #ratio of no. crew to recommended no. for the used ship
        sailing_speed_actual = max(float(SHIP['min_speed']) + crew_ratio_actual * speed_range * (1 - crew_ratio_actual / 4 ), float(SHIP['min_speed'])) #scaling of sailing speed based on crew ratio - optimises at 2*recommended_crew
        random_factor_1 = float(uniform(0.8,1.2)) #random factor applied to sailing speed
        days_passed_actual = int(DISTANCE_COVERED * overstorage_modifier / (sailing_speed_actual * random_factor_1 * float(PLAYER['sail_speed_modifier']))) #days passed, based on distance covered and sailing speed
        
        #CHECK HERE FOR RANDOM EVENTS
        if not EVENTDATA.isRandomEvent:
            is_in_random_event = False
            #print('##Checking RANDOM events')
            for day_num in range(1,days_passed_actual+1):
                
                if not is_in_random_event:
                    rand_roll = rand_roll = int(uniform(0,100 + int(PLAYER['prestige']/2))) #chqnce of random event occuring is 1 out of 100 +/- half of prestige
                    if SYSTEM['random_event_chance'] > rand_roll:
                        chosen_event, is_in_random_event = evaluate_random_events(ALLEVENTDATA[ALLEVENTS], ALLEVENTDATA[RANDEVENTCOND], ALLEVENTDATA[RANDEVENTDATA])
                        if is_in_random_event:
                            current_event = chosen_event
                            #print('Day ' + str(day_num) + ': a random event occurred! (id ' + str(current_event) + ')')
                            print('A random event occurred! (id: ' + str(current_event) + ')')                                                                                
                        
                #if not is_in_random_event:
                    #print('Day ' + str(day_num) + ': no random event.')
                
            if is_in_random_event:
                event_history.append(current_event)
                days_passed_actual = math.ceil(days_passed_actual/10) #random event day passage: 1/10 of actual, ROUNDED UP - #CURRENTLY NOT SHOWING IN EVENT UI
        
         
        random_factor_2 = float(uniform(0.9,1.1)) #random factor applied to food consumed
        food_consumed_actual = int((PLAYER['crew_amount'] + 1) * DAILY_FOOD_CONSUMPTION * float(PLAYER['food_consumption_modifier']) * overstorage_modifier * days_passed_actual * random_factor_2) #food consumed across all crew members and all days (the +1 to crew amount accounts for the player themself)
        
        #crew deaths
        #death chance: x2 at -100 prestige, x1 at 0 prestige, x0.5 at +100 prestige
        #death chance will increase if the player's stored gold is less than the amount of crew
        abandonment_factor = 1 - min(PLAYER['gold_amount'] - PLAYER['crew_amount'],0)/1000
        death_chance = BASE_DEATH_CHANCE * abandonment_factor * PLAYER['death_rate_modifier'] * overstorage_modifier / (0.25 * (PLAYER['prestige']/100)**2 + 0.75 * (PLAYER['prestige']/100) + 1)
        crew_deaths = 0
        for person in range(1,int(PLAYER['crew_amount'])): #check all persons
            random_factor_3 = float(uniform(0,100/death_chance)) #compute chance of death for person
            if random_factor_3 < days_passed_actual:
                crew_deaths += 1
                

        #print('Days passed: ' + str(days_passed_actual))
        SYSTEM['EV_days_passed'] = days_passed_actual  #EV stands for event - meaning the statistic is event-specific
        PLAYER['days_passed'] += days_passed_actual #passage of time
        
        
        #FOOD consumption
        SYSTEM['EV_food_consumed'] = food_consumed_actual
        #print('Your crew consume ' + str(food_consumed_actual) + ' food on the journey.')
        PLAYER['food_amount'] -= food_consumed_actual #food upkeep per event
        
        #deaths
        SYSTEM['EV_crew_deaths'] = crew_deaths
        #print('You lose ' + str(crew_deaths) + ' crew members during the journey.')
        PLAYER['crew_amount'] -= crew_deaths #food upkeep per event     
        
       
        
        
        #PRESTIGE DECAY
        prestige_decay = 0.01 * PLAYER['prestige_decay_modifier'] / overstorage_modifier #1% decay per day base
        if PLAYER['allegiance'].lower() == 'none':
            for ii in range(1,days_passed_actual):
                PLAYER['prestige'] += 0.1 #no ally gives passive 0.1 prestige per day
                PLAYER['prestige'] *= (1 - prestige_decay) 
        else:
            PLAYER['prestige'] *= (1 - prestige_decay) ** days_passed_actual #prestige decays by 1% each day.
        PLAYER['prestige'] = max(min(PLAYER['prestige'], 100), -100) #prestige scales from -100 to 100
            
            
        #Compute new score
        ally_score = PLAYER['allegiance'].lower()

        food_score = PLAYER['food_amount']
        crew_score = PLAYER['crew_amount'] * 2
        gold_score = PLAYER['gold_amount'] * 3
        treasure_score = ROOT['PLAYER']['treasure_amount'] * 8
        discoveries_score = len(PLAYER['discoveries']) * 5
        
        timeframe_score_modifier = float(1 + PLAYER['days_passed']/(5 * 365)) #increases by 0.2 per year
        prestige_score_modifier = float(1 + PLAYER['prestige']/100) #0.01 extra per point of prestige
        
        #COUNTRY MODIFIERS
        if ally_score == 'france': #FRANCE = 50% MORE FOR FOOD
            food_score *= 1.5
        elif ally_score == 'england': #ENGLAND = 50% MORE FOR CREW
            crew_score *= 1.5
        elif ally_score == 'netherlands': #NETHERLANDS = 50% MORE FOR GOLD
            gold_score *= 1.5
        elif ally_score == 'spain': #SPAIN = 50% MORE FOR TREASURE
            treasure_score *= 1.5
        elif ally_score == 'portugal': #PORTUGAL = 50% MORE FOR DISCOVERIES
            discoveries_score *= 1.5
        elif ally_score == 'norway': #NORWAY = LESS DAYS PER TIMEFRAME - higher score multiplier per day
            timeframe_score_modifier = float(1 + PLAYER['days_passed']/(4 * 365)) #increases by 0.25 per year
        elif ally_score == 'china': #CHINA = MORE FROM HIGH PRESTIGE, less from low prestige
            prestige_score_modifier = float(1 + PLAYER['prestige']/80) #0.0125 per point of prestige             
        
        PLAYER['score'] += (food_score + crew_score + gold_score + treasure_score + discoveries_score) * timeframe_score_modifier * prestige_score_modifier/100 * days_passed_actual/10
    
            
            
        #check active modifiers and reduce their duration
        #print(ROOT['PLAYER']['active_modifiers'])
        updateActiveModifiers(days_passed_actual)
        
            
        
        #Check loosing conditions
        if PLAYER['food_amount'] <= 0:
            print('The rum is gone... why is the rum always gone?\nYour crew have eaten all the food and everyone (including you) has starved to death!')
            SYSTEM['is_game_over'] = True
        elif PLAYER['crew_amount'] <= 0:
            print('Your crew... they have deserted you.\nYou cannot complete this expedition on your own! You are left to the wilderness. Maybe death will greet you before loneliness does.')
            SYSTEM['is_game_over'] = True        
        
        
        
        
        
    ROOT['PLAYER'] = PLAYER #reassign updated playerstate to ROOT variable
    ROOT['SYSTEM'] = SYSTEM #reassign updated systemstate to ROOT variable
    
    
    if EVENTDATA.isFreshEvent:
        event_history_actual.append(current_event)
        SYSTEM['days_passed_tracker'].append(PLAYER['days_passed']) #passage of events and days etc should be tracked in a seperate, self-contained unit and updated daily.        
        EVENTDATA.isFreshEvent = False


def updateActiveModifiers(days_passed_actual):
    #Check all active modifiers on player, update remaining time and remove if neccessary
    global ROOT
    
    active_modifiers = ROOT['PLAYER']['active_modifiers']
    new_modifier_list = []
    
    printText = False
    if printText: print('ACTIVE MODIFIERS: ', str(active_modifiers))
    for modifier_num in range(0,len(active_modifiers)):
        modifier_data = active_modifiers[modifier_num]
        #print(modifier_data)
        #for modifier_subnum in range(0,len(modifier_data[0])):
        if printText: print('#Updating modifier: ', str(modifier_data))
        
        retained_modifier = [[],[],[],[],[]]
        
        modifier_type = modifier_data[0].lower()
        modifier_target = modifier_data[1]
        modifier_effect = modifier_data[2]
        modifier_duration = modifier_data[3]
        modifier_value = modifier_data[4] #amount the modifier changed 
        
        modifier_duration -= days_passed_actual
        modifier_duration = max(modifier_duration, 0) 
        modifier_data[3] = modifier_duration          
        
        current_modifier_data = [modifier_type, modifier_target, modifier_effect, modifier_duration, modifier_value]
            
        #if printText: print('Current submodifier: ', str(current_modifier_data))

        if modifier_duration == 0: #modifier has expired
            #inverse modifier
            if modifier_type == 'change':
                modifier_effect = modifier_value #change back to original
            elif modifier_type == 'add':
                modifier_type = 'subtract'
                #modifier_effect = float(modifier_effect)
            elif modifier_type == 'subtract':
                modifier_type = 'add'
                #modifier_effect = float(modifier_effect)
            elif modifier_type == 'multiply':
                modifier_type = 'divide'
                #modifier_effect = float(modifier_effect)
            elif modifier_type == 'divide':
                modifier_type = 'multiply'
                #modifier_effect = float(modifier_effect)
            #apply modifier
            current_modifier_data = [[modifier_type], [modifier_target], [modifier_effect], [modifier_duration], [modifier_value]]
            if printText: print('>Removing modifier: ', str(current_modifier_data))
            apply_event_modifiers(current_modifier_data)
        
        else:
            #submodifier has not expired, so add it to the lsit of retained submodifiers and reconstruct modifier
            retained_modifier = modifier_data
            
                
        
        if retained_modifier[0] != []:
            new_modifier_list.append(retained_modifier) #retain modifier effects that haven't expired
            if printText: print('>Retained modifier: ', str(retained_modifier))    
            if printText: print('\n')
    
    #update player's active modifier list
    ROOT['PLAYER']['active_modifiers'] = new_modifier_list
    
    
    
   
def updateUserInterface():
    #Refreshes the user interface entirely
    #Refresh Background
    global EVENTDATA, BUTTONHANDLES
    
    #background UI STUFF
    DISPLAYSURF.fill(WHITE)
    drawTexture((0,0,WINDOWWIDTH,WINDOWHEIGHT), DISPLAYSURF, BGTEXTURE, True)

    #Add border to background
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOUR, (int(XMARGIN/2), int(YMARGIN/2), XINTERFACESIZE + XMARGIN, YINTERFACESIZE + YMARGIN), BORDERWIDTH)
    
    ##USERBAR
    #draw userbar
    x_start = int(XMARGIN/2)
    y_start = YINTERFACESIZE + int(YMARGIN/2) + YSPACING
    b_space_scale = 0.1 #space between buttons is 10% of standard X-spacing
    userBarRect = (x_start, y_start, XUSERBARSIZE, YUSERBARSIZE)
    pygame.draw.rect(DISPLAYSURF, WHITE, userBarRect)
    #add texture to userbar
    drawTexture(userBarRect, DISPLAYSURF, UBTEXTURE, True)
    
    #playerinfobutton
    playerButtonWidth = 0.085
    playerButtonRect = (int(XMARGIN/2),
                        YINTERFACESIZE + int(YMARGIN/2) + YSPACING,
                        int(XUSERBARSIZE * playerButtonWidth - 0*XMARGIN/2 - XSPACING*b_space_scale),
                        YUSERBARSIZE)
    #shipinfobutton
    shipButtonWidth = 0.085
    shipButtonRect = (int(playerButtonRect[0]+playerButtonRect[2] + XSPACING * b_space_scale/2),
                      YINTERFACESIZE + int(YMARGIN/2) + YSPACING,
                      int(XUSERBARSIZE * shipButtonWidth - XSPACING * b_space_scale),
                      YUSERBARSIZE)
    #resourceinfobutton
    storageButtonWidth = 0.085
    storageButtonRect = (int(shipButtonRect[0]+shipButtonRect[2] + XSPACING * b_space_scale/2),
                         YINTERFACESIZE + int(YMARGIN/2) + YSPACING,
                         int(XUSERBARSIZE * storageButtonWidth - XSPACING * b_space_scale),
                         YUSERBARSIZE)
    #discoveries button
    discoveriesButtonWidth = 0.085
    discoveriesButtonRect = (int(storageButtonRect[0]+storageButtonRect[2] + XSPACING * b_space_scale/2),
                             YINTERFACESIZE + int(YMARGIN/2) + YSPACING,
                             int(XUSERBARSIZE * discoveriesButtonWidth - XSPACING * b_space_scale),
                             YUSERBARSIZE)    
    #modifiers button
    modifierButtonWidth = 0.085
    modifierButtonRect = (int(discoveriesButtonRect[0]+discoveriesButtonRect[2] + XSPACING * b_space_scale/2),
                          YINTERFACESIZE + int(YMARGIN/2) + YSPACING,
                          int(XUSERBARSIZE * modifierButtonWidth - XSPACING * b_space_scale),
                          YUSERBARSIZE)
    spacer_width = 0.0125 #spacing between buttons and text
    #resources infobox
    resourceInfoWidth = 0.25
    resourceInfoRect_1 = (int(modifierButtonRect[0]+modifierButtonRect[2] + spacer_width*XUSERBARSIZE + XSPACING * b_space_scale/2),
                          YINTERFACESIZE + int(YMARGIN/2) + YSPACING,
                          int(XUSERBARSIZE * resourceInfoWidth/2 - XSPACING * b_space_scale),
                          YUSERBARSIZE)       
    resourceInfoRect_2 = (int(resourceInfoRect_1[0]+resourceInfoRect_1[2] + XSPACING * b_space_scale/2),
                          YINTERFACESIZE + int(YMARGIN/2) + YSPACING,
                          int(XUSERBARSIZE * resourceInfoWidth/2 - XSPACING * b_space_scale),
                          YUSERBARSIZE)           
    #Event text box
    eventBoxWidth = 0.3
    eventTextRect = (int(XUSERBARSIZE * (1 - eventBoxWidth) + XSPACING * b_space_scale/2),
                     YINTERFACESIZE + int(YMARGIN/2) + YSPACING,
                     int(XUSERBARSIZE * eventBoxWidth - 0*XMARGIN - XSPACING * b_space_scale/2),
                     YUSERBARSIZE)
    
    
    PLAYER = ROOT['PLAYER']
    all_ships = ROOT['SHIPS']
    SHIP = all_ships['$'+ROOT['PLAYER']['current_ship']] #"$" before shipname accesses data for the ship, rather than the ship value itself.

    #info text box
    #infoBoxwidth = 0.6 #portion of total width of userbar
    #infoTextRect = (int(XMARGIN), YINTERFACESIZE + int(YMARGIN/2) + YSPACING, int(XUSERBARSIZE * infoBoxwidth - XMARGIN - XSPACING/4), YUSERBARSIZE)
    
    ##INFO TEXT BOX
    #userbarText = (PLAYER['name'] + '   Role: ' + str(PLAYER['role'].capitalize()) + 
          #'   Allegiance: ' + str(PLAYER['allegiance'].capitalize()) +
          #'   Days: ' + str(int(PLAYER['days_passed'])) +
          #'   Score: ' + str(int(PLAYER['score'])) + 
          #'   Prestige: ' + str(round(PLAYER['prestige'], 2)) + '\n' +
          #'Ship: ' + str(PLAYER['current_ship'].capitalize()) +
          #'   Max Speed: ' + str(int(SHIP['max_speed'])) + 'km/day' +
          #'   Opt. Crew: ' + str(int(SHIP['recommended_crew'])*2) + '\n' +
          #'Rem. Storage: ' + str(int(PLAYER['remaining_storage_space'])) +
          #'   Food: ' + str(int(PLAYER['food_amount'])) + 
          #'   Crew: ' + str(int(PLAYER['crew_amount'])) + 
          #'   Gold: ' + str(int(PLAYER['gold_amount'])) + 
          #'   Treasure: ' + str(int(PLAYER['treasure_amount']))
          
          #)   #move into popup boxes under categories <player name> <ship name> and <resources>?
    
    #drawText(DISPLAYSURF, userbarText, WHITE, infoTextRect, FONTBOOK['User Bar'], aa=True, bkg=None)
    
    
    #PLAYER Button
    playerInfoText = str(
        str(PLAYER['name'].capitalize()) + ' ' + PLAYER['title'] + '\n' +
        'Role: ' + str(PLAYER['role'].capitalize()) + '\n' +
        'Allegiance: ' + str(PLAYER['allegiance'].capitalize()) + '\n' +
        ' \n' +
        'Score: ' + str(int(PLAYER['score'])) + '\n')
    
    player_button = Button(playerButtonRect,
                             BLACK,
                             playerButtonPressFcn, 
                             text = PLAYER['name'].capitalize(), 
                             font = FONTBOOK['User Bar'], 
                             hover_color = DARKGREY, 
                             call_on_release = False,
                             has_popup_box = True,
                             popup_box_text = str(playerInfoText),
                             popup_box_location = 'top right',
                             popup_box_xScale = 0.5,
                             texture = UBTEXTURE,
                             border_width = 0,
                             hover_border_width = 4) 
    player_button.update(DISPLAYSURF)
    BUTTONHANDLES.update({'player_button':player_button})
    #SHIP Button
    shipInfoText = str(
        'Max Speed: ' + str(int(float(SHIP['max_speed']) * float(PLAYER['sail_speed_modifier']))) + 'km/day' + '\n' +
        'Optimal Crew: ' + str(int(SHIP['recommended_crew'])*2)  + '\n' +
        'Max Storage: ' + str(PLAYER['total_storage_space']) + '\n' +
        'Remaining Space: ' + str(int(PLAYER['remaining_storage_space'])) 
        )
    ship_button = Button(shipButtonRect,
                             BLACK,
                             playerButtonPressFcn, 
                             text = PLAYER['current_ship'].capitalize(), 
                             font = FONTBOOK['User Bar'], 
                             hover_color = DARKGREY, 
                             call_on_release = False,
                             has_popup_box = True,
                             popup_box_text = str(shipInfoText),
                             popup_box_location = 'top middle',
                             popup_box_xScale = 0.6,
                             texture = UBTEXTURE,
                             border_width = 0,
                             hover_border_width = 4)  
    ship_button.update(DISPLAYSURF)
    BUTTONHANDLES.update({'ship_button':ship_button})
    #RESOURCES Button
    storageInfoText = str(
        'Storage Used: ' + str(int(PLAYER['storage_used'])) + '/' + str(int(int(SHIP['storage_space']) * PLAYER['storage_space_modifier'])) + '\n' +
        'Food Storage: ' + str(int(PLAYER['food_amount'] * 2)) + '\n' +
        'Crew Storage: ' + str(int(PLAYER['crew_amount'] * 5)) + '\n' +
        'Gold Storage: ' + str(int(PLAYER['gold_amount'] * 1)) + '\n' +
        'Treasure Storage: ' + str(int(PLAYER['treasure_amount'] * 3)) 
        )  
    storage_button = Button(storageButtonRect,
                             BLACK,
                             storageButtonPressFcn, 
                             text = 'Storage', 
                             font = FONTBOOK['User Bar'], 
                             hover_color = DARKGREY, 
                             call_on_release = False,
                             has_popup_box = True,
                             popup_box_text = str(storageInfoText),
                             popup_box_location = 'top middle',
                             popup_box_xScale = 0.6,
                             texture = UBTEXTURE,
                             border_width = 0,
                             hover_border_width = 4)  
    storage_button.update(DISPLAYSURF)
    BUTTONHANDLES.update({'storage_button':storage_button})
    #DISCOVERIES Button
    if PLAYER['discoveries'] == []:
        discoveries_string = 'You have not discovered anything yet.'
    else:
        discoveries_string = 'You have discovered the following:'
        for disc_item in PLAYER['discoveries']:
            discoveries_string = '\n'.join([discoveries_string, '>' + disc_item.capitalize()])
            
    discoveries_button = Button(discoveriesButtonRect,
                             BLACK,
                             discoveriesButtonPressFcn, 
                             text = 'Discoveries', 
                             font = FONTBOOK['User Bar'], 
                             hover_color = DARKGREY, 
                             call_on_release = False,
                             has_popup_box = True,
                             popup_box_text = str(discoveries_string),
                             popup_box_location = 'top middle',
                             popup_box_xScale = 0.6,
                             texture = UBTEXTURE,
                             border_width = 0,
                             hover_border_width = 4) 
    discoveries_button.update(DISPLAYSURF) 
    BUTTONHANDLES.update({'discoveries_button':discoveries_button})   
    
    #MODIFIERS BUTTON
    modifierInfoText = str('Active Modifiers:')
    
    #print(PLAYER['active_modifiers'])
    
    for modifier in PLAYER['active_modifiers']:
        #print('\nThere is an active modifier')
        #print(modifier)
        mod_type = modifier[0].lower()
        mod_name = modifier[1]
        mod_value = modifier[2]
        mod_duration = modifier[3]
        
        modifierString = '> '
        
        if mod_type == ('multiply' or 'divide'):
            modifierString = ''.join([modifierString, mod_type.capitalize() + ' ' + mod_name + ' by ' + mod_value])
        elif mod_type == 'add':
            modifierString = ''.join([modifierString, mod_type.capitalize() + ' ' + mod_value + ' to ' + mod_name])
        elif mod_type == 'subtract':
            modifierString = ''.join([modifierString, mod_type.capitalize() + ' ' + mod_value + ' from ' + mod_name])                            
        else:
            modifierString = ''.join([modifierString, mod_type.capitalize() + ' ' + mod_name + ' to ' + mod_value.capitalize()])
                
        modifierInfoText = ''.join([modifierInfoText,'\n' + modifierString + ' ('+ str(mod_duration) + 'd)'])
     
    modifier_button = Button(modifierButtonRect,
                             BLACK,
                             modifierButtonPressFcn, 
                             text = 'Modifiers', 
                             font = FONTBOOK['User Bar'], 
                             hover_color = DARKGREY, 
                             call_on_release = False,
                             has_popup_box = True,
                             popup_box_text = modifierInfoText,
                             popup_box_location = 'top middle',
                             popup_box_xScale = 0.9,
                             texture = UBTEXTURE,
                             border_width = 0,
                             hover_border_width = 4) 
    modifier_button.update(DISPLAYSURF)
    BUTTONHANDLES.update({'modifier_button':modifier_button})
    
    #RESOURCE text
    resourceInfoText_1 = str(
        'Day ' + str(int(PLAYER['days_passed'])) + '\n' +
        '       Food: ' + str(int(PLAYER['food_amount'])) + '\n' +
        '       Gold: ' + str(int(PLAYER['gold_amount'])) 
        )
    drawText(DISPLAYSURF, resourceInfoText_1, WHITE, resourceInfoRect_1, FONTBOOK['User Bar'], aa=True, bkg=None)
    resourceInfoText_2 = str(
        'Prestige: ' + str(round(PLAYER['prestige'], 2)) + '\n' +
        'Crew: ' + str(int(PLAYER['crew_amount'])) + '\n' +
        '       Treasure: ' + str(int(PLAYER['treasure_amount']))
        )
    drawText(DISPLAYSURF, resourceInfoText_2, WHITE, resourceInfoRect_2, FONTBOOK['User Bar'], aa=True, bkg=None)
    
    
    #OMG fancy icons!
    DISPLAYSURF.blit(FOODICON, (427, 690))
    DISPLAYSURF.blit(GOLDICON, (427, 705))
    DISPLAYSURF.blit(TREASUREICON, (547, 705)) 
    
    
    #DAILY EVENTS TEXT
    ev_text = (str(ROOT['SYSTEM']['EV_days_passed']) + ' days have passed since last stocktake.' + '\n' +
               'Your crew consumed ' + str(ROOT['SYSTEM']['EV_food_consumed']) + ' food on the journey.' + '\n' +             
               'You lost ' + str(ROOT['SYSTEM']['EV_crew_deaths']) + ' crew members during the journey.')               
               
    drawText(DISPLAYSURF, ev_text, WHITE, eventTextRect, FONTBOOK['User Bar'], aa=True, bkg=None)
    
    #JOURNAL BUTTON
    #this will open a 'diary' of all the events that have happened so you can read your adventure like a book!
    
    #HELP BUTTON
    helpButtonSize = [60,60] #pixels
    helpButtonRect = (WINDOWWIDTH - int(XMARGIN - XSPACING/4) - helpButtonSize[0],
                        int(YMARGIN/2 + YSPACING/4),
                        helpButtonSize[0],
                        helpButtonSize[1])
    help_button = Button(helpButtonRect,
                             BLACK,
                             helpButtonPressFcn, 
                             text = '  Help!!', 
                             font = FONTBOOK['User Bar'], 
                             hover_color = DARKGREEN, 
                             call_on_release = False) 
    help_button.update(DISPLAYSURF)
    BUTTONHANDLES.update({'help_button':help_button})
    
    #JOURNAL BUTTON
    journalButtonSize = [60,60] #pixels
    journalButtonRect = (WINDOWWIDTH - int(XMARGIN - XSPACING/4) - helpButtonSize[0] - XSPACING - journalButtonSize[0],
                      int(YMARGIN/2 + YSPACING/4),
                        journalButtonSize[0],
                        journalButtonSize[1])
    journal_button = Button(journalButtonRect, 
                            BLACK,
                            journalButtonPressFcn, 
                            text = 'Journal', 
                            font = FONTBOOK['User Bar'], 
                            hover_color = DARKGREEN, 
                            call_on_release = False) 
    journal_button.update(DISPLAYSURF)
    BUTTONHANDLES.update({'journal_button':journal_button})    
    
    #Get current EVENT and display
    EVENTDATA = ALLEVENTDATA[ALLEVENTS][current_event]
    
    #Update options
    for ii in range (0,MAXOPTIONS):
        OPTIONHANDLES[ii] = None #prepare option button data
    EVENTDATA.display_event() #display event  
    for option in OPTIONHANDLES:
        if option is not None:
            option.update(DISPLAYSURF) #display the options        
       
       
    ###BRING POPUP BOXES TO THE FRONT OF THE SCREEN
    #Check for popupboxes in option buttons from within the overall options database
    for option in OPTIONHANDLES:
        if option is not None and option.hovered:
            option.check_hover() #check for popup boxes and put them on top of EVERYTHING (by default it only puts it infront of the current button)   
    #Check for popupboxes in locally created buttons
    for value in vars().values():
        if type(value).__name__ == 'Button': #if the variable is a button
            button_properties = vars(value)
            if button_properties['hovered']: #check if it is hovered over
                value.check_hover() #bring popup box to front
                
                
    ###CHECK JOURNAL
    if ROOT['SYSTEM']['is_journal_open']:
        drawJournalInterface()
                       


    if ROOT['SYSTEM']['is_game_over']:
        boundingRect = (400, 400, 100, 100)
        excessText = drawText(DISPLAYSURF, 'GAME OVER - please stop the simulation in Wing101', RED, boundingRect, FONTBOOK['Event Title'])            
                
    #Update display window
    pygame.display.update()  
    
    
def journalButtonPressFcn(obj):
    #User presses the 'journal' button
    ## Brings up a log of all the player's previous events like a diary, for them to read through their story.
    
    global ROOT
    
    is_journal_open = ROOT['SYSTEM']['is_journal_open'] 
    
    if is_journal_open: #close the journal
        ROOT['SYSTEM']['is_journal_open'] = False
    else: 
        ROOT['SYSTEM']['is_journal_open'] = True #open the journal
    
def helpButtonPressFcn(obj):
    #opens the help text as a pseudo-event. Will return you to the original event upon proceeding. NOTE: currently will result in double application of on-event modifiers.
    global current_event
    print('You pressed the help button!')
    current_event = 'help.0'
    
def discoveriesButtonPressFcn(obj):
    print('You clicked the discoveries button.') 
    
def modifierButtonPressFcn(obj):
    print('You clicked the modifier button.')  
        
def playerButtonPressFcn(obj):
    print('You clicked the player button.')  
    
def storageButtonPressFcn(obj):
    print('You clicked the storage button.') 
    
def drawEventTitle(eventTitle): #change to be like options one?
    #Display the title of the event
    boundingRect = (XMARGIN, YMARGIN, XHEADERSIZE, YHEADERSIZE)
    excessText = drawText(DISPLAYSURF, eventTitle, EVENTTITLECOLOUR, boundingRect, FONTBOOK['Event Title'])
    if len(excessText) > 0:
        print('Header text too long: ' + excessText)

    #Draw underline on title
    pygame.draw.line(DISPLAYSURF, BORDERCOLOUR, (XMARGIN, YMARGIN + EVENTTITLESIZE + int(YSPACING/2)), (int(XMARGIN + XINTERFACESIZE/2), YMARGIN + EVENTTITLESIZE + int(YSPACING/2)), int(BORDERWIDTH/2)) 
    
def drawEventText(eventText):
    
    #Display the event descriptive text
    boundingRect = (XMARGIN, YMARGIN + YHEADERSIZE + YSPACING, XDESCRIPTIONSIZE, YDESCRIPTIONSIZE)
    excessText = drawText(DISPLAYSURF, eventText, EVENTTEXTCOLOUR, boundingRect, FONTBOOK['Event Description'])
    if len(excessText) > 0:
        print('Descriptive text too long: ' + excessText) 
        
    #Draw box around text
    borderRect = (boundingRect[0] - 10, boundingRect[1] - 10, boundingRect[2] + 20, boundingRect[3] + 20)
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOUR, borderRect, int(BORDERWIDTH/2))
    
    
def drawTexture(rect, surf, texture, isTiled):
    
    #draws given texture inside a rectangle on given surface
    
    TEXTUREWIDTH = texture.get_width() #size of texture X
    TEXTUREHEIGHT = texture.get_height() #size of texture in Y
    SURFACEWIDTH = rect[2]
    SURFACEHEIGHT = rect[3]
    
    NTILESX = math.ceil(SURFACEWIDTH/TEXTUREWIDTH) #number of tiles needed to fill width
    NTILESY = math.ceil(SURFACEHEIGHT/TEXTUREHEIGHT) #number tiles needed to fill height    
    
    #add texture to interface
    if isTiled:
        #Tile the image/texture in the rectangle given
        for row in range(NTILESY):
            for column in range(NTILESX):
                #crop texture to prevent it over spilling the given rectangle
                x_start = rect[0] + column*TEXTUREWIDTH
                y_start = rect[1] + row*TEXTUREHEIGHT
                
                #x_overhang = min(rect[2] - (x_start + TEXTUREWIDTH), 0)
                #y_overhang = min(rect[3] - (y_start + TEXTUREHEIGHT), 0)
                #if x_overhang < 0 or y_overhang < 0: #exceeds rectangle in horizontal or vertical direction
                    ##crop texture
                    #print(texture.get_clip())
                    #clipping_rect = Rect(x_start, y_start, TEXTUREWIDTH + x_overhang, TEXTUREHEIGHT + y_overhang)
                    #print(clipping_rect)
                    #texture.set_clip(clipping_rect)
                    
                    ##hi
                
                
                surf.blit(texture, (x_start, y_start))
    else: surf.blit(texture, (rect[0], rect[1])) #single image in top left
    

    
def drawJournalInterface():
    
    #Desperately need a WINDOW class to track the active windows and where things are clicking.
    global event_history_actual, ALLEVENTDATA
    
    #Create userinterface for player journal
    #Centre box
    x_start = int(WINDOWWIDTH/2 - JOURNALINTERFACESIZE[0]/2 - BORDERWIDTH)
    y_start = int(WINDOWHEIGHT/2 - JOURNALINTERFACESIZE[1]/2 - BORDERWIDTH)

    interfacePos = [x_start, y_start]


    JOURNALINTERFACEBORDER = pygame.Surface((JOURNALINTERFACESIZE[0] + BORDERWIDTH, JOURNALINTERFACESIZE[1] + BORDERWIDTH), pygame.SRCALPHA) #drawing surface at 50% transparency
    JOURNALINTERFACEBORDER.fill((JOURNALBORDERCOLOUR[0],JOURNALBORDERCOLOUR[1],JOURNALBORDERCOLOUR[2],255)) 

    bgColour = BLACK
    JOURNALINTERFACESURF = pygame.Surface((JOURNALINTERFACESIZE[0], JOURNALINTERFACESIZE[1]), pygame.SRCALPHA) #drawing surface 
    JOURNALINTERFACESURF.fill((bgColour[0],bgColour[1],bgColour[2],255)) #255 = not opaque
    
    DISPLAYSURF.blit(JOURNALINTERFACEBORDER, interfacePos)
    DISPLAYSURF.blit(JOURNALINTERFACESURF, [interfacePos[0] + int(BORDERWIDTH/2), interfacePos[1] + int(BORDERWIDTH/2)])


    textRect = (interfacePos[0]+int(BORDERWIDTH/2), interfacePos[1]+int(BORDERWIDTH/2), JOURNALINTERFACESIZE[0], JOURNALINTERFACESIZE[1])    
    #ADD TEXT
    #journal text is taken from player event history
    #print('Ev list length: ' + str(len(event_history)))
    #print('Days passed length: ' + str(len(ROOT['SYSTEM']['days_passed_tracker'])))
    journal_text = 'EVENT TRACKER'
    for ii in range(0,len(event_history_actual)-1):
        ev_key = event_history_actual[ii+1]
        ev_name = ALLEVENTDATA[ALLEVENTS][ev_key].name.upper()
        ev_text = ALLEVENTDATA[ALLEVENTS][ev_key].text
        day = int(ROOT['SYSTEM']['days_passed_tracker'][ii])
        #print(ev)
        journal_text = '\n'.join([journal_text, 'Day ' + str(day) + ': ' + ev_key + ' (' + ev_name + ')'])
        
        #slightly bugged with random events - will display rand event twice,r ather than the second instance being the original event
        
        
    if len(event_history_actual) > 1:
        journal_text = ''.join([journal_text, '     <<< current event'])
    
    
    
    drawText(DISPLAYSURF, journal_text, WHITE, textRect, FONTBOOK['Journal Body'], aa=True, bkg=None)         
    
    
def createEventOption(optionText, optionNumber, highlightedColour):
    #Display the event descriptive text
    #Prepare bounding box
    boundingRect = (XMARGIN, YMARGIN + YHEADERSIZE + int(1.5 * YSPACING) + (optionNumber) * int(YSPACING/3) + YDESCRIPTIONSIZE + YOPTIONSIZE * (optionNumber - 1), XOPTIONSIZE, YOPTIONSIZE)
    #draw
    #excessText = drawText(DISPLAYSURF, optionText, EVENTOPTIONCOLOUR, boundingRect, FONTBOOK['Event Option'])
    
    opt_button = Button(boundingRect, #size of button
                        BLACK, #background colour
                        optionButtonPressFcn, #function when clicked
                        text = optionText, 
                        font = FONTBOOK['Event Option'],
                        border_color = highlightedColour,
                        hover_color = BLUE, 
                        hover_border_color = highlightedColour,
                        call_on_release = False, 
                        has_popup_box = True, 
                        popup_box_text = '$EVENT OPTION$',
                        popup_box_xScale = 1.2,
                        popup_box_yScale = 0.85, 
                        user_data = optionNumber) #BUTTON CREATION CANNOT BE IN MAIN GAME LOOP.
    #CURRENTLY NO SUPPORT TO DISPLAY LESS THAN MAXOPTIONS options
    
    #if len(excessText) > 0:
     #   print('Option ' + str(optionNumber) + ' text too long: ' + excessText) 
        
    #Draw box around text
    #borderRect = (boundingRect[0] - 10, boundingRect[1] - 5, boundingRect[2] + 20, boundingRect[3] + 10)
    #pygame.draw.rect(DISPLAYSURF, BORDERCOLOUR, borderRect, int(BORDERWIDTH/2))
    return opt_button
   
def optionButtonPressFcn(obj):
    
    '''Function invoked when one of the option buttons is pressed.'''
    global current_event
    #print(obj)
    eventChoice, isValidChoice = EVENTDATA.get_link(optnum)
    #print('Option ' + str(optnum) + '. Link: ' + str(eventChoice))
    
    current_event = eventChoice
    

def drawText(surface, text, color, rect, font, aa=True, bkg=None):
    # draw some text into an area of a surface
    # automatically wraps words
    # returns any text that didn't get blitted 
    # aa = anti aliasing
    # bkg = background
    rect = Rect(rect)
    y = rect.top
    lineSpacing = LINESPACING

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        foundNewline = False
        while font.size(text[:i])[0] < rect.width and i < len(text) and not foundNewline:
            #check for newlines in the text. If found, break loop and start new line
            if text[i-1:i] == '\n':
                foundNewline = True
                #NEW LINES NOT WORKING. IT LOCATES THEM BUT DOES NOT IMPLEMENT THEM.
            i += 1   

             
        if foundNewline:
            # start new line after newline character
            i = text.rfind("\n", 0, i) + 1 
        elif i < len(text):
            # if we've wrapped the text, then adjust the wrap to the last word 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            if text[i-1] == '\n':
                image = font.render(text[:i-1], 1, color, bkg) #omit newline character
            else:
                image = font.render(text[:i], 1, color, bkg)                
            image.set_colorkey(bkg)
        else:
            if text[i-1] == '\n':
                image = font.render(text[:i-1], aa, color) #omit newline character
            else:
                image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text
    

def loadDefines(filename):
    #LOADS GAME DFINES FROM DEFINES FILE
    
    #>ADD LOCALISATION FOR VARIABLES
    #>INCORPORATE NONE TYPE INTO THIS AND CHECKS (SO THINGS NOT NEEDED DO NOT NEED TO BE DEFINED) - see the magic button creation code.
    
    import re
    print('###LOADING DEFINES FROM ' + filename + ':')
    
    ROOT = dict() #ROOT dictionary to hold all categories, variables and defines
    
    with open(filename) as defines_file: #open DEFINES file
        
        defines_files_ALL = defines_file.readlines() #read file
        defines_ALL_split = re.split(r'(PLAYER|SYSTEM|SHIPS)\s*\=\s*\{', ''.join(defines_files_ALL), maxsplit = 0, flags = re.I|re.M) #Split into ROOT: category, content
        #ROOT categories:
        #PLAYER
        #SYSTEM
        #SHIPS
        
        for ii in range(2,len(defines_ALL_split), 2): #Iterate through all found ROOT categories
            
            new_cat = dict() #set up new category
            
            cat_name = defines_ALL_split[ii - 1] #ROOT CATEGORY, e.g. PLAYER or SYSTEM or SHIPS
            cat_contents = defines_ALL_split[ii] #all text within given category
            
            print('Loading category: ' + cat_name + ' <reference: ' + cat_name[0:3].lower() + '>')

            def_C_split = re.split(r'(\w*)\s*\=\s*\{', cat_contents, maxsplit = 0, flags = re.I|re.M) #Split content into: variable, attributes
            for jj in range(2,len(def_C_split),2): #Iterate through and create new variables within the ROOT category space
                var_name = def_C_split[jj-1]
                var_attributes = def_C_split[jj]
                
                new_var = dict() #Set up new variable as dictionary
                
                print('Variable ' + var_name + ' found in category ' + cat_name)
                
                for attribute_line in var_attributes.split('\n'): #iterate through all attributes, line by line
                    if len(attribute_line) > 0:
                        attribute_line_COMMENT_split = attribute_line.split('#') #split out comments
                        attribute_line_NO_COMMENT = attribute_line_COMMENT_split[0] #remove comments
                    
                        attribute_split = re.split(r'\s*\=\s*', attribute_line_NO_COMMENT, re.I|re.M) #Split into attribute and value
                        if len(attribute_split) > 1:
                            att_name = attribute_split[0].strip()
                            att_val = attribute_split[1].strip()
                            
                            #COMPILE & SET UP UNIQUE ATTRIBUTES 
                            if att_name.lower() == 'limit': #limit attribute splits first two items in list and turns them into integers
                                #lim = [min, max]
                                lim_values = att_val.split(',')
                                #FORMAT EQUATIONS: %EQUATION%
                                val_1 = float(lim_values[0])
                                val_2 = float(lim_values[1])
                                del att_val
                                att_val = [min(val_1,val_2), max(val_1,val_2)]
                            
                            new_var.update({att_name:att_val})
                            #print(attribute_line_NO_COMMENT)
                            
                
                #Merge with existing variables and loading into category dictionary
                var_name_sub = '$' + var_name
                #Variable data is stored in the variable name prefixed with a '$'. The actual VALUE of the variable is stored in the variable name.
                #e.g. ship information is stored in "$SHIPNAME", and since there is no value "SHIPNAME" will simply return "0".
                if var_name_sub in new_cat:
                    print('! Variable ' + var_name + ' already found in ' + cat_name + '. Merging variables...')
                    var_data = new_cat[var_name_sub]
                    var_data.update(new_var)
                    new_cat.update({var_name_sub:var_data})
                else:                    
                    new_cat.update({var_name_sub:new_var}) #Load new variable into category under its variable name
                
                #VARIABLE DEFAULTS
                var_data_ALL = new_cat[var_name_sub]
                #Set up variable values as per TYPE and DEFAULT
                if 'default' in var_data_ALL: #get default value from script
                    var_value_default = var_data_ALL['default']
                else: #default variable value is ZERO: if no default is given
                    var_value_default = 0
                    
                if 'type' in var_data_ALL: #get variable type from script
                    var_type = var_data_ALL['type']
                    if re.match(r'(str|wor|tex)', var_type, re.I|re.M): #string/words/text
                        var_value = str(var_value_default)
                    elif re.match(r'(int)', var_type, re.I|re.M): #integer
                        var_value = int(var_value_default)
                    elif re.match(r'(flo|num)', var_type, re.I|re.M): #float/number
                        var_value = float(var_value_default)
                    elif re.match(r'(lis)', var_type, re.I|re.M): #list
                        
                        if var_value_default == '[]': #empty list
                            var_value = list()
                        else:
                            var_value = list(var_value_default)
                            
                    elif re.match(r'(dic)', var_type, re.I|re.M): #dictionary
                        var_value = dict(var_value_default)  
                    elif re.match(r'(boo|fla)', var_type, re.I|re.M): #boolean/flag
                        #CONSIDERS FIRST LETTER/NUMBER OF STRING:
                        #any number > 0 = TRUE
                        #letter 't' = TRUE
                        #words 'yes', 'on' and 'active' = TRUE
                        #emoji ':)' = TRUE
                        #any letter other than 't' = FALSE
                        #number 0 = FALSE
                        #any other words and emojis = FALSE
                        if re.match(r'([1-9]|t|yes|:\)|on|active)', var_value_default, re.I|re.M):
                            var_value = True
                        elif re.match(r'(0|\D)', var_value_default, re.I|re.M):
                            var_value = False
                        else:
                            var_value = None
                    else: #default to string
                        var_value = str(var_value_default)
                else: #Default variabe type is STRING
                    var_value = str(var_value_default)
                #Add variable value to category under variable name
                new_cat.update({var_name:var_value})
            
            #Merge with existing categories and load into ROOT
            if cat_name in ROOT:
                print('! Category ' + cat_name + ' already found. Merging categories...')
                cat_data = ROOT[cat_name]
                cat_data.update(new_cat)
                ROOT.update({cat_name:cat_data})
            else:
                ROOT.update({cat_name:new_cat}) #load category into ROOT variable unders its category name
                
                
        #print(ROOT['SHIPS'])
        
        #Add default game test state if not stated in script
        if not 'is_game_test' in ROOT['SYSTEM']:
            ROOT['SYSTEM']['is_game_test']['value'] = False
            
        
        
        
        print('###FINISHED LOADING DEFINES###')
        
        #ROOT['PLAYER']['name'] = 'Frodo Baggins' #player name
        #ROOT['PLAYER']['role'] = '???' #player role - affects choices and stuff
        
        #ROLES:
        #<INITIAL>
        #Merchant: Good at trade and locating gold. (Better trades, more gold located - playstyle = trade for treasure)
        #Explorer: Experienced at navigation, locating campsites and food and rationing food. (Unique navigation options, less food consumed - playstyle = explore for treasure)
        #Admiral: Good at motivating and hiring crew. Keeps people on task for less randomness. (Lower chance of random events at sea)
        #Peasant: A scavenger good at picking out things often overlooked. Has a knack for spotting shiny things. (find more gold in places. Unique event options - playstyle = day-by-day)
        #<BY EVENT>
        #<RE_general> Head of State: Ultimate commander of all things. (Cannot change allegiance. Much better event rewards)
        #<RE_land> Colonist: Resourceful and effective. Settles the lands and makes it useable. (Lower chance of random events on land).
        #<RE_ocean> Scholar: Study the surrounds and attempt to understand them. (More likely to discover new places and identify new ways of surviving)
        #<RE_general> Missionary: very prestigious. Wants to convert everyone. (Convert people for prestige but may not be popular with the crew).
        
        #ROOT['PLAYER']['days_passed'] = float(0)
        #ROOT['PLAYER']['food_amount'] = float(100) #amount of food player has - If food = 0 GAME OVER
        #ROOT['PLAYER']['treasure_storage'] = float(100) #amount of treasure a player can have - treasure = lots of points
        #ROOT['PLAYER']['treasure_amount'] = float(0) #amount of treasure the player does have - treasure = lots of points
        #ROOT['PLAYER']['crew_amount'] = float(100) #amount of crew members the player has - affects effectiveness of locating resources and number of random events
        #ROOT['PLAYER']['gold_amount'] = float(100) #amount of money the player has - used to trade for resources or keep the crew happy
        #ROOT['PLAYER']['allegiance'] = 'None' #name of country to which a bonus score is applied at game end. Allegiance can affect some events
        
        ##ALLEGIANCES POSSIBLE:
        ##<INITIAL>
        ##country - score bonus
        ##ENGLAND - crew
        ##FRANCE - food
        ##PORTUGAL - discoveries
        ##SPAIN - treasure
        ##NOBODY - NO SCORE BONUS, BUT PASSIVE PRESTIGE PER DAY
        ##<BY EVENT>
        ##NORWAY - length of quest <Greenland Event>
        ##NETHERLANDS - gold <African Event>
        ##CHINA - prestige <Chinese Event>
        ##AZTEC - sacrificing crew <American Event>
        
        #ROOT['PLAYER']['prestige'] = float(0) #measure of how glorious and successful this expedition appears to the outside world. Score is multiplied by 1 + prestige/100. Scales -100 to 100.
        #ROOT['PLAYER']['location'] = 'Europe'
        #ROOT['PLAYER']['discoveries'] = []
        #ROOT['PLAYER']['score'] = float(0)
        #ADD: discovered: to track if a player has discovered certain areas yet


    return ROOT
    
def loadEvents(index_file_name):
    #This function reads the event index file and hence the event category files to load up all of the events
    #It reads the event files to a predetermined scripting language and creates an event object for each event
    #events are then mapped into the dictionary event_list and can be drawn simply by searching their ID number

    import re, traceback
    print('###LOADING EVENTS FROM ' + index_file_name + ':')
    event_list = {} #dictionary of ALL events that link the event ID to the event data
    random_event_conditions = dict() #dictionary of conditions that must be met for each random event namespace
    random_event_sublist = dict() #Dictionary of random event namespace and the events that correspond to them
    try:
        with open(index_file_name, 'r+', encoding="utf-8") as index_file: #open and read index file #ADD A TRY STATEMENT HERE
            #index file is of format NAMESPACE = EVENT TEXT FILE, on seperate lines.
            event_categories_extract = index_file.readlines()
            category_reference = []
            category_baseID = []
            for line in event_categories_extract:
                line_contents = []
                line_contents = line.split()
                category_reference.append(line_contents[0])
                category_baseID.append(line_contents[0].lower())
                
                #extract events
                try:
                    with open(line_contents[2], 'r+', encoding="utf-8") as event_file:
                        #ALL events begin with the opener EVENT = {
                        #attributes are defined as ATTRIBUTE = VALUE
                        #options are listed as attributes under the opener OPTION = {
                        #Any amount of white space on both sides of all equal signs
                        #All text before the command "###BEGIN###" is ignored as an event
                        #Optional before the command ###BEGIN### (in order):
                        #The command ###DEFAULT### can be used to set default properties for all groups in the file <IN PROGRESS>
                        #The command ###CONDITIONS### sets default conditions the must be met for any events in the file to be cobsidered. Currently reserved to random events
                        print('LOADING FILE: ' + line_contents[2] + ' <namespace: ' + line_contents[0] + '>')
                        #try:
                        #    event_file_contents = event_file.read()
                        #except:
                        #    print('Well fuck')
                        event_file_contents = event_file.read()
                        event_data_complete = event_file_contents.split('###BEGIN###') #All text in file before this is ignored.
        
                        #Get defaults, if present
                        event_defaults = event_data_complete[0].split('###DEFAULT###') #Default properties applied to each event
        
                        #get conditions for random events: keyword RE (at start) to signify random event and LINK (at en) to signify it can only be accessed through other events
                        has_RE_namespace = ''.join(re.findall(r'\.{0}RE\W{0}', line_contents[0], re.I|re.M)).lower() == 're' #true if namespace starts with RE
                        has_LINK_namespace = ''.join(re.findall(r'\W{0}link\.{0}', line_contents[0], re.I|re.M)).lower() == 'link' #true if namespace ends with link
        
                        ###CONDITIONS###
                        #IS THIS BRokeN?????
                        is_random_event_namespace = False
                        if has_RE_namespace and not has_LINK_namespace: #conditions only apply to random events, but not random event links
                            is_random_event_namespace = True
                            #print(event_defaults)
                            event_conditions = event_defaults[0].split('###CONDITIONS###') #Conditions required for all events to apply
                            #print(event_conditions)
                            if len(event_conditions) > 1: #there are conditions
                                #store event conditions
                                #print('Random Event Conditions: ' + line_contents[0])
                                #print(event_conditions[-1])
                                condition_tracker = getConditionData(event_conditions[-1])
                                random_event_conditions.setdefault(line_contents[0], condition_tracker)
                                #print(random_event_conditions)
                            else: #there are no conditions - set conditions to NoneType
                                random_event_conditions.setdefault(line_contents[0], type(None))
        
                            
                        ###DEFAULTS###
                        #store defaults
                        category_defaults = dict()
                        
        ##                print(event_defaults[-1])
                        
                        if len(event_defaults) > 1: #successful split, i.e. there is a default category
                            for line in event_defaults[-1].split('\n'):
                                split_defaults = re.split(r'\s*\=\s*', line, re.I|re.M)
                                if len(split_defaults) == 2:
                                    removed_comment = split_defaults[1].split('#')
                                    category_defaults[split_defaults[0]] = removed_comment[0]

        
                        ###GET ALL EVENT DATA###
                                
                        event_data_ALL = re.split(r'EVENT\s*\=\s*\{', event_data_complete[-1], maxsplit = 0, flags = re.I|re.M)
                        
                        
        ##                print('First line: ' + event_data_ALL[0])
                        #Load each event. NOTE: ignore first line, always appears to be blank o.O
                        random_event_list = [] #stores list of events if in random event namespace
                        for event in event_data_ALL[1:]:
                            event_option_split = re.split(r'option\s*\=\s*\{', event,  maxsplit = 0, flags = re.I|re.M)
                            #Get main info. e.g title and description
                            event_data_main_ALL = event_option_split[0]
                            #Get on-event modifiers
                            event_data_main_modifiers = re.split(r'modify\s*\=\s*\{', event_data_main_ALL,  maxsplit = 0, flags = re.I|re.M)
                            
                            #ASSESS DEFAULT/REQUIRED PROPERTIES
       
                            event_data_split = event_data_main_modifiers[0].split('\n')
                            #create default event properties
                            event_properties = dict()
                            event_properties.update(category_defaults) #assign defaults
                            
                            split_data = []
                            ii = 0
                            for line in event_data_split:
                                line_remove_comment = line.split('#')
                                line_split = re.split(r'\s*\=\s*', line_remove_comment[0], re.I|re.M)
                                if line_split[0].strip() != '':
                                    split_data.append(line_split)
                                    ii += 1
                                
                            #set up categories
                            event_stuff = {}
                            for data in split_data:
                                event_stuff[data[0].strip()] = []
                            #append each entry to each category
                            for data in split_data:
                                tmp = event_stuff[data[0].strip()]
                                if len(tmp) < 1:
                                    str_to_add = data[1].strip()
                                else:
                                    str_to_add = '\n' + data[1].strip() #each mention starts on a new line
                                tmp.append(str_to_add)
                                event_stuff[data[0].strip()] = tmp
                            #join together all occurrances of that property
                            for data in split_data:
                                input_item = {data[0].strip(): ''.join(event_stuff[data[0].strip()])}
                                event_properties.update(input_item)
                                if data[0].strip() == 'ID': #record event ID
                                    input_item = {data[0].strip(): category_baseID[-1] + '.' + event_properties[data[0].strip()]}
                                    event_properties.update(input_item)
                                    #update random event list if necessary
                                    
                                    if is_random_event_namespace:
                                        random_event_list.append(event_properties[data[0].strip()])
        ##                    print('Event data:')
                            ##print(event_properties)
                            
                            ###ON-EFFECT MODIFIERS###
                            if len(event_data_main_modifiers) > 1: #modifiers exist
                                on_event_modifiers = event_data_main_modifiers[-1]
                                #print
                                #print('EVENT ID: ' + event_properties['ID'] + ' has on-effect modifiers:')
                                #print(on_event_modifiers)  
                                
                                #Assess modifiers
                                #split out any modifiers caused by the option
                                modifier_split = re.split(r'\w+\s*\=\s*\{', on_event_modifiers.strip(), re.I|re.M)
                                modifier_type_split = re.findall(r'\w+\s*\=\s*\{', on_event_modifiers.strip(), re.I|re.M)
        
                                standard_option_data = modifier_split[0] #required option data, i.e. link and text
                                modifier_option_data = modifier_split[1:] #option data, e.g. modifiers
                                #EXTRACT MODIFER DATA
                                modifier_data, condition_data = extractModiferData(modifier_option_data, modifier_type_split)
                                
                                #print(modifier_data)
                                event_properties.update({'on_effect_modifiers': modifier_data})
                                
                            else: #no on-effect modifiers
                                event_properties.update({'on_effect_modifiers': []})
                                
                                
                            
        
                            ###OPTION INFO###
                            xx = 0
                            option_storage = []
                            for option in event_option_split[1:]:
                                xx += 1
        ##                        print('OPTION ' + str(xx))
                                option_properties = {}
                                #print(option)
                                option_properties['conditions'] = []
                                
        
                                #EXTRACT MODIFIERS
                                #split out any modifiers caused by the option
                                modifier_split = re.split(r'\w+\s*\=\s*\{', option.strip(), re.I|re.M)
                                modifier_type_split = re.findall(r'\w+\s*\=\s*\{', option.strip(), re.I|re.M)
        
                                standard_option_data = modifier_split[0] #required option data, i.e. link and text, PLUS OPTIONALS LIKE HIGHLIGHT
                                modifier_option_data = modifier_split[1:] #option data, e.g. modifiers
                                #EXTRACT MODIFER DATA
                                modifier_data, condition_data = extractModiferData(modifier_option_data, modifier_type_split)
                                
                                option_properties['modifiers'] = modifier_data
                                option_properties['conditions'] = condition_data
                                
        ##                        print(standard_option_data.split('\n'))
                                #REQUIRED data assessment: text and link
                                for line in standard_option_data.split('\n'):
                                    #print(line)
                                    line_remove_comment = line.split('#')
                                    line_split = re.split(r'\s*\=\s*', line_remove_comment[0], re.I|re.M) #split into property and value
                                    if len(line_split) > 1:
                                        if line_split[0].strip() == 'link': #linked event for this option
                                            #Add functionality for ~ operator to do a range of numbers (e.g. 100~105)
                                            
                                            #Read link data
                                            #link = X; This links to X in the current namespace (i.e. category)
                                            #link = namespace.X; This links to X in the given namespaces
                                            #link = namespace.[X,Y,Z]; This links to X, Y and Z in the given namespace
                                            #Currently, X = INTEGER & namespace = STRING
        
                                            #KEYWORDS:
                                            #return - goes back to the most recent non-random/startup event before the current event
                                            #repeat - repeats the current event
                                            #resume - carries on to the originally intended event if the link was interrupted by a random event
                                            
                                            #extract keywords
                                            link_keywords = re.findall(r'return|repeat|resume', line_split[1].strip(), re.I|re.M) #KEYWORDS
                                            link_data_excl_keywords = re.split(r'return|repeat|resume\,?\s*', line_split[1].strip(), re.I|re.M) #REMOVE KEYWORDS
        
                                            
                                            #Extract EXTERNAL multi-links: namespace.[X,Y,Z]
                                            multi_link_ext = re.findall(r'\w*\.\[[\d+\,?]*\]', ''.join(link_data_excl_keywords), re.I|re.M) #multi item links from other categories
                                            #remove from list
                                            link_data_excl_multi = re.split(r'\w*\.\[[\d+\,?]*\]\,?\s*', ''.join(link_data_excl_keywords),  maxsplit = 0, flags = re.I|re.M) #multi item links from other categories
                                            
                                            #Extract EXTERNAL single-links: namespace.X
                                            single_link_ext = re.findall(r'\w+\.\w+', ''.join(link_data_excl_multi), re.I|re.M) #single item links from other categories
                                            #remove from list
                                            link_data_excl_ext = re.split(r'\s*\w+\.\w+\s*\,?\s*', ''.join(link_data_excl_multi), re.I|re.M) #single item links from other categories
                                            
                                            #Extract INTERNAL single-links: X
                                            single_link_int = re.findall(r'\-?\d+', ''.join(link_data_excl_ext), re.I|re.M) #single item links from other categories
        
        ##                                    print('New Option')
        ##                                    print('Links: ' + line_split[1].strip())
        ##                                    print('Multi-links: ' + ','.join(multi_link_ext))
        ##                                    print('Remaining links: ' + ''.join(link_data_excl_multi))
        ##                                    print('Single-links: ' + ','.join(single_link_ext))
        ##                                    print('Remaining links: ' + ''.join(link_data_excl_ext))
        ##                                    print('Internal links: ' + ','.join(single_link_int))
        ##                                    print('\n')
        
                                            #iterate through all cases and add them to the link list for the option, in correct form
                                            option_properties['link'] = []
                                            option_properties['highlight'] = 'black'
                                            #KEYWORDS
                                            for link_str in link_keywords:
                                                option_properties['link'].append(link_str.lower())
                                            #MULTILINKS - EXTERNAL
                                            for link_str in multi_link_ext:
                                                #extract digits inside [...] and apply each of them to the given namespace
                                                split_link = link_str.split('.[')
                                                split_values = split_link[1][:-1].split(',')
                                                for value in split_values:
                                                    option_properties['link'].append(split_link[0].lower() + '.' + value)
        
                                            #SINGLELINKS - EXTERNAL
                                            for link_str in single_link_ext:
                                                option_properties['link'].append(link_str.lower())
        
                                            #SINGLELINKS - INTERNAL
                                            for link_str in single_link_int:
                                                if int(link_str) < 0:
                                                    option_properties['link'].append(str(link_str)) #link < 0 means go backward that many events
                                                else: #is not a return, or go backward event
                                                    option_properties['link'].append(category_baseID[-1].lower() + '.' + link_str)
                                                
                                       
        ##
        ##                                    link_values = line_split[1].split(',') #split any lists into their components
        ##                                    if len(link_values) > 1: #multiple options
        ##                                        option_properties[line_split[0].strip()] = link_values
        ##                                    else:
        ##                                        option_properties[line_split[0].strip()] = category_baseID[-1] + '.' + line_split[1]
                                        elif line_split[0].strip() == 'highlight': #highlight is specified
                                            option_properties['highlight'] = str(line_split[1].strip())     
                                        
                                        else: #string thing
                                            
                                            option_properties[line_split[0].strip()] = str(line_split[1])
                                            
                                #END OPTION ASSESSEMENT
                                #add current option data to the list of all options for this event
                                option_storage.append(option_properties)
                                                               
        
            #                   #Store option data in event data
                                if len(option_storage) > 0:
                                    event_properties['option_data'] = option_storage
                            #END EVENT ASSESSMENT
                            #Store this event data in an event object
                                                       
                            if event_properties != {}:
                                event_list[event_properties['ID']] = new_event(event_properties) #reference the event ID and you get the event!
                                
                            
                    #store random event data for this namespace
                    if is_random_event_namespace:
                        random_event_sublist.update({category_baseID[-1]: random_event_list})
                        
                except FileNotFoundError:
                        print('! Event file ' + line_contents[2] + ' does not exist.')
                        #traceback.print_exc()
    except FileNotFoundError:
        print('! Index file ' + index_file_name + ' does not exist.')
        
    print('###FINISHED LOADING EVENTS###')
                
    return event_list, random_event_conditions, random_event_sublist
    
    
    
def extractModiferData(raw_modifier_data, modifier_type_data):
    import re

    #print('New modifier')
    #Modifier assessment
    modifier_type = [] #constructs a list of the type of modifier that is to be applied. Acceptable choices are: change, add, subtract, multiply, divide
    modifier_target = [] #constructs a list of the target property each modifier is to be applied to, e.g. name, role, food_amount
    modifier_effect = [] #constructs a list of the value that the modifier is to apply, e.g. 1.2 (for numeric operations),'painter' (for a role to change)
    modifier_duration = [] #list of duration for modifiers
    condition_data = []
    #Iterate through modifier types and extract the effects (things they will modify)
    for modifier_index in range(0,len(modifier_type_data)):
        modifier_name_data = modifier_type_data[modifier_index]
        modifier_effect_data = raw_modifier_data[modifier_index]
        #get modifier name.
        modifier_name = re.split(r'\s*\=\s*\{', modifier_name_data.strip(),re.I|re.M)
        
        
        #check & extract any conditions
        if modifier_name[0].lower() == 'conditions':
            condition_data = getConditionData(modifier_effect_data)

        else: #this is a modifier
            #get and split modifier targets and effects
            has_duration = False
            #duration counting goes in here
            item_start = 0
            item_end = 0            
            
            for line in modifier_effect_data.split('\n'):
                
                line_remove_comment = line.split('#')
                if str(line_remove_comment[0].strip()) != '':
                    #print('\nApproved: ' + str(line_remove_comment[0].strip()))
                    #print('#')
                    line_split = re.split(r'\s*\=\s*', line_remove_comment[0].strip(), re.I|re.M) #split into property and value
                    #add modifier details to the list
                    #print('Mod target: ' + line_split[0].strip())
                    if line_split[0].strip().lower() != 'duration':
                        if modifier_name[0] != '' and line_split[0].strip() != '' and line_split[-1].strip() != '':
                            modifier_type.append(modifier_name[0])
                            modifier_target.append(line_split[0].strip())
                            modifier_effect.append(line_split[-1].strip())
                            
                            item_end += 1
                        
                    elif line_split[0].strip().lower() == 'duration':  #apply duration
                        has_duration = True
                        duration_line = line_split
          
            #add duration to each entry in modifier type. Duration of -1 means permanent
            
            for counter in range(item_start, item_end):
                if has_duration:
                    modifier_duration.append(int(duration_line[-1].strip()))                        
                else:
                    modifier_duration.append(-1)  #no duration - i.e. permanent modifier                
                
            item_start = item_end + 1            
            
                       
    #Check if a modifier was present   
    if len(modifier_type) > 0:
        #print('Results:')
        #print(modifier_duration)
        modifier_data = [modifier_type, modifier_target, modifier_effect, modifier_duration] #SEEMS TO BE STORING AS ANA RRAY IN AN ARRAY - NEED TO FIX
        #print(modifier_data)
    else:
        modifier_data = [[],[],[],[]]
        
        
    #print(modifier_data)

    return modifier_data, condition_data


def getConditionData(modifier_effect_data):
    import re

    condition_data = []
    for line in modifier_effect_data.split('\n'):
        line_remove_comment = line.split('#')
        line_split = re.split(r'\s*\=\s*', line_remove_comment[0], re.I|re.M) #split into property and value
        if len(line_split) > 1:
            #split value by the commas!
            stripped_vals = line_split[1].strip()
            split_vals = re.split(r'\s*\,\s*', stripped_vals, re.I|re.M)
            condition_data.append([line_split[0].strip(),split_vals])
            #if len(split_vals) > 1:
                #print('EVENT ID: ' + event_properties['ID'] + '; Option Number: ' + str(xx))
                #print(split_vals)

    #print(condition_data)
    return condition_data

def format_text(text_string):
#Formats an input string from script as per any special operators entered into the text
#$NAME$ - $ symbols mean the path specified between should be accessed from the root PLAYER and the text inputted in its stead. e.g. $NAME$ will access the player name.
#ADD SUPPORT FOR APOSTROPHE'S. Add range of numbers using ~ e.g. 100~110, for use in random number/event links
    import re
    PLAYER = ROOT['PLAYER']
##    print(text_string)
    
    user_links = re.findall(r'\$(\w+)\$', text_string) #extracts all text that needs to be replaced with a user's value. e.g. name
    string_split = re.split(r'\$(\w+)\$', text_string) #splits by the location needed

    ii = 1 #indexing to find locations to be replaced
    for user_category in user_links:
        try:
            text_val_temp = PLAYER[str(user_category).lower()]
            if type(text_val_temp).__name__ == 'str':
                text_value = str(text_val_temp).capitalize()
            elif type(text_val_temp).__name__ == 'int' or type(text_val_temp).__name__ == 'float':
                text_value = str(int(text_val_temp)).capitalize()
                
            string_split[ii] = text_value
        except KeyError:
            print('!!!ERROR: PLAYER define $' + str(user_category) + '$ unknown.')
        finally:
            ii += 2

    output_string = ''.join(string_split)

    return output_string


def evaluate_random_events(event_list, random_event_conditions, random_event_sublist):
    #THIS FUNCTION DOES THE FOLLOWING:
    #-Accesses all random event namepsaces
    #-Checks any conditions set on those namepsaces
    #-extracts the namepsaces for which the conditions are met
    #-selects an event at random from all complying namespaces - ###Need to add weightings to random events
    
    #Random Event namespaces that are eligible to be considered must begin with "RE" and not end with "link".
    
    #PROPOSED CHANGE: define random_event = yes tag in script. RE namespace will automatically add it, but can toherwise be manually defined. All events will then have a random_event = yes/no flag for easy access and checking.
    
    
    from random import uniform
    all_event_links = event_list.keys()
    #select random event from event namespaces that begin with "RE" but not those that end in "link" AND meet event conditions
    
    #print(random_event_conditions)
    RE_namespaces_ALL = random_event_conditions.keys()
    #check conditions
    RE_allowable = [] #List of random event namespaces that currently meet conditions
    for RE_namespace in RE_namespaces_ALL:
        required_conditions = random_event_conditions[RE_namespace]
        #print(required_conditions)
        all_conditions_met = True
        #conditions are stored in a dictionary.
        if type(required_conditions).__name__.lower() == 'list':
            #check all the conditions - ALL must be met
            all_conditions_met = evaluate_conditions(required_conditions)
        else:
            all_conditions_met = False

        if all_conditions_met:
            RE_allowable.append(RE_namespace)
            is_test_game = False
            if is_test_game:
                print(RE_namespace + ' meets the conditions')
    all_acceptable_events = []
    #Get list of random event ID's in each of the acceptable namespaces
    for accepted_namespace in RE_allowable:
##                            print(accepted_namespace + ' events:')
##                            print(random_event_sublist[accepted_namespace.lower()])
        relevant_events = random_event_sublist[accepted_namespace.lower()]
        for event in relevant_events:
            all_acceptable_events.append(event)
            
    #select event at random for the acceptable ones
    if all_acceptable_events != []:
        rand_roll = int(uniform(0,len(all_acceptable_events) - 1))
    ##  print('Chosen event: ' + all_acceptable_events[rand_roll])
        linked_event = all_acceptable_events[rand_roll]
        is_in_random_event = True
    else:
        is_in_random_event = False
        linked_event = None
        print('No random events meet the current conditions.')
    
    return linked_event, is_in_random_event


def evaluate_conditions(required_conditions):
    
    ###EVALUATE CONDITIONS###
    #Takes the input list of conditions and evaluates whether the conditions are met or not.
    
    
    #CONDITIONS are defined in the script by:
    #conditions = {
    
    
    #By default, all listed conditions must be met, i.e. the condition statement is also an AND statement.
    #For example:
    #conditions = {
    #    name = harry
    #    role = wizard
    #
    #This requires the name to be 'harry' AND the role to be 'wizard'.
    
    
    #NOT operator: ~
    #Inverses result. 
    #For example
    #conditions = {
    #    ~name = draco malfoy
    #
    #This requires the name to NOT be 'draco malfoy'.
    
    
    #If multiple choices are listed for one condition it is treated as an OR
    #For example:
    #conditions = {
    #    name = harry, ron
    #    role = wizard
    #
    #This requires the name to be 'harry' OR 'ron', AND their role must be 'wizard'.
    
    
    #To override the default AND function of the condition statement, one entry can be linked with an OR to the entry above it. as follows:
    #OR operator: | (not yet added)
    #For example:
    #conditions = {
    #    name = harry
    #    |role = wizard
    #
    #This requires the name to be 'harry' OR their role must be 'wizard'.
    
    
    #DETAILED EXAMPLE:
    #conditions = {
    #    name = harry, ron, hermione
    #    role = wizard
    #    |parents = wizards
    #
    #This requires the name to be 'harry', 'ron' OR 'hermione', AND their role must be 'wizard' OR their parents must be 'wizards'
    #AKA:
    #all(
    #    name = harry OR ron OR hermione
    #    any(
    #        role = wizard
    #        parents = wizards
    #        )
    #    )
    
    
    #The OR operator takes precedence over the TILDA: i.e.
    #conditions = {
    #    name = harry
    #    |~age = 12
    #
    #This requires the name to be 'harry' OR the age to be NOT greater than 12.
    
    
    global ROOT
    
    #CONDITIONS DEFAULT TRUE IF THERE ARE NONE
    PLAYER = ROOT['PLAYER']
    condition_tracker = []
    is_conditions_met = False    
    for condition in required_conditions:
        specific_condition_tracker = []
        c_tar = condition[0] #Target property to be checked - string: PLAYER[string]
        c_val_ALL = condition[1] #allowable values, inferred OR statement - list: [a,b,c]
        #PLAYER[string] = a OR b OR c
        
        for c_val in c_val_ALL:
            
            if c_tar[0] == '~': #LESS THAN (floats) | NOT EQUAL TO (strings)
                #tilda operator means at the start of a variable name means NOT
                #i.e. ~food_amount = 50 means food must be less than 50, as opposed to greater than.
                if type(PLAYER[c_tar[1:]]).__name__ == 'float': #numbers are a comparitve assesment
                    if float(PLAYER[c_tar[1:]]) < float(c_val):
##                        print('Condition met (number)')
                        specific_condition_tracker.append(True)
                    else:
                        specific_condition_tracker.append(False)
##                            print('Condition not met')
                          
                elif PLAYER[c_tar[1:]].lower() != c_val: #strings are direct
                    specific_condition_tracker.append(True)
##                    print('Condition met (string)')
                else:
                    specific_condition_tracker.append(False)
##                            print('Condition not met')

            else: #no tilda operator: GREATER THAN OR EQUAL TO (floats) | EQUIVALENT (strings)

                if type(PLAYER[c_tar]).__name__ == 'float':
                    if not(float(PLAYER[c_tar]) < float(c_val)):
##                        print('Condition met (number)')
                        specific_condition_tracker.append(True)
                    else:
                        specific_condition_tracker.append(False)
                        ##print('Condition not met')
                          
                elif not(PLAYER[c_tar].lower() != c_val):
                    specific_condition_tracker.append(True)
##                    print('Condition met (string)')
                else:
                    specific_condition_tracker.append(False)
                    ##print('Condition not met')

        condition_tracker.append(any(specific_condition_tracker)) #Any of the required results can be met for the entire line to be TRUE (ANY TRUE)
            
    #Check if all conditions were met (ALL TRUE)   
    if all(condition_tracker) or len(required_conditions) < 1:
        is_conditions_met = True
        
    return is_conditions_met


def apply_event_modifiers(event_modifier_data):
    #reads the event modifiers and applies them
    global ROOT
    #print('MODIFYING\n' + str(event_modifier_data))
    
    #~ infront of variable name means NOT
    #INT%var_name means that the applied effect is calculated as INT% of the variable name. e.g. 10%crew_amount is the same as 0.1 * crew_amount - TO BE ADDED
    #Modifiers can be permanent (no duration specified in script) or temporary (number of days specified in script with duration = XXX) - TO BE ADDED
    
    
    #seperate out modifier data
    modifier_type = event_modifier_data[0]
    modifier_target = event_modifier_data[1]
    modifier_value = event_modifier_data[2]
    modifier_duration = event_modifier_data[3]
    modifier_effect = []
    #for each modifier, apply effects
    for modifier_index in range(0,len(modifier_type)):
        m_type = modifier_type[modifier_index].lower()
        m_tar = modifier_target[modifier_index]
        m_val = modifier_value[modifier_index]
        m_dur = modifier_duration[modifier_index]

        if not(m_type == '' or m_val == '' or m_type == ''): #ignore anything that draws a blank in any of the required fields
            
            #apply!
            if m_type == 'change':
                #MODIFIER TYPE: CHANGE
                #print('Changing ' + m_tar + ' to ' + str(m_val) + '.')
                #change the value of the target to the given value.
                modifier_effect.append(ROOT['PLAYER'][m_tar]) #value before it gets changed
                if type(ROOT['PLAYER'][m_tar]).__name__ == ('int' or 'float'):
                    ROOT['PLAYER'][m_tar] = float(m_val)
                else:
                    ROOT['PLAYER'][m_tar] = str(m_val)
                    

            elif m_type == 'add':
                #MODIFIER TYPE: ADD
                #adds the given value to the value of the target.
                if type(ROOT['PLAYER'][m_tar]).__name__ == 'float':
                    try:
                        ROOT['PLAYER'][m_tar] += float(m_val)
                        modifier_effect.append(float(m_val))
                    except ValueError:
                        print('Invalid Addition. You are trying to add a non-number to a number')
                        modifier_effect.append(0)
                elif type(ROOT['PLAYER'][m_tar]).__name__ == 'list':
                    ROOT['PLAYER'][m_tar].append(m_val) #add to list - add check if item already exists
                    modifier_effect.append(m_val)

                else:
                    ROOT['PLAYER'][m_tar] += str(m_val)
                    modifier_effect.append(str(m_val))
                    
            elif m_type == 'subtract':
                #MODIFIER TYPE: SUBTRACT
                #removes the given value from the value of the target. NUMBERS ONLY
                if (type(ROOT['PLAYER'][m_tar]).__name__ == 'int' or 'float') and (type(m_val).__name__ == 'int' or 'float'):
                    if m_tar != 'prestige': #prestiage variable can go negative
                        ROOT['PLAYER'][m_tar] = max(ROOT['PLAYER'][m_tar] - float(m_val), 0)
                    else:
                        ROOT['PLAYER'][m_tar] -= float(m_val)
                        
                    modifier_effect.append(float(m_val))
                    
                else:
                    print('Invalid Subtraction. You are trying to subtract using non-numbers')
                    modifier_effect.append(0)

            elif m_type == 'multiply':
                #MODIFIER TYPE: MULTIPLY
                #multiplies the given value with the value of the target. NUMBERS ONLY
                if (type(ROOT['PLAYER'][m_tar]).__name__ == 'int' or 'float') and (type(m_val).__name__ == 'int' or 'float'):
                    ROOT['PLAYER'][m_tar] = float(ROOT['PLAYER'][m_tar])
                    initial_value = ROOT['PLAYER'][m_tar]
                    ROOT['PLAYER'][m_tar] *= float(m_val) 
                    modifier_effect.append(ROOT['PLAYER'][m_tar] - initial_value)
                else:
                    print('Invalid Multiplication. You are trying to multiply using non-numbers')
                    modifier_effect.append(0)

            elif m_type == 'divide':
                #MODIFIER TYPE: DIVIDE
                #divides the value of the target by the given value. NUMBERS ONLY. Note this turns ints into floats
                if (type(ROOT['PLAYER'][m_tar]).__name__ == 'int' or 'float') and (type(m_val).__name__ == 'int' or 'float'):
                    initial_value = ROOT['PLAYER'][m_tar]
                    ROOT['PLAYER'][m_tar] /= float(m_val)
                    modifier_effect.append(ROOT['PLAYER'][m_tar] - initial_value)
                else:
                    print('Invalid Division. You are trying to divide using non-numbers')
                    modifier_effect.append(0)
                    
        #save modifier if it is a temporary one
        
        if m_tar and m_dur > 0:
            #print('temp modifier detected - ' + m_type + ' ' + m_tar + ': ' + str(m_val) + ' for ' + str(m_dur) + ' days')    
            mod_data = [m_type, m_tar, m_val, m_dur, modifier_effect]
            ROOT['PLAYER']['active_modifiers'].append(mod_data)

##ADD MODIFIER: RANDOM - for random application of things
                    
    ###END APPLICATION OF MODIFIERS###

def printModifierData(modifier_data):
    #Prints the effects of the input modifiers to the log
    modifierString = 'This will have the following effects:'
    for mod_num in range(0, len(modifier_data[0])): #duration is the last item
        
        if modifier_data[1][mod_num] != '':
            #format text for popup box when hovering over options
            modifierString = ''.join([modifierString, '\n   > ('])
            #if modifier_data[3][mod_num] < 0:
            #    modifierString = ''.join([modifierString, 'permanently ']) 
            if modifier_data[0][mod_num] == ('multiply' or 'divide'):
                modifierString = ''.join([modifierString, modifier_data[0][mod_num] + ' ' + modifier_data[1][mod_num] + ' by ' + modifier_data[2][mod_num]])
            elif modifier_data[0][mod_num] == 'add':
                modifierString = ''.join([modifierString, modifier_data[0][mod_num] + ' ' + modifier_data[2][mod_num] + ' to ' + modifier_data[1][mod_num]])
            elif modifier_data[0][mod_num] == 'subtract':
                modifierString = ''.join([modifierString, modifier_data[0][mod_num] + ' ' + modifier_data[2][mod_num] + ' from ' + modifier_data[1][mod_num]])                            
            else:
                modifierString = ''.join([modifierString, modifier_data[0][mod_num] + ' ' + modifier_data[1][mod_num] + ' to ' + modifier_data[2][mod_num].capitalize()])
            
            if modifier_data[3][mod_num] >= 0:
                modifierString = ''.join([modifierString, ' for ' + str(modifier_data[3][mod_num]) + ' days']) 
                
                
            modifierString = ''.join([modifierString, ')'])
                
    
        
    if modifierString == 'This will have the following effects:':
        modifierString = ''.join([modifierString, '\n   > None.'])

    return modifierString

class new_event:
    
    def __init__(self, event_data):
        self.name = event_data.get('title')
        self.ID = event_data.get('ID')
        self.text = event_data.get('text')
        self.location = event_data.get('location')
        self.on_effect_modifiers = event_data.get('on_effect_modifiers')
        self.option_text = []
        self.option_link = []
        self.option_modifiers = []
        self.option_conditions = []
        self.option_highlight = ['black']
        self.isEventActive = False #track whether this event is being actively displayed on the screen - avoids spam to the log
        self.isFreshEvent = True #Flag. Is this event being freshly displayed (regardless of it has been previously displayed)
        self.isRandomEvent = event_data.get('random_event') #Flag. Is this event a random event - can it be included in the list of potential random events? By default all events in the RE namespace are included, unless specifically excluded.
        self.isLinkedOnly = event_data.get('linked_only') #Flag. Is this event one that can only be reached through a link from another event. This will exclude random events from the considered random event pool when rolling for an event.
        self.isStartupEvent = event_data.get('startup_event') #Flag. Is this event a startup event - is it only possible to be loaded during the startup phase? By default all events in the startup namespace are included, unless specifically excluded.
        self.isHelpEvent = event_data.get('help_event')
        option_data = event_data.get('option_data')
        self.optionTooltip = []
        self.image = event_data.get('image')
        #print(option_data)
        ii = 0
        for option in option_data:
            self.option_text.append(option.get('text'))
            self.option_link.append(option.get('link'))
            self.option_modifiers.append(option.get('modifiers'))
            self.option_conditions.append(option.get('conditions'))
            modifierString = printModifierData(self.option_modifiers[ii]) #move into tooltip
            self.optionTooltip.append(modifierString)
            highlightColour = option.get('highlight')
            self.option_highlight.append(highlightColour)  
            ii += 1
            
    
            
        #ADD DEFAULT OPTION AT END FOR WHEN NO OTHERS ARE AVAILABLE
        self.option_text.append('I think I forgot what I was doing...')
        self.option_link.append('return')   
        self.option_highlight.append('black')
        self.option_modifiers.append([[],[],[]])
        self.option_conditions.append([])
        

    def display_event(self):
        #DISPLAY THE GIVEN EVENT
        #This will print the event info to the console.
        #It will set up the option selection, checking the conditions on each option and deciding whether to make them selectable or not
        #options that do not pass the condition check are not able to be chosen and are hidden.
        
        global ROOT
        
        ###PRINT EVENT TITLE AND TEXT###
        #Update title
        eventTitle = 'Missing Event Title...'
        eventTitle = format_text(self.name.upper()).upper()
        drawEventTitle(eventTitle)
        #Update description
        eventDescription = 'Missing Event Description...'
        eventDescription = format_text(self.text)
        drawEventText(eventDescription)
        
        #print('<'+format_text(self.name.upper()).upper()+'>') #Event title

        #print(format_text(self.text)) #flavour text
        
        ###EVENT PICTURE###
        y_pos = YMARGIN + YHEADERSIZE + int(1.75 * YSPACING) + YDESCRIPTIONSIZE
        x_pos = int(3*XINTERFACESIZE/4)-EVENTPICTURESIZE[0]/2 + XMARGIN + int(0.5 * XSPACING) 
        try: #display event picture (if given)
            DISPLAYSURF.blit(pygame.image.load('gfx/events/'+self.image), (x_pos,y_pos))
        except:
            #Default
            DISPLAYSURF.blit(EVENTPICTUREDEFAULT, (x_pos,y_pos))
            
                
        

        ###EVENT LOCATION###
        #Update location, if necessary
        if type(self.location).__name__ != 'NoneType' and not self.isEventActive: #if nonetype do not change anything. i.e keep previous
            ROOT['PLAYER']['location'] = self.location
            if ROOT['SYSTEM']['is_game_test']:
                print('Location changed to ' + self.location)
        
        ##ON-EFFECT MODIFIERS
        if len(self.on_effect_modifiers) > 0 and not self.isEventActive:
            apply_event_modifiers(self.on_effect_modifiers) #apply modifiers
            #printModifierData(self.on_effect_modifiers) #print to log
        print
        
        ###OPTION ASSESSMENT AND DISPLAY###
        option_number = 0
        visible_option_number = 1 
        
        self.visible_options = []
        for option_text in self.option_text[0:-1]:
            #check option conditions: ALL LISTED CONDITIONS MUST BE MET FOR CONDITION TO PROCEED
            
            required_conditions = self.option_conditions[option_number]
            
            is_option_conditions_met = evaluate_conditions(required_conditions)            
            
            
                
            ##DISPLAY EVENT OPTION IF CONDITIONS MET
            if is_option_conditions_met:
                eventOptionsText = 'Missing Option Text...'
                eventOptionsText = '(' + str(visible_option_number) + ') ' + format_text(option_text)
                #print('(' + str(visible_option_number) + ') ' + format_text(option_text)) #list of options
                
                #change highlight to be rgb input?
                highlightColour_str = self.option_highlight[visible_option_number].lower()
                #print(highlightColour_str)
                if highlightColour_str == 'black':
                    highlightColour = BLACK
                elif highlightColour_str == 'red':
                    highlightColour = RED
                elif highlightColour_str == 'green':
                    highlightColour = GREEN
                elif highlightColour_str == 'dark green':
                    highlightColour = DARKGREEN
                elif highlightColour_str == 'yellow':
                    highlightColour = YELLOW
                elif highlightColour_str == 'blue':
                    highlightColour = BLUE
                elif highlightColour_str == 'light grey':
                    highlightColour = LIGHTGREY
                elif highlightColour_str == 'dark grey':
                    highlightColour = DARKGREY
                elif highlightColour_str == 'white':
                    highlightColour = WHITE
                elif highlightColour_str == 'purple':
                    highlightColour = PURPLE
                else: highlightColour = BLACK
                
                
                OPTIONHANDLES[visible_option_number-1] = createEventOption(eventOptionsText, visible_option_number, highlightColour) 
                
                #Format and display modifier data
                
                
                
                self.visible_options.append(option_number)
                visible_option_number += 1
                
            option_number += 1
            
        #CHECK: IF NO OPTIONS AVAILABLE SET TO DEFAULT: link = return
        if len(self.visible_options) < 1: #there are no options that can be accessed: print default option (end one)
            option_text = self.option_text[option_number]
            eventOptionsText = 'Missing Option Text...'
            eventOptionsText = '(' + str(visible_option_number) + ') ' + format_text(option_text)
            OPTIONHANDLES[visible_option_number-1] = createEventOption(eventOptionsText, visible_option_number, self.option_highlight[visible_option_number]) 
            #drawEventOption(eventOptionsText, visible_option_number)   
            #print('(' + str(visible_option_number) + ') ' + format_text(option_text)) #list of options
            self.visible_options.append(option_number)
        if not self.isEventActive:
            print
            
        self.isEventActive = True
    def get_link(self, selected_option):
        #Get event ID from input INT detailing which number option was chosen.
        #For events with multiple options, one will be chosen at random (equal weighting)
        from random import uniform
        global event_history, event_choices_excl_randoms, ALLEVENTDATA, event_history_actual

        #DEFINITIONS:
        #selected_option = the user inputted digit (>0)
        #chosen_option = the corresponding option index in that event
        has_chosen_valid_option = False
        if ROOT['SYSTEM']['is_game_test']:
            print('You chose option ' + str(selected_option) + '.') #for testing purposes
        
        if selected_option > len(self.visible_options): #Chosen option number is larger than the number of options available
            print('Unacceptable choice! Try again please.')
            selected_event_final = self.ID #if you chose an unacceptable option
        else: #user input an acceptable option
            has_chosen_valid_option = True
            chosen_option = self.visible_options[selected_option - 1]
            available_events = self.option_link[chosen_option]

##            print('Possible links: ' + ','.join(available_events))
            
            rand_roll = int(uniform(1,len(available_events)))
            selected_event = available_events[rand_roll - 1]
            #event ID = namespace.X
            #check for reversing
            event_X = selected_event.split('.')
##            print(event_X)
            if event_X[-1].lower() == 'return': #return to the previous non-random event
                selected_event_final = event_choices_excl_randoms[-2]
            elif event_X[-1].lower() == 'repeat': #repeat the current event
                selected_event_final = event_history[-1]
            elif event_X[-1].lower() == 'resume': #continue to the originally intended event
                selected_event_final = event_choices_excl_randoms[-1]
            elif int(event_X[-1]) < 0: #go backwards a number of events
                selected_event_final = event_history[max(int(event_X[-1]), -len(event_history))]
            else:
                selected_event_final = selected_event

            if ROOT['SYSTEM']['is_game_test']:
                print('This corresponds to event: <' + str(selected_event_final) + '>.') #for testing purposes
                
            apply_event_modifiers(self.option_modifiers[chosen_option])
        
        
        #store selected event in list
        if not ALLEVENTDATA[ALLEVENTS][selected_event_final].isHelpEvent:
            event_history.append(selected_event_final)
            if not ALLEVENTDATA[ALLEVENTS][selected_event_final].isRandomEvent:
                event_choices_excl_randoms.append(selected_event_final)        
        
        #random event check is in daily calculations
        
        
        self.isEventActive = False
        self.isFreshEvent = True
        
        return selected_event_final, has_chosen_valid_option
    
    
    
class Button(object):
    """A fairly straight forward button class."""
    def __init__(self,rect,color,function,**kwargs):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.function = function
        self.clicked = False
        self.hovered = False
        self.hover_text = None
        self.clicked_text = None
        self.process_kwargs(kwargs)
        self.render_text()

    def process_kwargs(self,kwargs):
        """Various optional customization you can change by passing kwargs."""
        settings = {"text" : None,
                    "font" : pygame.font.Font(None,16),
                    "call_on_release" : True,
                    "hover_color" : None,
                    "clicked_color" : None,
                    "font_color" : pygame.Color("white"),
                    "hover_font_color" : None,
                    "clicked_font_color" : None,
                    "click_sound" : None,
                    "hover_sound" : None,
                    "clicked" : False,
                    "border_color" : pygame.Color("black"),
                    "hover_border_color" : pygame.Color("black"),
                    "border_width" : 4,
                    "hover_border_width" : 4,
                    "user_data" : None,
                    "has_popup_box" : False,
                    "popup_box_text" : 'You are hovering over the button',
                    "popup_box_location" : 'bottom right', #location of popupbox relative to cursor
                    "popup_box_xScale" : 1.0, #scaling factor applied to width of popup box
                    "popup_box_yScale" : 1.0, #scaling factor applied to height of popup box
                    "texture" : None,
                    "hover_texture" : None}
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("Button has no keyword: {}".format(kwarg))
        self.__dict__.update(settings)
        if self.call_on_release:
            self.clicked = True
        else:
            self.clicked = False
            
        return self.hovered

    def render_text(self):
        """Pre render the button text."""
        if self.text:
            if self.hover_font_color:
                color = self.hover_font_color
                self.hover_text = self.font.render(self.text,True,color)
            if self.clicked_font_color:
                color = self.clicked_font_color
                self.clicked_text = self.font.render(self.text,True,color)
            self.text = self.font.render(self.text,True,self.font_color)

    def check_event(self,event):
        """The button needs to be passed events from your program event loop."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)

    def on_click(self,event):
        if self.rect.collidepoint(event.pos): 
            self.clicked = True
            if not self.call_on_release:
                self.function(self)   

    def on_release(self,event):
        if self.clicked and self.call_on_release and self.rect.collidepoint(event.pos): 
            self.function(self)
        self.clicked = False

    def check_hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):

            #POPUP BOXES SHOULD REALLY BE A SEPERATE OBJECT
            if self.has_popup_box: #need to specifically identify event buttons when hovered over
                #tooltip popup
                if self.popup_box_text == '$EVENT OPTION$': #keyword to tell engine to get the event option modifier data and display it
                    popupText = EVENTDATA.optionTooltip[EVENTDATA.visible_options[self.user_data-1]]
                else: popupText = self.popup_box_text
                #change button and option creation to have userdata/tooltip string entered, then use the data to display the tooltip
                mousePos = pygame.mouse.get_pos()
                #compute popupbox location starting coordinates
                #commands are:
                #TOP (+Y)
                #CENTRE
                #BOTTOM (-Y)
                #LEFT (-X)
                #MIDDLE
                #RIGHT (+X)
                location_string = self.popup_box_location
                if type(location_string).__name__ != 'str':
                    print('The entered popup box location identifier (' + location_string + ') is not a string, defaulting popupbox to bottom left corner.')
                    location_string = 'bottom right'
 
                location_array = location_string.split(' ')
                
                pBox_h = self.popup_box_yScale * POPUPBOXHEIGHT
                pBox_w = self.popup_box_xScale * POPUPBOXWIDTH
                #print(location_array)
                #split input string and read given locations
                boxPos = [mousePos[0], mousePos[1]]
                for loc_cmd in location_array:
                    if loc_cmd.lower() == 'top':
                        boxPos[1] -= (3*YPOPUPOFFSET + pBox_h)
                    elif loc_cmd.lower() == 'centre':
                        boxPos[1] -= int(pBox_h/2 + YPOPUPOFFSET)
                    elif loc_cmd.lower() == 'bottom':
                        boxPos[1] += YPOPUPOFFSET
                    elif loc_cmd.lower() == 'left':
                        boxPos[0] -= (3*XPOPUPOFFSET + pBox_w)
                    elif loc_cmd.lower() == 'middle':
                        boxPos[0] -= int(pBox_w/2 + XPOPUPOFFSET)
                    elif loc_cmd.lower() == 'right':
                        boxPos[0] += XPOPUPOFFSET
 
                textRect = (boxPos[0] + XPOPUPOFFSET, boxPos[1] + YPOPUPOFFSET, pBox_w - 2*XPOPUPOFFSET, pBox_w - 2*YPOPUPOFFSET)
                #CREATE POPUP BOX
                POPUPBOX = pygame.Surface((pBox_w+ 2*XPOPUPOFFSET, pBox_h+2*YPOPUPOFFSET), pygame.SRCALPHA) #drawing surface at 50% transparency
                bgColour = BLACK
                
                POPUPBOX.fill((bgColour[0],bgColour[1],bgColour[2],128))
                DISPLAYSURF.blit(POPUPBOX, boxPos)
                #ADD TEXT
                drawText(DISPLAYSURF, popupText, WHITE, textRect, FONTBOOK['Popup Box Small'], aa=True, bkg=None)
            
            if not self.hovered:
                self.hovered = True
                if self.hover_sound:
                    self.hover_sound.play()
        else:
            self.hovered = False

    def update(self,surface):
        """Update needs to be called every frame in the main loop."""
        color = self.color
        text = self.text
        texture = self.texture
        border_color = self.border_color
        border_width = self.border_width
        self.check_hover()
        if self.clicked and self.clicked_color:
            color = self.clicked_color
            if self.clicked_font_color:
                text = self.clicked_text
        elif self.hovered and self.hover_color:
            color = self.hover_color
            border_color = self.hover_border_color
            border_width = self.hover_border_width
            texture = self.hover_texture
            if self.hover_font_color:
                text = self.hover_text
                
        #create border
        surface.fill(border_color,self.rect)
        surface.fill(color,self.rect.inflate(-border_width,-border_width))
        
        if texture:
            #print('This button has a texture')
            
            drawTexture(self.rect.inflate(-border_width,-border_width), surface, texture, True)
        
        if self.text:
            text_rect = text.get_rect(center=self.rect.center)
            text_rect[0] = self.rect[0] + 5 #align left
            surface.blit(text,text_rect) 
            
        self.check_hover() #bring popup boxes to the front
            
    def change_text(self, text):
        self.text = text
        self.render_text()

if __name__ == '__main__':
    main()    