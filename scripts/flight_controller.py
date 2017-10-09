import math
import sys

import numpy
from pymorse import Morse
import pygame
import base64
from field_api_service import FieldAPIService
from issue import Issue
from fault_detector import FaultDetector
from PIL import Image
import numpy as np
import cv2

pygame.init()
w = 480
h = 320
resolution = (w, h)

height = 3.5
delta = 0.3
dyaw = 0.05;

def show_image(image, screen):
    surface = pygame.image.frombuffer(image, resolution, 'RGBA');
    screen.blit(surface, (0, 0))
    pygame.display.flip()

def get_cv_image(image):
    pil_image = Image.frombytes("RGBA", (480, 320), image)
    pil_image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
    return np.array(pil_image)

field = FieldAPIService()
fault_detector = FaultDetector()

def control_quadcoptor(x_coord=0,y_coord=0,z_coord=0, angle = 0):

    screen = pygame.display.set_mode(resolution)
    with Morse() as morse:
        motion = morse.drone.waypoint
        pose = morse.drone.pose
        video_cam = morse.drone.video_cam
        hor_laser = morse.drone.hor_laser
        ver_laser = morse.drone.ver_laser
        gps = morse.drone.gps

        current_pos = {'yaw': angle, 'tolerance': 0.5, 'x': x_coord, 'z': z_coord, 'y': y_coord};
        new_pos = current_pos
        while True:
            capture = video_cam.get()
            image = base64.b64decode(capture['image'])
            show_image(image, screen)
            events = pygame.event.get()
            yaw = pose.get()['yaw']
            x = current_pos['x']
            y = current_pos['y']

            if len(sys.argv) > 1 and sys.argv[1] == 'auto':
                #Automation
                new_pos = automatic_navigation(image, current_pos, hor_laser, new_pos, ver_laser, x, y, yaw, gps)
            else:
                # Keyboard control
                new_pos = manual_navigation(image, current_pos, events, new_pos, x, y, yaw, gps)


            next_pos = dict(list(current_pos.items()) + list(new_pos.items()))
            motion.publish(next_pos)


def automatic_navigation(image, current_pos, hor_laser, new_pos, ver_laser, x, y, yaw, gps):
    range_list = hor_laser.get()['range_list']
    if range_list[1] >= 2.5:
        new_pos = move_forward(current_pos, x, y, yaw)

    elif range_list[2] == 4:
        new_pos = turn_left(current_pos, 1.57)

    elif range_list[0] == 4:
        new_pos = turn_right(current_pos, 1.57)
    faulty, image_array = fault_detector.isFaulty( get_cv_image(image))
    if faulty:
        im = Image.fromarray(image_array)
        im.save('test.jpg')
        create_issue('test.jpg', gps);
    return new_pos


def manual_navigation(image, current_pos, events, new_pos, x, y, yaw, gps):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                new_pos = move_forward(current_pos, x, y, yaw)
            elif event.key == pygame.K_LEFT:
                new_pos = move_left(current_pos, x, y, yaw)
            elif event.key == pygame.K_RIGHT:
                new_pos = move_right(current_pos, x, y, yaw)
            elif event.key == pygame.K_DOWN:
                new_pos = move_back(current_pos, x, y, yaw)
            elif event.key == pygame.K_a:
                new_pos = turn_left(current_pos, dyaw)
            elif event.key == pygame.K_d:
                new_pos = turn_right(current_pos, dyaw)
            elif event.key == pygame.K_w:
                new_pos = climb_up(current_pos)
            elif event.key == pygame.K_s:
                new_pos = drop_down(current_pos)
            elif event.key == pygame.K_p:
                surface = pygame.image.frombuffer(image, resolution, 'RGBA');
                pygame.image.save(surface, 'test.jpg')
                create_issue('test.jpg', gps);

    return new_pos


def create_issue(filename, gps):
    gps_coord = gps.get()
    new_issue = Issue(gps_coord)
    field.send_create_issue_request(new_issue)
    field.send_attach_photo_to_issue_request(new_issue, filename)


def drop_down(waypoint):
    waypoint['z'] -= delta*0.25
    return waypoint


def climb_up(waypoint):
    waypoint['z'] += delta*0.25
    return waypoint


def turn_right(waypoint, angle):

    waypoint['yaw'] -= angle
    return waypoint


def turn_left(waypoint, angle):
    waypoint['yaw'] += angle
    return waypoint


def move_back(waypoint, x, y, yaw):
    waypoint['x'] = x - (delta * math.cos(yaw))
    waypoint['y'] = y - (delta * math.sin(yaw))
    return waypoint


def move_right(waypoint, x, y, yaw):
    waypoint['x'] = x + (delta * math.sin(yaw))
    waypoint['y'] = y - (delta * math.cos(yaw))
    return waypoint


def move_left(waypoint, x, y, yaw):
    waypoint['x'] = x - (delta * math.sin(yaw))
    waypoint['y'] = y + (delta * math.cos(yaw))
    return waypoint


def move_forward(waypoint, x, y, yaw):
    waypoint['x'] = x + (delta * math.cos(yaw))
    waypoint['y'] = y + (delta * math.sin(yaw))
    return waypoint


def main():
    """ Main behaviour """
    control_quadcoptor(x_coord=-3.5 , y_coord= -20, z_coord= 2, angle= 1.57)


if __name__ == '__main__':
    main()
