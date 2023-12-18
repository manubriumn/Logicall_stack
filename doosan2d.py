from DEPTH_HOW import DepthCamera
import socket
import time
import stacking_algorithm as SA
import storage as ST

status = 0
xx = 0
boxcount = 0

def scale_coordinate(pixel_coord):
    # Given coordinates
    real_world_start = -4
    real_world_end = -76.0

    # Given pixel coordinates
    pixel_start = 300
    pixel_end = 360

    # Calculate the scaling factor for x-values
    x_scaling_factor = (real_world_end - real_world_start) / (pixel_end - pixel_start)

    # Function to scale x-coordinate
    def scale_x_coordinate(x, scaling_factor):
        scaled_x = (x - pixel_start) * scaling_factor + real_world_start
        return scaled_x

    # Check if the pixel_coord is within the given range
    if pixel_coord < pixel_start or pixel_coord > pixel_end:
        return "0"

    # Scale the input pixel coordinate
    scaled_x = scale_x_coordinate(pixel_coord, x_scaling_factor)

    return scaled_x

def move_robot_pallet(sock, boxcount, Coords_val, size, classification):
    global status
    global xx
    

    place = SA.coordinates(Coords_val, size, Height)
    print(f'place: {place}')
    x, y, z = place[boxcount]


    camera = DepthCamera()

    try:
        for i in range(1):
            data = camera.get_data()
            if data:
                classification, centroid_x, centroid_y, distance = data

                print(f"Classification: {classification}")
                print(f"Centroid Coordinates (x, y): ({centroid_x}, {centroid_y})")
                print(f"Distance: {distance} meters")

                # =========== SCALE VISION COORD TO REAL WORLD =============#
                scaled_result = scale_coordinate(centroid_x)
                xx = scaled_result
                print(f"Scaled coordinate for xx  {xx}")
                # =========== ROBOT HOME POS MVT =============#
            sock.sendall(b"movel(posx(559.0, -56.8, 661.1, 169.3, 180.0, -10.7), v=200, a=200)")
            time.sleep(2)
            if classification == size:
                z1 = {'s': 204.1, 'm': 245.8, 'xl': 379.0}
                zz = z1[size]
                print(xx)
                time.sleep(2)
                sock.sendall(
                    f"movel(posx(547.0, {xx}, {zz}, 168.5, -177.8, -11.9), v=200, a=200)".encode())  ### get small
                time.sleep(3)
                status = 1
                print(f"stattt: {status}")
                if status == 1:
                    time.sleep(2)
                    sock.sendall(b"set_digital_output(1, ON)")
                    time.sleep(2)
                    sock.sendall(b"movel(posx(559.0, -56.8, 400, 169.3, 180.0, -10.7), v=200, a=200)")
                    time.sleep(3)
                    sock.sendall(b"movej(posj(121.9, 15.8, 75.8, 181.1, -84.3, -9.2), v=40, a=40)")
                    time.sleep(4)
                    sock.sendall(
                        f"movel(posx({x}, {y}, {z+zz}, 168.5, -177.8, -11.9), v=200, a=200)".encode())
                    time.sleep(4)
                    sock.sendall(
                        f"movel(posx({x}, {y}, {z}, 168.5, -177.8, -11.9), v=200, a=200)".encode())
                    time.sleep(4)
                    sock.sendall(b"set_digital_output(1, OFF)")
                    time.sleep(4)
                    sock.sendall(
                        f"movel(posx({x}, {y}, {z + zz}, 168.5, -177.8, -11.9), v=200, a=200)".encode())
                    time.sleep(4)
                    sock.sendall(b"movel(posx(-135.9, 609.5, 509.1,  168.8, -178.0, -11.6), v=200, a=200)")
                    time.sleep(4)
                    status = 0
                    sock.sendall(b"movel(posx(559.0, -56.8, 661.1, 169.3, 180.0, -10.7), v=300, a=300)")
                    time.sleep(9)
                    boxcount = boxcount +1

                if classification == "unknown":
                    boxcount = boxcount -1

            return place, boxcount

    except KeyboardInterrupt:
        pass
    finally:
        camera.stop()

