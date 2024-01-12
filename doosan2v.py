from DEPTH_HOW import DepthCamera
import socket
import time
import stacking_algorithm as SA
import storage as ST
import barcode_scanner as BARC

# =========== ROBOT CONN & INIT  ============= #
z1 = {'s': 204.1, 'm': 245.8, 'l': 328.8, 'xl': 379.0, 'unknown': 661.1}
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
robot_address = ('192.168.137.100', 9225)
sock.connect(robot_address)
#sock.sendall(b"movel(posx(559.0, -56.8, 661.1, 169.3, 180.0, -10.7), v=200, a=200)")  #HOME POS NR 1
sock.sendall(b"movel(posx(559.0, -56.8, 661.0, 139.4, 180.0, -42.6), v=1000, a=2000)")  #HOME POS NR 2
Buf = ST.fill_buf()
# ==================================== #

# def check_position():
#     if SA.matrix[0] >= SA.matrix[1] : return 100
#     elif SA.matrix[0] < SA.matrix[1] : return -100


def scale_coordinate(pixel_coord, classification):
    # Given coordinates
    real_world_start = {'s': 30, 'm': 47, 'l': -10, 'xl': 35, 'unknown': 0}
    real_world_end = {'s': -107, 'm': -190, 'l': -137, 'xl': -120, 'unknown': 1}
    # Given pixel coordinates
    pixel_start = {'s': 290, 'm': 265, 'l': 284, 'xl': 240, 'unknown': 0}
    pixel_end = {'s': 365, 'm': 425, 'l': 409, 'xl': 390, 'unknown': 1}

    # Calculate the scaling factor for x-values
    x_scaling_factor = (real_world_end[classification] - real_world_start[classification]) / (pixel_end[classification] - pixel_start[classification])

    # Function to scale x-coordinate
    def scale_x_coordinate(x, scaling_factor):
        scaled_x = (x - pixel_start[classification]) * scaling_factor + real_world_start[classification]
        return scaled_x

    # Check if the pixel_coord is within the given range
    if pixel_coord < pixel_start[classification] or pixel_coord > pixel_end[classification]:
        return "0"

    # Scale the input pixel coordinate
    scaled_x = scale_x_coordinate(pixel_coord, x_scaling_factor)

    return scaled_x


