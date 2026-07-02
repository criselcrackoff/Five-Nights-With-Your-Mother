from pypresence import Presence
import pygame
import time

class RichPresense:
    def __init__(self):

        self.__client_id = "1444378635426337030"
        self.__rpc = Presence(self.__client_id)

        self.__last_rpc = None
    
    def initiate_rpc(self):
        try:
            self.__rpc.connect()
            self.__rpc.update(details="In a menu")
        except:
            pass    
        
    def update_rpc(self, state, details):

        rpc_key = f"{state}|{details}"

        if rpc_key == self.__last_rpc:
            return

        self.__last_rpc = rpc_key

        try:

            self.__rpc.update(
                state=state,
                details=details
            )

        except:
            pass