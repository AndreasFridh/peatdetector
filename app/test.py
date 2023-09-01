from vimba import *


def print_preamble():
    print('//////////////////////////////////////')
    print('/// Vimba API List Cameras Example ///')
    print('//////////////////////////////////////\n')


def print_camera(cam: Camera):
    print('/// Camera Name   : {}'.format(cam.get_name()))
    print('/// Model Name    : {}'.format(cam.get_model()))
    print('/// Camera ID     : {}'.format(cam.get_id()))
    print('/// Serial Number : {}'.format(cam.get_serial()))
    print('/// Interface ID  : {}\n'.format(cam.get_interface_id()))


def main():
    print_preamble()
    with Vimba.get_instance() as vimba:
        cams = vimba.get_all_cameras()

        print('Cameras found: {}'.format(len(cams)))

        for cam in cams:
            print_camera(cam)


if __name__ == '__main__':
    main()