def move_robot_pallet(sock, boxcount, Coords_val, size, classification):
    global status
    global yy
    camera = DepthCamera()
    place = SA.coordinates(Coords_val, size, Height)
    print(f'place: {place}')
    x, y, z = place[boxcount]
    try:
        data = camera.get_data()
        if data:
            classification, _,_,_ = data
            if classification != wantedSize:
                move_robot_conveyor(sock)
                return place, boxcount
            print(f"Classification: {classification}")

            # =========== MOVE BACK TO MAKE SURE ONLY DETECT 1 BOX =============#
            move = {'s':(347.8, -56.8, 661.0, 140.5, 180.0, -41.5) , 'm':(363.0, -56.8, 661.0, 138.7, 180.0, -43.3) ,
                    'l': (401.4, -56.8, 661.0, 139.5, 180.0, -42.5), 'xl':(498.4, -56.8, 661.0, 138.6, 180.0, -43.4),
                    'unknown': (559.0, -56.8, 661.0, 139.4, 180.0, -42.6)}
            sock.sendall(f"movel(posx{move[classification]}, v=2000, a=2000)".encode())
            time.sleep(1)
            _, centroid_x, centroid_y, distance = camera.get_data()
            print(f"Centroid Coordinates (x, y): ({centroid_x}, {centroid_y})")
            print(f"Distance: {distance} meters")

            # =========== SCALE VISION COORD TO REAL WORLD =============#
            scaled_result = scale_coordinate(centroid_x, classification)
            yy = scaled_result
            print(f"Scaled coordinate for yy  {yy}")
            # =========== ROBOT HOME POS MVT =============#
        #sock.sendall(b"movel(posx(559.0, -56.8, 661.1, 169.3, 180.0, -10.7), v=1000, a=1000)")
        sock.sendall(b"movel(posx(559.0, -56.8, 661.0, 139.4, 180.0, -42.6), v=1000, a=2000)")
        zz = z1[size]
        print(yy)
        sock.sendall(
            f"movel(posx(547.0, {yy}, {zz}, 168.5, -177.8, -11.9), v=1000, a=1000)".encode())
        time.sleep(.1)
        status = 1
        print(f"stattt: {status}")
        if status == 1:
            time.sleep(2)
            sock.sendall(b"set_digital_output(1, ON)")
            time.sleep(2)
            sock.sendall(b"movel(posx(559.0, -56.8, 750, 169.3, 180.0, -10.7), v=1000, a=1000)")
            time.sleep(1)
            if classification == 'xl':
                sock.sendall(b"movej(posj(100, 15.8, 75.8, 181.1, -84.3, -9.2), v=100, a=100)")
                time.sleep(2)
                if z > 500:
                    sock.sendall(
                        f"movel(posx(-161.6, 719.1, {z + 150}, 136.9, 175.8, -174.1), v=1000, a=1000)".encode())
                    time.sleep(2)
                sock.sendall(
                    f"movel(posx({x + 100}, {y + 100}, {z + 100}, 52.4, 180, 139.3), v=1000, a=1000)".encode())
                time.sleep(2)
                sock.sendall(
                    f"movel(posx({x + 10}, {y + 10}, {z + 10}, 158.4, -180.0, -112.0), v=1000, a=1000)".encode())
                time.sleep(2)
                sock.sendall(
                    f"movel(posx({x}, {y}, {z}, 158.4, -180.0, -112.0), v=1000, a=1000)".encode())
                time.sleep(2)
                sock.sendall(b"set_digital_output(1, OFF)")
                time.sleep(2)
                sock.sendall(
                    f"movel(posx({x}, {y}, {z + 25}, 158.4, -180.0, -112.0), v=100, a=100)".encode())

            elif classification == size:
                sock.sendall(b"movej(posj(100, 15.8, 75.8, 181.1, -84.3, -9.2), v=100, a=100)")
                time.sleep(2)
                if z > 500:
                    sock.sendall(
                        f"movel(posx(-161.6, 719.1, {z + 150}, 136.9, 175.8, -174.1), v=1000, a=1000)".encode())
                    time.sleep(2)
                sock.sendall(
                    f"movel(posx({x + 100}, {y + 100}, {z + 100}, 66.5, -180, -113.1), v=1000, a=1000)".encode())
                time.sleep(2)
                sock.sendall(
                    f"movel(posx({x+ 50}, {y + 50}, {z + 10}, 66.5, -180, -113.1), v=1000, a=1000)".encode())
                time.sleep(2)
                sock.sendall(
                    f"movel(posx({x}, {y}, {z}, 66.5, -180, -113.1), v=1000, a=1000)".encode())
                time.sleep(2)
                sock.sendall(b"set_digital_output(1, OFF)")
                time.sleep(2)
                sock.sendall(
                    f"movel(posx({x}, {y}, {z + 25}, 66.5, -180, -113.1), v=100, a=100)".encode())
            # time.sleep(2)
            # sock.sendall(b"movel( posx(-518.1, 69.4, 600, 168.8, -178.0, -11.6), v=1000, a=2000)") #SAFE PLACE NR 1
            time.sleep(1)
            if z > 500:
                sock.sendall(
                    f"movel(posx(-420.0, 605.8, {z + 150}, 136.9, 175.8, -174.1), v=1000, a=1000)".encode())
                time.sleep(2)
            sock.sendall(b"movel(posx(-135.9, 609.5, 600,  168.8, -178.0, -11.6), v=1000, a=1000)") #SAFE PLACE NR 2
            time.sleep(2)
            status = 0
            #sock.sendall(b"movel(posx(559.0, -56.8, 661.1, 169.3, 180.0, -10.7), v=1000, a=1000)") #HOME
            sock.sendall(b"movel(posx(559.0, -56.8, 661.0, 139.4, 180.0, -42.6), v=1000, a=2000)")
            time.sleep(4)
            boxcount = boxcount + 1
        return place, boxcount

    except KeyboardInterrupt:
        pass
    finally:
        camera.stop()


