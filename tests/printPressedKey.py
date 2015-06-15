#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

class cFontManager:
    def __init__(self, listOfFontNamesAndSizesAsTuple):
        '''
        Pass in a tuple of 2-item tuples.  Each 2-item tuple is a fontname / 
        size pair. To use the default font, pass in a None for the font name.
        Font objects are created for each of the pairs and can then be used
        to draw text with the Draw() method below.
        
        Ex: fontMgr = cFontManager(((None, 24), ('arial', 18), ('arial', 24),
            ('courier', 12), ('papyrus', 50)))
        '''
        self._fontDict = {}
        for pair in listOfFontNamesAndSizesAsTuple:
            assert len(pair) == 2, \
                "Pair must be composed of a font name and a size - ('arial', 24)"
            if pair[0]:
                fontFullFileName = pygame.font.match_font(pair[0])
                assert fontFullFileName, 'Font: %s Size: %d is not available.' % pair
            else:
                fontFullFileName = None # use default font
            self._fontDict[pair] = pygame.font.Font(fontFullFileName, pair[1])
 
    def Draw(self, surface, fontName, size, text, rectOrPosToDrawTo, color,
            alignHoriz='left', alignVert='top', antialias=False):
        '''
        Draw text with the given parameters on the given surface.
        
        surface - Surface to draw the text onto.
        
        fontName - Font name that identifies what font to use to draw the text.
        This font name must have been specified in the cFontManager 
        
        rectOrPosToDrawTo - Where to render the text at.  This can be a 2
        item tuple or a Rect.  If a position tuple is used, the align
        arguments will be ignored.
        
        color - Color to draw the text with.
        
        alignHoriz - Specifies horizontal alignment of the text in the
        rectOrPosToDrawTo Rect.  If rectOrPosToDrawTo is not a Rect, the
        alignment is ignored.
        
        alignVert - Specifies vertical alignment of the text in the
        rectOrPosToDrawTo Rect.  If rectOrPosToDrawTo is not a Rect, the
        alignment is ignored.
 
        antialias - Whether to draw the text anti-aliased or not.
        '''
        pair = (fontName, size)
        assert pair in self._fontDict, \
            'Font: %s Size: %d is not available in cFontManager.' % pair
        fontSurface = self._fontDict[(fontName, size)].render(text,
            antialias, color)
        if isinstance(rectOrPosToDrawTo, tuple):
            surface.blit(fontSurface, rectOrPosToDrawTo)
        elif isinstance(rectOrPosToDrawTo, pygame.Rect):
            fontRect = fontSurface.get_rect()
            # align horiz
            if alignHoriz == 'center':
                fontRect.centerx = rectOrPosToDrawTo.centerx
            elif alignHoriz == 'right':
                fontRect.right = rectOrPosToDrawTo.right
            else:
                fontRect.x = rectOrPosToDrawTo.x  # left
            # align vert
            if alignVert == 'center':
                fontRect.centery = rectOrPosToDrawTo.centery
            elif alignVert == 'bottom':
                fontRect.bottom = rectOrPosToDrawTo.bottom
            else:
                fontRect.y = rectOrPosToDrawTo.y  # top
                
            surface.blit(fontSurface, fontRect)

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Quiz')
    fontMgr = cFontManager(((None, 24), (None, 48), ('arial', 48)))

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    white = (255,255,255)
    black = (0,0,0)
    background.fill(white)

    # Display some text
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    text = font.render("Druecke eine Taste:", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(text, textpos)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    # Event loop
    keyGotPressed = 0
    while True:
        for event in pygame.event.get():

            # Wenn Taste gedrueckt wird, anzeigen
            if event.type == pygame.KEYDOWN:
                keyName = pygame.key.name(event.key)
                fontMgr.Draw(screen, 'arial', 48, keyName, (keyGotPressed, 50), black, 'center', 'center', True)
                pygame.display.update()
                keyGotPressed = keyGotPressed + 20
                
            if event.type == QUIT:
                pygame.quit()

if __name__ == '__main__':
    main()
