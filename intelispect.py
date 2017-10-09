from morse.builder import *

from math import pi

drone = Quadrotor()
drone.translate(x=-20, y=-20, z=1.0)
drone.rotate(z=pi/2)

video_cam = VideoCamera()
video_cam.translate(x=0, z=-0.25)
video_cam.rotate(x=+0.25)

video_cam.properties(Vertical_Flip=False)
video_cam.properties(capturing = True)
video_cam.properties(cam_width = 480)
video_cam.properties(cam_height = 320)
video_cam.properties(cam_focal = 25.0000)
video_cam.properties(Vertical_Flip = True)
drone.append(video_cam)
video_cam.add_stream('socket')

light = Light()
light.translate(x=0, z=0.1)
light.rotate(x=+0.2)
drone.append(light)

hor_laser = SickLDMRS()
hor_laser.properties(resolution = 90)
hor_laser.properties(scan_window = 180)
hor_laser.properties(laser_range = 4.0)
hor_laser.properties(Visible_arc = True)
hor_laser.properties(layers = 1)

hor_laser.translate(x=0, z=-0)
drone.append(hor_laser)
hor_laser.add_stream('socket')

gps = GPS()
gps.translate(x=0, z=-0)
gps.properties(altitude=1000.0759)
gps.properties(latitude=28.1647)
gps.properties(longitude=74.5932)
gps.level('raw')
drone.append(gps)
gps.add_stream('socket')

ver_laser = SickLDMRS()
ver_laser.properties(resolution = 90)
ver_laser.properties(scan_window = 180)
ver_laser.properties(laser_range = 4.0)
ver_laser.properties(Visible_arc = True)
ver_laser.properties(layers = 1)

ver_laser.translate(x=0, z=0.0)
ver_laser.rotate(x=+1.57)
drone.append(ver_laser)
ver_laser.add_stream('socket')

waypoint = RotorcraftWaypoint()
drone.append(waypoint)
waypoint.add_stream('socket')

pose = Pose()
drone.append(pose)
pose.add_stream('socket')

env = Environment('data/semi-transparent-pipe-with-hole.blend')
env.properties(altitude=1000.0759, latitude=28.1647, longitude=74.5932)
env.set_camera_location([10.0, -10.0, 10.0])
env.set_camera_rotation([1.0470, 0, 0.7854])