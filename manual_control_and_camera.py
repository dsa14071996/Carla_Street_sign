import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import random
import time


def main():

    actor_list = []

    try:
            # First of all, we need to create the client that will send the requests
            # to the simulator. Here we'll assume the simulator is accepting
            # requests in the localhost at port 2000.
            client = carla.Client('localhost', 2000)
            client.set_timeout(10.0)

            # # Getting world and actors
            world = client.get_world()
            # actors = world.get_actors()

            # Get blueprint blueprint_library
            blueprint_library = world.get_blueprint_library()

            # Spawning Vehicel in Carla
            vehicle_bp = random.choice(blueprint_library.filter('vehicle.tesla.*'))
            transform = carla.Transform(carla.Location(x=-50, y=2, z=3), carla.Rotation())
            vehicle = world.spawn_actor(vehicle_bp, transform)
            vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer = 0.0))
            actor_list.append(vehicle)
            #vehicel.set_autopilot(True)

            # Mounting Camera on the Vehicel
            camera_bp = blueprint_library.find('sensor.camera.rgb')
            camera_bp.set_attribute('image_size_x', '1920')
            camera_bp.set_attribute('image_size_y', '1080')
            camera_bp.set_attribute('fov', '110')
            camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
            camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
            camera.listen(lambda image: image.save_to_disk('output/%06d.png' %image.frame_number))
            actor_list.append(camera)

            # Deciding simulation time.
            time.sleep(120)

    finally:
        for actor in actor_list:
            actor.destroy()
        print('All clear')

if __name__ == '__main__':
        main()
