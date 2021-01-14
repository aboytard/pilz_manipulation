#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 15:59:29 2020

@author: ret
"""

import rospy
import class_thread_Emission
import class_thread_Reception
import socket,sys
import tool_pose_listener_socket_message
import write_influxdb
import write_csv




def run(connexion,client_db,writer):

    try:
        #starting the thread
        th_E = class_thread_Emission.Thread_BtnPosition(connexion,"Btn1","Btn2",x1,y1,z1,x2,y2,z2,client_db,name_file)
        th_R = class_thread_Reception.ThreadReception(connexion)
        th_E.start()
        th_R.start()
    except KeyboardInterrupt :
        th_E._Thread__stop()
        th_R._Thread__stop()
        print("done") # in order to know that we have well shutdown the thread when we end the test
    tool_pose_listener_socket_message.run(th_E) ## this is the node hearing the tool_pose_position and telling the th_Emission to send the msg to the Rpi
    
''' Add this part and use it when the ret is not running
I am afraid that this thread that I setup as daemon could be mutex by the other thread, and get bad information'''
def get_information_pilz(pilz_object_class_pilz_info,client_db, writer):
    pass
''' '''

if __name__ == '__main__':
    try:
        # I use the position of the end effector 
        ''' To use with the endurance_demo launch'''
        x1 = -0.1
        y1 = -0.5
        z1 = 0.319 -0.03 # -0.03 is the argument we gave to the pick and place to deal with
        x2 = 0.05
        y2 = -0.5
        z2 = 0.319 -0.03 
        print("lancement")
        host = '10.4.11.117'
        port = 5003
            #Establishment of the connection :
        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            connexion.connect((host, port))
        except socket.error:
            print "Connection has failed."
            sys.exit()    
        print "Connection established with the servor."
        name_file = write_csv.create_csv_file(write_csv.header, write_csv.name_file)
        client_db = write_influxdb.write_into_db()
        run(connexion,client_db,name_file) # Define in which way and where we want to log the data 
    except rospy.ROSInterruptException or KeyboardInterrupt:
        connexion.close()
        print("Close the socket communication")
        pass