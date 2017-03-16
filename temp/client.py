# EzText example
from pygame.locals import *
import pygame, sys, client_add_on
import socket
import threading
import time


def main(sock):
    """
    the main function run the main screen.
    send the data from txtbx.get_value to the server, recieve new data from the server
    and display it on the screen
    """
    # initialize pygame
    pygame.init()
    # create the screen
    screen = pygame.display.set_mode((640, 240))
    # fill the screen w/ white
    screen.fill((255, 255, 255))
    # here is the magic: making the text input
    # create an input with a max length of 45,
    # and a red color and a prompt saying 'type here: '
    txtbx = client_add_on.Input(maxlength=45, color=(255, 0, 0), prompt='type here: ')
    # create the pygame clock
    clock = pygame.time.Clock()
    # main loop!

    def recv_data():
        """
        receives data from the server
        """
        while True:
            new_data = sock.recv(4000)
            if new_data != "":
                txtbx.set_value(new_data.split("#")[-1])
            time.sleep(0.4)

    threading.Thread(target=recv_data).start()
    while 1:
        # make sure the program is running at 30 fps
        clock.tick(30)
        # events for txtbx
        events = pygame.event.get()
        # process other events
        for event in events:
            # close it x button si pressed
            if event.type == QUIT:
                return
        # clear the screen
        screen.fill((255, 255, 255))
        # update txtbx
        current = txtbx.get_value()
        txtbx.update(events)
        if txtbx.get_value() != current:
            sock.send("#" + txtbx.get_value())
        # blit txtbx on the sceen
        txtbx.draw(screen)
        # refresh the display
        pygame.display.flip()


if __name__ == '__main__':
     #------------------------------------------
    my_socket = socket.socket()
    my_socket.connect(("127.0.0.1", 69))
    #------------------------------------------
    time.sleep(5)
    main(my_socket)