def move_robot_conveyor(sock):
    global status
    global yy

    # =========== CALL VISION =============#
    camera = DepthCamera()
    try:
        data = camera.get_data()
        if data:
            classification, _, _, _ = data
            print(f"Classification: {classification}")

            # =========== MOVE BACK TO MAKE SURE ONLY DETECT 1 BOX =============#
            move = {'s': (347.8, -56.8, 661.0, 140.5, 180.0, -41.5), 'm': (363.0, -56.8, 661.0, 138.7, 180.0, -43.3),
                    'l': (401.4, -56.8, 661.0, 139.5, 180.0, -42.5), 'xl': (498.4, -56.8, 661.0, 138.6, 180.0, -43.4),
                    'unknown' : (559.0, -56.8, 661.0, 139.4, 180.0, -42.6)}
            sock.sendall(f"movel(posx{move[classification]}, v=2000, a=2000)".encode())
            _, centroid_x, centroid_y, distance = camera.get_data()
            print(f"Centroid Coordinates (x, y): ({centroid_x}, {centroid_y})")
            print(f"Distance: {distance} meters")

            # =========== SCALE VISION COORD TO REAL WORLD =============#
            scaled_result = scale_coordinate(centroid_x, classification)
            yy = scaled_result
            print(f"Scaled coordinate for yy  {yy}")

            # =========== ROBOT HOME POS MVT =============#
            #sock.sendall(b"movel(posx(559.0, -56.8, 661.1, 169.3, 180.0, -10.7), v=200, a=200)")
            sock.sendall(b"movel(posx(559.0, -56.8, 661.0, 139.4, 180.0, -42.6), -44.5), v=1000, a=2000)")
            time.sleep(1)
            z2 = {'s': 200.5, 'm': 282.5, 'l': 313, 'xl': 382.5, 'unknown':661.1}
            zz = z1[classification]
            zzz = z2[classification]

            # =========== MVT FOR XL =============#
            if classification == "xl":
                print(yy)
                time.sleep(1)
                sock.sendall(
                    f"movel(posx(569.3, {yy}, {zz}, 145.9, -178.3, -34.3), v=1000, a=2000)".encode())  ### get big
                time.sleep(1)
                status = 3
                print(f"stattt: {status}")
                if status == 3:
                    time.sleep(1)
                    sock.sendall(b"set_digital_output(1, ON)")
                    time.sleep(1)
                    sock.sendall(b"movel(posx(559.0, -56.8, 650, 169.3, 180.0, -10.7), v=1000, a=2000)")
                    time.sleep(1)
                    sock.sendall(b"movel(posx(630.6, 587.0, 650, 177.7, -173.2, -3.1), v=1000, a=2000)")
                    time.sleep(1)
                    sock.sendall(f"movel(posx(630.7, 582.7, {zzz}, 172.9, -173.5, -8.1), v=1000, a=2000)".encode())
                    time.sleep(1)
                    sock.sendall(b"set_digital_output(1, OFF)")
                    time.sleep(1)
                    status = 0
                    sock.sendall(b"movel(posx(630.7, 582.7, 661, 172.9, -173.5, -8.1), v=1000, a=2000)")
                    time.sleep(1)
                    #sock.sendall(b"movel(posx(559.0, -56.8, 661.1, 169.3, 180.0, -10.7), v=1000, a=2000)")
                    sock.sendall(b"movel(posx(559.0, -56.8, 661.0, 139.4, 180.0, -42.6), v=1000, a=2000)")

            # =========== MVT FOR SMALL MEDIUM LARGE =============#
            elif classification != "unknown":
                print(yy)
                time.sleep(1)
                sock.sendall(
                    f"movel(posx(547.0, {yy}, {zz}, 168.5, -177.8, -11.9), v=1000, a=2000)".encode())  ### get small
                time.sleep(1)
                status = 1
                print(f"stattt: {status}")
                if status != 0:
                    time.sleep(1)
                    sock.sendall(b"set_digital_output(1, ON)")
                    time.sleep(1)
                    sock.sendall(b"movel(posx(559.0, -56.8, 650, 169.3, 180.0, -10.7), v=1000, a=2000)")
                    time.sleep(1)
                    sock.sendall(b"movel(posx(630.6, 587.0, 650, 177.7, -173.2, -3.1), v=1000, a=2000)")
                    time.sleep(1)
                    sock.sendall(f"movel(posx(630.7, 582.7, {zzz}, 66.5, -180, -113.1), v=1000, a=2000)".encode())
                    time.sleep(1)
                    sock.sendall(b"set_digital_output(1, OFF)")
                    time.sleep(1)
                    status = 0
                    sock.sendall(b"movel(posx(630.7, 582.7, 661, 172.9, -173.5, -8.1), v=1000, a=2000)")
                    time.sleep(1)
                    #sock.sendall(b"movel(posx(559.0, -56.8, 661.1, 169.3, 180.0, -10.7), v=1000, a=2000)")
                    sock.sendall(b"movel(posx(559.0, -56.8, 661.0, 139.4, 180.0, -42.6), v=1000, a=2000)")

            elif classification == "unknown":
                time.sleep(1)
                status = 0
                #sock.sendall(b"movel(posx(559.0, -56.8, 661.1, 169.3, 180.0, -10.7), v=200, a=200)")
                sock.sendall(b"movel(posx(559.0, -56.8, 661.0, 139.4, 180.0, -42.6), v=1000, a=2000)")

    except KeyboardInterrupt:
        pass
    finally:
        camera.stop()

def run():
    boxcount = 0
    status = 0
    yy = 0
    while True:
        camera = DepthCamera()
        classification, _, _, _ = camera.get_data()
        if classification != 'unknown':
            if ST.buf_size == len(ST.Buf):
                global wantedSize
                _, wantedSize = ST.take_buf(Buf)
            print(wantedSize)
            if classification == wantedSize:
                global Height
                x, Coords_val, Height = SA.place(size=wantedSize)
                coords = SA.coordinates(Coords_val=Coords_val, size=wantedSize, Height=Height)
                print(f'coords:{coords}')
                SA.give_coords(coords)
                if classification == wantedSize:
                    if classification == 'xl':
                        loop = 3
                    else:
                        loop = 4
                    while True:
                        if classification != 'unknown':
                            #BARC.main()
                            _,boxcount = move_robot_pallet(sock, boxcount, Coords_val, wantedSize, classification)
                        if boxcount == loop:
                            boxcount = 0
                            break
                        if Height >= 580:
                            break
                    ST.refill_buf()
            else:
                move_robot_conveyor(sock)


if __name__ == '__main__':
    run()
