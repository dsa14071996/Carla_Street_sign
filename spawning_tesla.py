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

    try:
        # First of all, we need to create the client that will send the requests
        # to the simulator. Here we'll assume the simulator is accepting
        # requests in the localhost at port 2000.
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)

        world = client.get_world()

        blueprint_library = world.get_blueprint_library()

        vehicle_bp = random.choice(blueprint_library.filter('vehicle.tesla.*'))

        transform = random.choice(world.get_map().get_spawn_points())

        vehicle = world.spawn_actor(vehicle_bp, transform)

        vehicle.set_autopilot(False)

        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', '1920')
        camera_bp.set_attribute('image_size_y', '1080')
        camera_bp.set_attribute('fov', '110')
        camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)


        time.sleep(60)

    finally:

        print('destroying actors')
        camera.destroy()
        vehicle.destroy()
        #client.apply_batch([carla.command.DestroyActor())
        print('done.')


if __name__ == '__main__':

    main()
