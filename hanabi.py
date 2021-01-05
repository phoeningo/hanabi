import numpy as np
import random
import os 
import copy

#==========Static Data===============
Color=['Red','Yellow','White','Green','Blue']
Number=[1,1,1,2,2,3,3,4,4,5]
type_dict={'1':'Color','2':'Number'}


#===========DATA========
#Total_num=50

All=[]            # all cards , type : list
#ct_point=1       #   
Players={}        # all players , type : dict ,
                  # each player seems like: {'Kongfang':{'cards':['Red 2','Yellow 1','Blue 5','Blue 2'] , 'marks': ['','','Blue','']} }
Trash=[]          # discarded cards are stored here. type : list
Board={'Red':'','Yellow':'','White':'','Green':'','Blue':''}
                  # current board , type : dict

#  Tokens
tip_point=8 
bomb_point=3


# the final player name
end_name=''
pre_end=0
end_point=0
#




#===========FUNCTIONS========================
def shuffle(ls,iters):
  for si in range (iters ):
    random.shuffle(ls)


def create_player(alias):
  tmp_player={alias:{'cards':[],'marks':[]}}
  return tmp_player


# 'top' card(s) from [All] cards.
def top(ls,alias,num):
  if len(ls) < num:
    print('Not so many cards.')
    return 0
  else:
    for each_i in range(num):
      Players[alias]['cards'].append(ls[each_i])
      Players[alias]['marks'].append('')
    del (ls[:num])
    return 1
  

def add_player(ap,single_player):
  tmp=dict(ap,**single_player)
  return tmp

def show_player(Players):
  print('---Players---')
  for each_player in Players:
    print (each_player+' : ')
    print(Players[each_player])

def show_board():
  print('===Board===')
  for item in Color:
    print(item+' : '+Board[item])
def show_trash():
  print("***Trash***")
  print(Trash)

def add2board(card):
  global tip_point
  global bomb_point
  color=card.split(' ')[0]
  num=card.split(' ')[1]
  print(num)
  ls=Board[color]
  print (ls)
  total=len(ls.split(' '))
  print(total)
  if int(num)==total:
    print('Add :'+num+' to Color '+color)
    Board[color]=Board[color]+' '+num
    if num=='5':
      tip_point+=1
    return 0
  else:
    print('Can not set this card,Boom!')
    bomb_point-=1
    Trash.append(card)
    return 1

def discard(player_name,card_index):
  global tip_point
  card=Players[player_name]['cards'][card_index]
  print('Discard card : '+card)
  del (Players[player_name]['cards'][card_index])
  del (Players[player_name]['marks'][card_index])
  Trash.append(card)
  if tip_point<8:
    tip_point+=1
  if top(All,player_name,1):
    return 0
  else:
    print('Game will reach end point.')
    return 1


    
def post(player_name,card_index):

  card=Players[player_name]['cards'][card_index]
  del (Players[player_name]['cards'][card_index])
  del (Players[player_name]['marks'][card_index])

  if(add2board(card)):
    return 1

  if top(All,player_name,1):
    return 0
  else:
    print('Game will reach end point.')
    return 1

#show all 
def show():
  os.system('clear')
  show_board() 
  show_player(Players)
  show_trash()


# This is what one could see.
def view(player_name):
  print('It\'s '+ player_name+'\'s turn.\nIn your view:')

  global Players
  tmp_view=copy.deepcopy(Players)
  del(tmp_view[player_name]['cards'])
  show_player(tmp_view)

def tips():
  global tip_point
  tip_point-=1
  player_name=input('Who do you what to prompt ? \n')
  which_type=input('Choose a type, Color or number? \n 1 ) Color \n 2 ) Number \n')
  if ( which_type!='1' and which_type !='2'):
    print ('Please input 1 or 2 ')
    return 1
  if which_type=='1':
    sp_type=input('Choose a specific type:  '+color_print)
    sp_name=Color[int(sp_type)-1]
  else:
    sp_name=input('Input the number you want to prompt: \n')

  which_card=input('Please enter the locations of all cards, separated by commas.\n')
  tip_type=type_dict[which_type]
  for each_card in which_card.split(','):
    Players[player_name]['marks'][int(each_card)-1]=sp_name
  show()
  return 0



def turn(player_name):
  global pre_end
  global end_point
  global end_name
#===this is player_name 's turn=== 
  print('It\'s '+ player_name+'\'s turn.\nIn your view:')

  os.system('clear')
  show_board() 
  view(player_name)
  show_trash()

  
  if (pre_end):
    if (player_name==end_name):
      end_point=1
  choice_loop=1
  while(choice_loop):
    choice=input('Choose your action: \n 1) Prompt\n 2) Set \n 3) Discard \n')
    if choice=='1':
      if tip_point<1:
        continue
      while(tips()):
        tips()
      choice_loop=0
    elif choice=='2':
      which_card=int(input('Choose a card: '))
      try:
        assert which_card>0 and which_card<=4," "
      except :
        print('Please check your input')
      pre_end=post(player_name,which_card-1)
      choice_loop=0
    else:
      which_card=int(input('Choose a card: '))
      try:
        assert which_card>0 and which_card<=4," "
      except :
        print('Please check your input')
      pre_end=discard(player_name,which_card-1)
      choice_loop=0

  #==============
  
  if (pre_end):
    end_name=player_name
    if bomb_point<=0:
      end_point=1
  if (end_point):
    print('The game is over now.')
      

#==========INIT=======
# var color_print is used only for print.
color_print='\n'

for cl in Color :
  color_print+=cl+' : '+str(1+Color.index(cl))+'\n'
  for nu in Number :
    All.append(cl+' '+str(nu))

# shuffle twice.
shuffle(All,2)

# Init Players :


player_number=int(input('Input player number : \n'))
assert player_number<6 and player_number>0 ,"Please check your input."
# player_number was limited.

#Add players
for each_i in range(player_number):
  name=input('Input a name for player '+ str(each_i+1)+': \n')
  tmp_player=create_player(name)
  Players=add_player(Players,tmp_player)
  tmp_player=-1


# Set up
player_name_list=[]

for each_player in Players:
  player_name_list.append(each_player)
  top(All,each_player,4)

#show()

turn_i=0
while(end_point==0):
  tmp_i=turn_i%player_number
  turn(player_name_list[tmp_i])
  turn_i+=1
