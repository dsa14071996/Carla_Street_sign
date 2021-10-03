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

try:
    


    import pygame
    from pygame.locals import KMOD_CTRL
    from pygame.locals import KMOD_SHIFT
    from pygame.locals import K_0
    from pygame.locals import K_9
    from pygame.locals import K_BACKQUOTE
    from pygame.locals import K_BACKSPACE
    from pygame.locals import K_COMMA
    from pygame.locals import K_DOWN
    from pygame.locals import K_ESCAPE
    from pygame.locals import K_F1
    from pygame.locals import K_LEFT
    from pygame.locals import K_PERIOD
    from pygame.locals import K_RIGHT
    from pygame.locals import K_SLASH
    from pygame.locals import K_SPACE
    from pygame.locals import K_TAB
    from pygame.locals import K_UP
    from pygame.locals import K_a
    from pygame.locals import K_b
    from pygame.locals import K_c
    from pygame.locals import K_d
    from pygame.locals import K_g
    from pygame.locals import K_h
    from pygame.locals import K_j
    from pygame.locals import K_y
    from pygame.locals import K_m
    from pygame.locals import K_n
    from pygame.locals import K_p
    from pygame.locals import K_q
    from pygame.locals import K_r
    from pygame.locals import K_s
    from pygame.locals import K_v
    from pygame.locals import K_w
    from pygame.locals import K_x
    from pygame.locals import K_z
    from pygame.locals import K_MINUS
    from pygame.locals import K_EQUALS

except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')


# def game_loop():
#     pygame.init()
#     pygame.font.init()
#     world = None

#     try:
#         # client = carla.Client(args.host, args.port)
#         # client.set_timeout(2.0)

#         display = pygame.display.set_mode(
#             ([700, 400]),
#             pygame.HWSURFACE | pygame.DOUBLEBUF)
#         display.fill((0,0,0))
#         pygame.display.flip()

#         hud = HUD(700, 400)
#         world = World(client.get_world(), hud, args)
#         controller = KeyboardControl(world, args.autopilot)

#         clock = pygame.time.Clock()
#         while True:
#             clock.tick_busy_loop(60)
#             if controller.parse_events(client, world, clock):
#                 return
#             world.tick(clock)
#             world.render(display)
#             pygame.display.flip()


#     finally:

#         # if (world and world.recording_enabled):
#         #     client.stop_recorder()
#         #
#         # if world is not None:
#         #     world.destroy()

#         pygame.quit()

def main():

    #game_loop()

    actor_list = []

    try:
        # First of all, we need to create the client that will send the requests
        # to the simulator. Here we'll assume the simulator is accepting
        # requests in the localhost at port 2000.
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)

        # # Getting world and actors
        world = client.get_world()
        #world = client.load_world('Town01')
        # actors = world.get_actors()

        # Get blueprint blueprint_library
        blueprint_library = world.get_blueprint_library()

        # Spawning Vehicel in Carla
        vehicle_bp = random.choice(blueprint_library.filter('vehicle.tesla.*'))
        transform = carla.Transform(carla.Location(x=-50, y=2, z=3), carla.Rotation())
        vehicle = world.spawn_actor(vehicle_bp, transform)
        #vehicel.set_autopilot(True)
        #vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer = 0.0))
        actor_list.append(vehicle)


        # Mounting Camera on the Vehicel
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', '1920')
        camera_bp.set_attribute('image_size_y', '1080')
        camera_bp.set_attribute('fov', '110')
        camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
        camera.listen(lambda image: image.save_to_disk('output/%06d.png' %image.frame_number))
        actor_list.append(camera)

        pygame.init()

        keys = pygame.key.get_pressed()
        # if keys[K_ESCAPE]:
        #     return True

        control = vehicle.get_control()

        control.throttle = 0

        if keys[K_y]:
            control.throttle =1
            control.reverse = False

        elif keys[K_h]:
            control.throttle =1
            control.reverse = True

        if keys[K_g]:
            control.steer = max(-1., min(control.steer - 0.05,0))

        elif keys[K_j]:
            control.steer = min(1. , max(control.steer + 0.05, 0))
        
        else:
            control.steer = 0 

        control.hand_brake = keys[K_SPACE]

        vehicle.apply_control(control)
        return True

        time.sleep(120)

        #print(actor_list)

        # while keys[K_i] == False:
        #     if keys[K_UP] or keys[K_w]:
        #         print('It works')
        #         vehicle.apply_control(carla.VehicleControl(throttle=throttle + 0.01))
        #         #vehicle._control.throttle = min(vehicle._control.throttle + 0.01, 1)
        #     else:
        #         vehicle.apply_control(carla.VehicleControl(throttle=0))
                #vehicle._control.throttle = 0.0
            # if keys[K_DOWN] or keys[K_s]:
            #     vehicle._control.brake = min(vehicle._control.brake + 0.2, 1)
            # else:
            #     vehicle._control.brake = 0
            #
            # steer_increment = 5e-4 * milliseconds
            # if keys[K_LEFT] or keys[K_a]:
            #     if vehicle._steer_cache > 0:
            #         vehicle._steer_cache = 0
            #     else:
            #         vehicle._steer_cache -= steer_increment
            # elif keys[K_RIGHT] or keys[K_d]:
            #     if vehicle._steer_cache < 0:
            #         vehicle._steer_cache = 0
            #     else:
            #         vehicle._steer_cache += steer_increment
            # else:
            #     vehicle._steer_cache = 0.0
            # vehicle._steer_cache = min(0.7, max(-0.7, vehicle._steer_cache))
            # vehicle._control.steer = round(vehicle._steer_cache, 1)
            # vehicle._control.hand_brake = keys[K_SPACE]

        # Deciding simulation time.
        #time.sleep(120)
        
        

    finally:
        for actor in actor_list:
            actor.destroy()
            print('All clear')

# if __name__ == '__main__':
#     main()
if __name__ =='__main__':
    main()