def move_robot_conveyor(sock):
    global status
    global xx

    # =========== CALL VISION =============#
    camera = DepthCamera()
    try:
        data = camera.get_data()
        if data:
            classification, centroid_x, centroid_y, distance = data

            print(f"Classification: {classification}")
            print(f"Centroid Coordinates (x, y): ({centroid_x}, {centroid_y})")
            print(f"Distance: {distance} meters")



            # =========== SCALE VISION COORD TO REAL WORLD =============#
            scaled_result = scale_coordinate(centroid_x)
            xx = scaled_result
            print(f"Scaled coordinate for xx  {xx}")

            # =========== ROBOT HOME POS MVT =============#
            sock.sendall(b"movel(posx(559.0, -56.8, 661.1, 169.3, 180.0, -10.7), v=200, a=200)")
            time.sleep(4)

            # =========== MVT FOR SMALL =============#
            if classification == "s" and not (-2 <= xx <= 2):
                print(xx)
                time.sleep(1)
                sock.sendall(
                    f"movel(posx(547.0, {xx}, 204.1, 168.5, -177.8, -11.9), v=200, a=200)".encode())  ### get small
                time.sleep(2)
                status = 1
                print(f"stattt: {status}")
                if status == 1:
                    time.sleep(2)
                    sock.sendall(b"set_digital_output(1, ON)")
                    time.sleep(3)
                    sock.sendall(b"movel(posx(559.0, -56.8, 650.1, 169.3, 180.0, -10.7), v=1000, a=1000)")
                    time.sleep(2)
                    sock.sendall(b"movel(posx(630.6, 587.0, 500.4, 177.7, -173.2, -3.1), v=1000, a=1000)")
                    time.sleep(2)
                    sock.sendall(b"movel(posx(630.6, 587.0, 224.4, 177.7, -173.2, -3.1), v=200, a=200)")
                    time.sleep(3)
                    sock.sendall(b"movel(posx(630.7, 582.7, 200.5, 172.9, -173.5, -8.1), v=200, a=200)")
                    time.sleep(3)
                    sock.sendall(b"set_digital_output(1, OFF)")
                    time.sleep(3)
                    status = 0
                    sock.sendall(b"movel(posx(559.0, -56.8, 661.1, 169.3, 180.0, -10.7), v=1000, a=2000)")

            # =========== MVT FOR MEDIUM =============#
            elif classification == "m" and not (-2 <= xx <= 2):
                print(xx)
                time.sleep(1)
                sock.sendall(
                    f"movel(posx(545.8, {xx}, 245.8, 151.3, -176.5, -28.9), v=200, a=200)".encode())  ### get medium
                time.sleep(2)
                status = 2
                print(f"stattt: {status}")
                if status == 2:
                    time.sleep(2)
                    sock.sendall(b"set_digital_output(1, ON)")
                    time.sleep(3)
                    sock.sendall(b"movel(posx(559.0, -56.8, 650.1, 169.3, 180.0, -10.7), v=1000, a=1000)")
                    time.sleep(2)
                    sock.sendall(b"movel(posx(630.6, 587.0, 500.4, 177.7, -173.2, -3.1), v=1000, a=1000)")
                    time.sleep(2)
                    sock.sendall(b"movel(posx(630.6, 587.0, 324.4, 177.7, -173.2, -3.1), v=200, a=200)")
                    time.sleep(3)
                    sock.sendall(b"movel(posx(630.7, 582.7, 282.5, 172.9, -173.5, -8.1), v=200, a=200)")
                    time.sleep(3)
                    sock.sendall(b"set_digital_output(1, OFF)")
                    time.sleep(3)
                    status = 0
                    sock.sendall(b"movel(posx(559.0, -56.8, 661.1, 169.3, 180.0, -10.7), v=1000, a=2000)")

            # =========== MVT FOR BIG =============#
            elif classification == "xl" and not (-2 <= xx <= 2):
                print(xx)
                time.sleep(3)
                sock.sendall(
                    f"movel(posx(569.3, {xx}, 379.0, 145.9, -178.3, -34.3), v=60, a=60)".encode())  ### get big
                time.sleep(5)
                status = 3
                print(f"stattt: {status}")
                if status == 3:
                    time.sleep(5)
                    sock.sendall(b"set_digital_output(1, ON)")
                    time.sleep(6)
                    sock.sendall(b"movel(posx(559.0, -56.8, 650.1, 169.3, 180.0, -10.7), v=80, a=80)")
                    time.sleep(7)
                    sock.sendall(b"movel(posx(630.6, 587.0, 424.4, 177.7, -173.2, -3.1), v=80, a=80)")
                    time.sleep(8)
                    sock.sendall(b"movel(posx(630.7, 582.7, 382.5, 172.9, -173.5, -8.1), v=80, a=80)")
                    time.sleep(9)
                    sock.sendall(b"set_digital_output(1, OFF)")
                    time.sleep(10)
                    status = 0
                    sock.sendall(b"movel(posx(559.0, -56.8, 661.1, 169.3, 180.0, -10.7), v=80, a=80)")

            elif classification == "unknown":
                time.sleep(5)
                status = 0
                sock.sendall(b"movel(posx(559.0, -56.8, 661.1, 169.3, 180.0, -10.7), v=200, a=200)")

    except KeyboardInterrupt:
        pass
    finally:
        camera.stop()

# =========== ROBOT CONN =============#
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
robot_address = ('192.168.137.100', 9225)
sock.connect(robot_address)

while True:
    Buf = ST.fill_buf()
    camera = DepthCamera()
    classification, _, _, _ = camera.get_data()
    if classification != 'unknown':
        _, wantedSize = ST.take_buf(Buf)
        print(wantedSize)
        time.sleep(5)
        x, Coords_val, Height = SA.place(size=wantedSize)
        coords = SA.coordinates(Coords_val=Coords_val, size=wantedSize, Height=Height)
        print(f'coords:{coords}')
        time.sleep(5)
        SA.give_coords(coords)
        loop = 4
        if classification == wantedSize:
            if classification == 'xl':
                loop = 3
            for boxcount in range(loop):
                _, boxcount = move_robot_pallet(sock, boxcount, Coords_val, wantedSize, classification)
                if boxcount == 3:
                    boxcount = 0
        else:
            time.sleep(4)
            move_robot_conveyor(sock)
