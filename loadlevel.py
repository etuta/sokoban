#!/usr/bin/env python

import sys
import pygame


class loadLevel:


    def __init__(self):
        pass


    
    def cutLvl(self, pos, rpl):
        '''cutLvl: Removes unneeded Tiles from self.level on all borders
        
        Parameters:
        ===========
        pos = unneeded Tile on the borders
        rpl = Replacement Tile on the borders
        
        '''
        
        # Cut from the left:
        for self.__yf in range(self.__y):
            if self.level[0, self.__yf] == pos:
                self.level[0, self.__yf] = rpl
            for self.__xf in range(self.__maxwidth - 1):
                    if self.level[self.__xf, self.__yf] == rpl \
                    and self.level[self.__xf + 1, self.__yf] == pos:
                        self.level[self.__xf + 1, self.__yf] = rpl

        # Cut from the right:
        for self.__yf in range(self.__y):
            if self.level[self.__maxwidth - 1, self.__yf] == pos:
                self.level[self.__maxwidth - 1, self.__yf] = rpl
            for self.__xf in range(self.__maxwidth - 1,0,-1):
                    if self.level[self.__xf, self.__yf] == rpl \
                    and self.level[self.__xf - 1, self.__yf] == pos:
                        self.level[self.__xf - 1, self.__yf] = rpl

        # Cut from the top:
        for self.__xf in range(self.__maxwidth):
            if self.level[self.__xf, 0] == pos:
                self.level[self.__xf, 0] = rpl
            for self.__yf in range(self.__y - 1):
                    if self.level[self.__xf, self.__yf] == rpl \
                    and self.level[self.__xf, self.__yf + 1] == pos:
                        self.level[self.__xf, self.__yf + 1] = rpl

        # Cut from the bottom:
        for self.__xf in range(self.__maxwidth):
            if self.level[self.__xf, self.__y - 1] == pos:
                self.level[self.__xf, self.__y - 1] = rpl
            for self.__yf in range(self.__y - 1,0,-1):
                    if self.level[self.__xf, self.__yf] == rpl \
                    and self.level[self.__xf, self.__yf - 1] == pos:
                        self.level[self.__xf, self.__yf - 1] = rpl

        
    # getPos: Get a list of [x,y]-Position.
    # pos = Searched Value in self.level
    def getPos(self, pos):
        '''getPos: Get a list of [x,y]-Position from self.level

        Parameters:
        ===========
        pos = Searched Value
        
        '''
        
        self.__returnvalue = False
        for self.__yf in range(self.__y):
            for self.__x in range(self.__maxwidth):
                if self.level[self.__x, self.__yf] == self.vals[pos][2]:
                    self.__returnvalue = [self.__x, self.__yf]
        return self.__returnvalue


    # count: count Values in self.level
    # pos = Searched Value
    def count(self, pos):
        ''' count: Count Values in self.level
        
        Parameters:
        ===========
        pos = Value that will be counted.
        
        '''

        self.__returnvalue = 0
        for self.__yf in range(self.__y):
            for self.__x in range(self.__maxwidth):
                if self.level[self.__x, self.__yf] == self.vals[pos][2]:
                    self.__returnvalue += 1
        return self.__returnvalue
    
        
    # setScreen:
    # screen = pygame.display.set_mode
    def setScreen (self, screen):
        '''setScreen: set Surface (from pygame.Surface)'''
        self.screen = screen


    # setLvlFile:
    # lvlFile = Name of Levelset, is  - of course - a File.
    # lvlNum = The Number of Level from Levelset.
    def setLvlFile (self, lvlFile, lvlNum):
        '''setLvlFile: Sets Level and File
        
        Parameters:
        ===========
        lvlFile: File to read
        lvlNum: Value, describes which Level would be loaded.
        
        '''

        self.lvlFile = lvlFile
        self.lvlNum = lvlNum


    # setVals: Set Variables and describes, how to fill the self.level
    # vals = list with the follow function:
    #   for example: ['#', 'graphic.bmp', 1]
    def setVals (self, vals):
        '''setVals: Set Variables and describes, how to fill self.level
        
        Parameters:
        ===========
        vals: The List of Variables.
        
        Example:
        ========
        var = loadLevel()
        var.setVals([
          ['#', 'foo.bmp', 1],
          ['+', 'bar.bmp', 2]
        ])
        If Levelfile has a "#"-Character, it will shows the "foo.bmp"
        and set self.level[x,y] to the Value "1".
        If Levelfile has a "+"-Character, it will shows the "bar.bmp"
        and set self.level[x,y] to the Value "2".
        
        '''

        self.vals = vals


    # TODO: Is it REALLY not possible to read the Resolution from
    # self.screen itself?
    def setCalc (self, calc):
        '''setCalc: Needed to read max_width/height from screen.Surface.'''
        self.calc = calc


    # setSym: Takes care that Graphic are symmentric.
    # (works on the "fillArray"-Method)
    def setSym (self, sym=True):
        '''setSym: Takes care that Graphic are symmentric or not.

        Parameters:
        ===========
        sym: A Bool. If it is True, the Level will be draw symmentric.
             Otherwise, the screen.Height will be completely filled.
             (Default: True)
        
        '''
        
        self.sym = sym


    # filllArray: If no Argument is given, it fills self.level and load
    # (but not display) the graphics. If Argument is given, it replace
    # self.level.
    # TODO: Just strange... I'm not sure, but I think, that isn't the
    #       right way to write Classes and Methods...
    def fillArray(self, array=None):
        '''fillArray: It fills self.level and load graphics.
        
        Parameters:
        ===========
        array: The self.level-Array. If this Parameter is set, it will
               be referenced(?) to self.level . If this Parameter is
               NOT set, it will read the Level and fill self.level from
               that file.
               (Default: None)
               
        Return-Values:
        ==============
        -1  if some Values are not set.
        -2  if LvlNum is bigger than the LvlFile had.
        
        Required Variables:
        ===================
        setSym, setCalc setLvlFile, setVals
        
        '''
        
        # Return-Values:
        # -1 : Some Vars aren't set
        # -2 : Levelfile is over.
        try:
            self.sym
            self.calc
            self.lvlNum
            self.vals
            self.lvlFile
        except AttributeError:
            return -1
        except:
            raise
        if array == None:
            self.level = {}
            self.__maxwidth = 0
            self.__x = 0
            self.__y = 0
            self.__f = open(self.lvlFile,'r')
            
            # Read as long as we reach the Level:
            while self.lvlNum != 0:
                self.__line = self.__f.readline()
                if self.__line == "\r" \
                or self.__line == "\n" \
                or self.__line == "\r\n":
                    self.lvlNum -= 1
                elif len(self.__line) == 0:
                    return -2

            # Read Level and fill Array:
            while True:
                self.__line = self.__f.readline()
                if len(self.__line) == 0:
                    return -2
                elif self.__line == "\r" \
                or self.__line == "\n" \
                or self.__line == "\r\n":
                    break
                self.__line = self.__line.rstrip()
                if self.__maxwidth < len(self.__line):
                    self.__maxwidth = len(self.__line)
                for self.__x in range(len(self.__line)):
                    for self.__i in self.vals:
                        if self.__line[self.__x] == self.__i[0]:
                            self.level[self.__x, self.__y] = self.__i[2]
                self.__y += 1

            self.__f.close()

            # Set Resolution
            if self.calc[0] > self.calc[1]:
                self.calc[0] = self.calc[1]
            else:
                self.calc[1] = self.calc[0]

            # Set symmetric graphic if necessary:
            if self.sym == True:
                if self.__y > self.__maxwidth:
                    self.__mul = self.__y
                else:
                    self.__mul = self.__maxwidth
                    if self.__mul == 0: self.__mul = 1
                self.__cwidth = self.calc[0] // self.__mul
                self.__cheight = self.calc[1] // self.__mul

            else:
                if self.__maxwidth == 0 or self.__y == 0:
                    self.__maxwidth = 1; self.__y = 1
                self.__cwidth = self.calc[0] // self.__maxwidth
                self.__cheight = self.calc[1] // self.__y

            # Fill Graphics
            self.__pic = [0 for self.__i in range(len(self.vals))]            
            for self.__i in range(len(self.vals)):
                self.__pic[self.__i] = pygame.image.load(
                  self.vals[self.__i][1]).convert()
                self.__pic[self.__i] = pygame.transform.scale(
                  self.__pic[self.__i], [self.__cwidth, self.__cheight])
            self.__picrect = self.__pic[0].get_rect()


        else:
            self.level = array

        # Fill Array if he had spaces:
        for self.__yf in range(self.__y):
            for self.__xf in range(self.__maxwidth):
                if not (self.__xf, self.__yf) in self.level:
                    self.level[self.__xf, self.__yf] = 0


    # getArray:
    def getArray(self):
        return self.level


    # drawlevel: Not really hard to understand ;)
    # TODO: Any possibility to rewrite this Method? Every Call needs a
    # pygame.display.update for the whole screen, that isn't very good...
    def drawlevel(self):
        '''drawLevel: Draws the Level, depends on self.level'''
        for self.__y in range(self.__y):
            for self.__x in range(self.__maxwidth):
                for self.__i in range(len(self.vals)):
                    if self.level[self.__x, self.__y] == \
                      self.vals[self.__i][2]:
                        self.screen.blit(self.__pic[self.__i],
                          self.__picrect.move([self.__cwidth * self.__x,
                            self.__cheight * self.__y]))
        self.__y += 1
        pygame.display.update()
    
            
if __name__ == '__main__':
    sys.stderr.write("You should not start me.")
    sys.exit()
