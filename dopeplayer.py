from guizero import *
import pygame
import os
import subprocess
import time
from search_class import Upper_Search, Lower_Search

font = 'Helvetica'
text_size = 10
appwidth = 600
appheight = 450
lbwidth = 200
lbheight = 338
buttwidth = 5
buttheight = 1
volbuttwidth = 2
volbuttheight = 1
search_input_width = 28
light_grey = 130, 130, 130
medium_grey = 100, 100, 100
medium_grey_1 = 70, 70, 70
medium_grey_2 = 60, 60, 60
dark_grey = 40, 40, 40
off_white = 255, 255, 240
search_butt_width = 13
search_butt_height = search_butt_width

music_folder = '/path/to/your/Music'

pygame.mixer.init()

def artist():
    for filenames in os.listdir(music_folder):
        artist_list.append(filenames)

def albums():
    album_list.clear()
    music_list.clear()
    error.value=''
    for filenames in os.listdir('%s/%s' % (music_folder, artist_list.value)):
        if filenames.endswith('.mp3'):
            music_list.append(filenames)
        else:
            album_list.append(filenames)

def mp3s():
    music_list.clear()
    error.value=''
    for filenames in os.listdir('%s/%s/%s' % (music_folder, artist_list.value, album_list.value)):
        if filenames.endswith('.mp3'):
            music_list.append(filenames)
        else:
            error.value='No mp3 files found'

def play():
    play.text = 'Playing'
    if album_list.value == None:
        pygame.mixer.music.load('%s/%s/%s' % (music_folder, artist_list.value, music_list.value))
        pygame.mixer.music.play()
        now_playing.value = music_list.value
    else:
        pygame.mixer.music.load('%s/%s/%s/%s' % (music_folder, artist_list.value, album_list.value, music_list.value))
        pygame.mixer.music.play()
        now_playing.value = music_list.value
    
def pause():
    play.text = 'Play'
    if pause.text=='Pause':
        pygame.mixer.music.pause()
        pause.text='Unpause'
    elif pause.text=='Unpause':
        pygame.mixer.music.unpause()
        pause.text='Pause'
        play.text = 'Playing'

def stop():
    pygame.mixer.music.stop()
    now_playing.value = ''
    play.text = 'Play'

def search_artist():
    album_list.clear()
    music_list.clear()
    search_in = artist_list.items
    search_input = search_box.value
    search_results = artist_list
    search_results.clear()
    for filenames in search_in:
        if filenames.startswith('%s' % search_input):
            search_results.append(filenames)
        elif search_input == '<':
            artist_list.clear()
            album_list.clear()
            music_list.clear()
            error.value=''
            search_box.value='Search Artist'
            search_box.font=font
            search_box.text_color=off_white
            for filenames in os.listdir(music_folder):
                artist_list.append(filenames)
        elif search_input in Upper_Search:
            letter = Upper_Search.index(search_input)
            if filenames.startswith(Lower_Search[letter]):
                search_results.append(filenames)
        elif search_input in Lower_Search:
            letter = Lower_Search.index(search_input)
            if filenames.startswith(Upper_Search[letter]):
                search_results.append(filenames)
        
def volume_up():
    vol_down.enable()
    get_level = current_vol.value
    step = 0.10
    up = float(get_level) + float(step)
    rup = round(up, 1)
    pygame.mixer.music.set_volume(rup)
    current_vol.value = rup
    if rup == 1.0:
        vol_up.disable()
        
def volume_down():
    vol_up.enable()
    get_level = current_vol.value
    step = 0.10
    down = float(get_level) - float(step)
    rdown = round(down, 1)
    pygame.mixer.music.set_volume(rdown)
    current_vol.value = rdown
    if rdown == 0.0:
        vol_down.disable()

def elapse_time():
    if play.text == 'Playing':
        sec.value = int(sec.value) + 1
        if sec.value == str(60):
            sec.value = 0
            minu.value = int(minu.value) + 1
            if minu.value == str(60):
                minu.value = 0
    elif pause.text == 'Pause':
        sec.value = 0
        minu.value = 0        
  
app = App(title='Dope Player!', width=appwidth, height=appheight, layout='grid', bg=dark_grey)

box1 = Box(app, layout='grid', grid=[0,0])
box4 = Box(app, layout='grid', grid=[0,1], align='left')
box2 = Box(app, layout='grid', grid=[0,2])
box3 = Box(app, layout='grid', grid=[0,3], align='left')

previous_track = PushButton(box1, text='Previous', command=None, grid=[3,0], width=buttwidth, height=buttheight, align='left')
previous_track.bg=medium_grey
previous_track.text_color=off_white
play = PushButton(box1, text='Play', command=play, grid=[4,0], width=buttwidth, height=buttheight, align='left')
play.bg=medium_grey
play.text_color=off_white
pause = PushButton(box1, text='Pause', command=pause, grid=[5,0], width=buttwidth, height=buttheight, align='left')
pause.bg=medium_grey_1
pause.text_color=off_white
next_track = PushButton(box1, text='Next', command=None, grid=[6,0], width=buttwidth, height=buttheight, align='left')
next_track.bg=medium_grey_1
next_track.text_color=off_white
stop = PushButton(box1, text='Stop', command=stop, grid=[7,0], width=buttwidth, height=buttheight, align='left')
stop.bg=medium_grey_2
stop.text_color=off_white

vol_down = PushButton(box1, command=volume_down, text='-V', grid=[8,0], width=volbuttwidth, height=volbuttheight)
vol_down.bg=medium_grey_2
vol_down.text_color=off_white
current_vol = Text(box1, text='0.4', grid=[9,0])
current_vol.text_color=off_white
vol_up = PushButton(box1, command=volume_up, text='V+', grid=[10,0], width=volbuttwidth, height=volbuttheight)
vol_up.bg=medium_grey_2
vol_up.text_color=off_white
vol_up.after(100, volume_up)

now_playing = Text(box4, text='', grid=[0,0], align='left')
now_playing.text_color=off_white
now_playing.font=font

minu = Text(box1, text='0', grid=[0,0])
minu.text_color=off_white
minu.font=font

colon = Text(box1, text=':', grid=[1,0])
colon.text_color=off_white
colon.font=font

sec = Text(box1, text='0', grid=[2,0])
sec.repeat(1000, elapse_time)
sec.text_color=off_white
sec.font=font

error = Text(box4, text='', grid=[4,0], align='right')
error.text_color=off_white
error.font=font

artist_list = ListBox(box2, items=[], scrollbar=False, command=albums, width=lbwidth, height=lbheight, grid=[0,1])
artist_list.after(100, artist)
artist_list.font=font
artist_list.text_size=text_size
artist_list.text_color=off_white
artist_list.bg=medium_grey

album_list = ListBox(box2, items=[], scrollbar=False, command=mp3s, width=lbwidth, height=lbheight, grid=[1,1])
album_list.font=font
album_list.text_size=text_size
album_list.text_color=off_white
album_list.bg=medium_grey_1

music_list = ListBox(box2, items=[], scrollbar=False, width=lbwidth, height=lbheight, grid=[2,1])
music_list.font=font
music_list.text_size=text_size

music_list.text_color=off_white
music_list.bg=medium_grey_2

search_box = TextBox(box3, width=search_input_width, grid=[0,0])
search_box.value='Search Artist'
search_box.font=font
search_box.text_color=off_white
search_box.bg=medium_grey

search_button = PushButton(box3, command=search_artist, image='images/black_search.png', width=search_butt_width, height=search_butt_height, grid=[1,0])
search_button.bg=medium_grey_1







app.display()
