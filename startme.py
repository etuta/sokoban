#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

import sys

# Be Python 2.5-Compatible:
try:
    import json
except ImportError:
    import simplejson as json

import os
import pygame
import settings as ini
import dumbmenu as dm
import loadlevel as ll

pygame.init()


def setDefaultFont():
    return pygame.font.SysFont("Courier", int(ini.fontsize / 4.6), True)


def setManualFont():
    return pygame.font.SysFont("Courier", int(ini.fontsize // 2), True)    


def waitOnKey():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(ini.framerate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit(1)
            elif event.type == pygame.KEYDOWN: run = False


def main():
    # A few static Things:
    black  =   0,  0,  0
    red    = 255,  0,  0
    green  =   0,255,  0
    blue   =   0,  0,255    
    grey   = 128,128,128
    yellow = 255,255,  0
    white  = 255,255,255

    clock = pygame.time.Clock()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    gradir = os.curdir + os.sep + "graphics" + os.sep + \
             "skins" + os.sep + ini.skin + os.sep
    savdir = os.curdir + os.sep + "saves" + os.sep
    runReplay = []


    # Init Pygame, create Object, load Graphics
    pygame.init()
    if ini.fullscreen == 1:
        screen = pygame.display.set_mode(ini.size, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(ini.size)
    pygame.key.set_repeat(ini.repeat, ini.framerate)
    pygame.display.set_caption("Sokoban")

    # Use loadLevel-Class
    lev = ll.loadLevel()
    lev.setScreen(screen)
    lev.setVals([
      [' ',gradir + "bottom.bmp",0],
      ['#',gradir + "block.bmp",1],
      ['@',gradir + "player.bmp",2],
      ['$',gradir + "box.bmp",3],
      ['.',gradir + "place.bmp",4],
      ['*',gradir + "box_over_place.bmp",5],
      ['+',gradir + "player_over_place.bmp",6]
    ])
    lev.setCalc(list(ini.size))
    lev.setSym(True)

    # Sound
    if ini.sound:
        tada = pygame.mixer.Sound(os.curdir + \
          os.sep + "sounds" + os.sep + "tada.wav")
        tada.set_volume(0.5)

    # Load all Images
    tm = pygame.image.load(gradir + "titlescreen.bmp").convert()
    tm = pygame.transform.scale(tm, ini.size)
    tmrect = tm.get_rect()
    hud = pygame.image.load(gradir + "hud.bmp").convert()
    hud = pygame.transform.scale(hud, [ini.width - ini.height, ini.height])
    hudrect = hud.get_rect()
    hudrect = hudrect.move(ini.width - (ini.width - ini.height), 0)
    font = setDefaultFont()
    back = pygame.image.load(gradir + "background.bmp").convert()
    back = pygame.transform.scale(back, [ini.width, ini.height])
    backrect = back.get_rect()
    setwin = pygame.image.load(gradir + "setwinner.bmp").convert()
    setwin = pygame.transform.scale(setwin, [ini.width, ini.height])
    setwinrect = setwin.get_rect()

    # Titlescreen, shows Mainmenu:
    while True:
        screen.blit(tm, tmrect)
        pygame.display.update()
        dmval = dm.dumbmenu(screen, (
                'Start Game',
                'Manual',
                'Credits',
                'Quit Game'), ini.xpos, ini.ypos,
                    ini.fontsize, ini.distance, white, red)
        
        # Quit Game:
        if dmval == 3:
            sys.stdout.write("Thanks for Playing the Game. Bye bye...\n")
            sys.exit()
        
        # Manual
        elif dmval == 1:
            y = 12
            screen.blit(back, backrect)
            font = setManualFont()
            for z in ("The Objective is easy: Just push all the",
                      "boxes into their places. But you're only",
                      "able to push the boxes, you cannot pull",
                      "them! After all boxes are on their places,",
                      "you'll get - surprise, surprise - the next",
                      "Level :)",
                      "About saving: Each Level is a different",
                      "Savestate. That means, you can play another",
                      "Levelset and save, without losing your",
                      "previous Savestate from the previous",
                      "Levelset. If you'll save, the game will save",
                      "the Level from the current Levelset and(!)",
                      "every move you have taken.",
                      "",
                      "Oh, and a tip for Beginners: Maybe it's the",
                      "best you start with \"Microban\"-Levelsets.",
                      "These Levels are much easier than the",
                      "\"Sasquatch\"-Levels...                  :-)",
                     ):
                y -= .5

                text = font.render(z, True, yellow)
                textrect = text.get_rect()
                textrect = textrect.move(40, ini.height - ini.fontsize * y)
                screen.blit(text, textrect)

            pygame.display.update()

            font = setDefaultFont()
            waitOnKey()
            
        # Credits
        elif dmval == 2:
            screen.blit(back, backrect)
            font = setManualFont()
            y = 10.5
            for z in ("Thanks/Greetings to:",
                      "- David W. Skinner, who released his",
                      "  Sokoban-Levels",
                      "  (http://users.bentonrea.com/~sasquatch/)",
                      "- The Python-, Pygame- and SDL-Community",
                      "- The german QBasic-Community",
                      "- My Betatesters (if I had someone...)",
                      "",
                      "- Of course YOU, because you are",
                      "  playing this game :)"):
                y -= 0.5
                      
                text = font.render(z, True, yellow)
                textrect = text.get_rect()
                textrect = textrect.move(40, ini.height - ini.fontsize * y)
                screen.blit(text, textrect)

            pygame.display.update()
            font = setDefaultFont()
            waitOnKey()

        
        # Start Game:
        elif dmval == 0:
            
            # First: Read Levelsets, Player must choose one:
            # TODO: What if there are more Levelsets on the Folder?
            levels = ()
            for j in os.walk(os.curdir + os.sep + "levelsets" + os.sep):
                levels = j[2]
            levels.append('[Back to Main Menu]')
            screen.blit(tm, tmrect)
            font = pygame.font.SysFont("Courier", ini.lvlfont, True)
            text = font.render("Which Levelset do you want to play?", True, yellow)
            textrect = text.get_rect()
            textrect = textrect.move(ini.xpos - ini.lvlfont,
              ini.ypos - ini.lvlfont)
            screen.blit(text, textrect)
            pygame.display.update()            
            dmval = dm.dumbmenu(screen, levels,
                ini.xpos - ini.lvlfont, ini.ypos, ini.lvlfont, ini.distance,
                white, red)    
            font = setDefaultFont()
            
            # Want Back to Main Menu? No Problem...
            if dmval == len(levels) - 1:
                continue
            
            else:
                lvlNum = 0
                lvlminus = -1
                MainMenu = True
                loadSave = False
                
                while MainMenu:
                    lev.setLvlFile(os.curdir + os.sep + "levelsets" + \
                      os.sep + levels[dmval], lvlNum)

                    # First: Has Levelsets enough Levels (depends on
                    # "lvlNum")? If not, the Levelset is finished
                    # (fillArray() returns -2 if it is so...).
                    if lev.fillArray() == -2:
                        screen.blit(setwin, setwinrect)
                        pygame.display.update()
                        waitOnKey()
                        MainMenu = False
                        continue

                    # Cut Level, find out the Playerposition
                    lev.cutLvl(0,-1)
                    ppos = lev.getPos(2)
                    if not ppos: ppos = lev.getPos(6)

                    level = lev.getArray()
                    pmov = [0,0]
                    replay = []
                    replaymove = 0
                    steps = 0
                    updateGraphic = True
                    nextLvl = False
                    showWinner = False

                    # Now the very hard Engine ;)
                    while MainMenu:
                        
                        # No boxes (in other Words: Every boxes are
                        # on their positions)? Then, load next Level!
                        if lev.count(3) == 0:
                            nextLvl = True

                        if nextLvl:
                            lev.drawlevel()
                            if showWinner:
                                font = pygame.font.SysFont("Courier",
                                  ini.fontsize, True)
                                text = text = font.render("WINNER!",
                                  True, yellow)
                                textrect = text.get_rect()
                                screen.blit(text, textrect.move(
                                  ini.height // 2 - ini.fontsize,
                                  ini.height // 2 - ini.fontsize))
                                pygame.display.update()
                                if ini.sound:
                                    tada.play(0)
                                font = setDefaultFont()
                                pygame.time.wait(ini.winnertime)
                            else:
                                lvlminus += 1
                            lvlNum += 1
                            break

                        # Restore Savepoint (important for replay-list!)
                        if len(runReplay):
                            nextLvl = False
                            if runReplay[0] == 1 or runReplay[0] == 5:
                                pmov = [-1,0]
                            elif runReplay[0] == 2 or runReplay[0] == 6:
                                pmov = [0,-1]
                            elif runReplay[0] == 3 or runReplay[0] == 7:
                                pmov = [0,1]
                            elif runReplay[0] == 4 or runReplay[0] == 8:
                                pmov = [1,0]
                            runReplay = runReplay[1:]

                        if not len(runReplay):
                            clock.tick(ini.framerate)
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT: sys.exit()
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE    \
                                    and updateGraphic == False:
                                        text = font.render("Really Quit?",
                                          True, yellow)
                                        textrect = text.get_rect()
                                        textrect = textrect.move(ini.hudfontxpos,
                                          ini.height - ini.fontsize * 6.5)
                                        screen.blit(text, textrect)
                                        pygame.display.update(textrect)
                                        if dm.dumbmenu(screen, ('Yes','No'),
                                          ini.hudfontxpos, ini.height // 2,
                                          int(ini.fontsize / 4.6),
                                          ini.distance, yellow, blue) == 0:
                                            MainMenu = False
                                        else:
                                            updateGraphic = True
                                    elif event.key == pygame.K_LEFT:
                                        pmov = [-1,0]; showWinner = True
                                    elif event.key == pygame.K_RIGHT:
                                        pmov = [1,0]; showWinner = True
                                    elif event.key == pygame.K_UP:
                                        pmov = [0,-1]; showWinner = True
                                    elif event.key == pygame.K_DOWN:
                                        pmov = [0,1]; showWinner = True
                                    elif event.key == pygame.K_c:
                                        if ini.allowCheating:
                                            nextLvl = True
                                            showWinner = False
                                            lvlminus -= 1
                                    elif event.key == pygame.K_r:
                                        nextLvl = True
                                        showWinner = False
                                        lvlNum -= 1
                                        lvlminus -= 1
                                    elif event.key == pygame.K_s:
                                        f = file(savdir + levels[dmval], 'w')
                                        f.write(str(lvlNum) + "\r\n")
                                        f.write(str(lvlminus) + "\r\n")
                                        f.write(str(steps) + "\r\n")
                                        f.write(json.dumps(replay) + "\r\n")
                                        f.close()
                                        font = pygame.font.SysFont("Courier",
                                          ini.fontsize, True)
                                        text = text = font.render("Game Saved!",
                                          True, red)
                                        textrect = text.get_rect()
                                        screen.blit(text, textrect.move(
                                          ini.height // 2 - ini.fontsize,
                                          ini.height // 2 - ini.fontsize))
                                        pygame.display.update()
                                        font = setDefaultFont()

                                    elif event.key == pygame.K_l:
                                        try:
                                            f = file(savdir + levels[dmval], 'r')
                                            lvlNum = int(f.readline())
                                            lvlminus = int(f.readline()) - 1
                                            steps = int(f.readline())
                                            steps = 0
                                            runReplay = json.loads(f.readline())
                                            type(runReplay)
                                            nextLvl = True
                                            showWinner = False
                                            lvlNum -= 1
                                            f.close()
                                            
                                        except IOError:
                                            pass
                                        except:
                                            raise
                                    elif event.key == pygame.K_u \
                                    and len(replay) > 0:
                                        steps -= 1
                                        replaymove = 1
                                        if replay[-1] == 1:
                                            pmov = [1,0]
                                        elif replay[-1] == 2:
                                            pmov = [0,1]
                                        elif replay[-1] == 3:
                                            pmov = [0,-1]
                                        elif replay[-1] == 4:
                                            pmov = [-1,0]
                                        else:
                                            replaymove = 2
                                            if replay[-1] == 5:
                                                pmov = [1,0]
                                            elif replay[-1] == 6:
                                                pmov = [0,1]
                                            elif replay[-1] == 7:
                                                pmov = [0,-1]
                                            elif replay[-1] == 8:
                                                pmov = [-1,0]
                                        replay = replay[0:-1]

                        # Move!    
                        if pmov != [0,0] or updateGraphic == True:
                            # Move to (empty?) box-field?
                            if level[ppos[0] + pmov[0],
                              ppos[1] + pmov[1]] == 0 \
                              or level[ppos[0] + pmov[0],
                              ppos[1] + pmov[1]] == 4:
                                if level[ppos[0], ppos[1]] == 6:
                                    level[ppos[0], ppos[1]] = 4
                                elif level[ppos[0], ppos[1]] == 2:
                                    level[ppos[0], ppos[1]] = 0
                                ppos[0] += pmov[0]; ppos[1] += pmov[1]
                                if level[ppos[0], ppos[1]] == 4:
                                    level[ppos[0], ppos[1]] = 6
                                elif level[ppos[0], ppos[1]] == 0:
                                    level[ppos[0], ppos[1]] = 2
                                    
                                if replaymove == 0:                
                                    if pmov == [-1,0]: replay.append(1)
                                    elif pmov == [0,-1]: replay.append(2)
                                    elif pmov == [0,1]: replay.append(3)
                                    elif pmov == [1,0]: replay.append(4)
                                    steps += 1

                                
                            # Move to box:
                            elif level[ppos[0] + pmov[0],
                              ppos[1] + pmov[1]] == 3 \
                              or level[ppos[0] + pmov[0],
                              ppos[1] + pmov[1]] == 5:
                                # Is that move possible?
                                if level[ppos[0] + pmov[0] * 2,
                                  ppos[1] + pmov[1] * 2] == 0 or \
                                  level[ppos[0] + pmov[0] * 2,
                                  ppos[1] + pmov[1] * 2] == 4:
                                    if level[ppos[0], ppos[1]] == 6:
                                        level[ppos[0], ppos[1]] = 4
                                    elif level[ppos[0], ppos[1]] == 2:
                                        level[ppos[0], ppos[1]] = 0
                                    ppos[0] += pmov[0]; ppos[1] += pmov[1]
                                    if level[ppos[0], ppos[1]] == 5:
                                        level[ppos[0], ppos[1]] = 6
                                    elif level[ppos[0], ppos[1]] == 3:
                                        level[ppos[0], ppos[1]] = 2

                                    
                                    # Move that box:

                                    if level[ppos[0] + pmov[0],
                                      ppos[1] + pmov[1]] == 0:
                                        level[ppos[0] + pmov[0],
                                          ppos[1] + pmov[1]] = 3
                                    elif level[ppos[0] + pmov[0],
                                      ppos[1] + pmov[1]] == 4:
                                        level[ppos[0] + pmov[0],
                                          ppos[1] + pmov[1]] = 5
                                        
                                    if replaymove == 0:
                                        if pmov == [-1,0]: replay.append(5)
                                        elif pmov == [0,-1]: replay.append(6)
                                        elif pmov == [0,1]: replay.append(7)
                                        elif pmov == [1,0]: replay.append(8)
                                        steps += 1

                            # Replay, if box has been pushed:
                            if replaymove == 2:
                                # "push" box
                                if level[ppos[0] - pmov[0],
                                  ppos[1] - pmov[1]] == 0:
                                    level[ppos[0] - pmov[0],
                                      ppos[1] - pmov[1]] = 3
                                elif level[ppos[0] - pmov[0],
                                  ppos[1] - pmov[1]] == 4:
                                    level[ppos[0] - pmov[0],
                                      ppos[1] - pmov[1]] = 5
                                # "remove" box
                                if level[ppos[0] - pmov[0] * 2,
                                  ppos[1] - pmov[1] * 2] == 3:
                                    level[ppos[0] - pmov[0] * 2,
                                      ppos[1] - pmov[1] * 2] = 0
                                elif level[ppos[0] - pmov[0] * 2,
                                  ppos[1] - pmov[1] * 2] == 5:
                                    level[ppos[0] - pmov[0] * 2,
                                      ppos[1] - pmov[1] * 2] = 4
                                
                            # Draw Graphics
                            if not len(runReplay):
                                screen.blit(back, backrect)
                                screen.blit(hud, hudrect)

                                y = 0
                                for z in ['Level: ' + str(lvlNum -lvlminus),
                                          'Steps: ' + str(steps)]:
                                
                                    y += .5
                                    text = font.render(z, True, black)
                                    textrect = text.get_rect()
                                    textrect = textrect.move(ini.hudfontxpos,
                                      ini.fontsize * y)
                                    screen.blit(text, textrect)
                                
                                y = 4.5
                                for z in ("< ^ > v = Move Player",
                                          "   u    = Undo Move",
                                          "   s    = Save Level",
                                          "   l    = Load Level",
                                          "   r    = Reset Level",
                                          "  ESC   = Quit Game"):
                                    y -= .5
                                    text = font.render(z, True, black)
                                    textrect = text.get_rect()
                                    textrect = textrect.move(ini.hudfontxpos,
                                      ini.height - ini.fontsize * y)
                                    screen.blit(text, textrect)
                                    
                                if ini.allowCheating:
                                    y -= .5
                                    text = font.render("   c    = Cheat Level",
                                      True, black)
                                    textrect = text.get_rect()
                                    textrect = textrect.move(ini.hudfontxpos,
                                      ini.height - ini.fontsize * y)
                                    screen.blit(text, textrect)

                                lev.fillArray(level)

                                pmov = [0,0]
                                replaymove = 0
                                
                                updateGraphic = False
                                lev.drawlevel()

if __name__ == '__main__':
    main()
else:
    sys.stderr.write("You should not import me.")
    sys.exit()
