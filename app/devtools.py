import functools
import queue
import threading
import time

import cv2
import vimba


class ImageRecorder:
    def __init__(self, cam: vimba.Camera, frame_queue: queue.Queue):
        self._cam = cam
        self._queue = frame_queue

    def __call__(self, cam: vimba.Camera, frame: vimba.Frame):
        # Place the image data as an opencv image and the frame ID into the queue
        self._queue.put((frame.as_opencv_image(), frame.get_id()))

        # Hand used frame back to Vimba so it can store the next image in this memory
        cam.queue_frame(frame)

    def _setup_software_triggering(self):
        # Always set the selector first so that folling features are applied correctly!
        self._cam.TriggerSelector.set('FrameStart')

        # optional in this example but good practice as it might be needed for hadware triggering
        self._cam.TriggerActivation.set('RisingEdge')

        # Make camera listen to Software trigger
        self._cam.TriggerSource.set('Software')
        self._cam.TriggerMode.set('On')

    def record_images(self, num_pics: int):
        # This method assumes software trigger is desired. Free run image acquisition would work
        # similarly to get higher fps from the camera
        with vimba.Vimba.get_instance():
            with self._cam:
                try:
                    self._setup_software_triggering()
                    self._cam.start_streaming(handler=self)
                    for i in range(num_pics):
                        print(i)
                        self._cam.TriggerSoftware.run()
                        # Delay between images can be adjusted or removed entirely
                        time.sleep(0.1)
                finally:
                    self._cam.stop_streaming()


def write_image(frame_queue: queue.Queue):
    while True:
        # Get an element from the queue.
        frame, id = frame_queue.get()
        cv2.imwrite(f'image_{id}.png', frame)
        # let the queue know we are finished with this element so the main thread can figure out
        # when the queue is finished completely
        frame_queue.task_done()


def main():
    num_pics = 60
    with vimba.Vimba.get_instance() as vmb:
        cams = vmb.get_all_cameras()

        frame_queue = queue.Queue()
        recorder = ImageRecorder(cam=cams[0], frame_queue=frame_queue)
        # Start a thread that runs write_image(frame_queue). Marking it as daemon allows the python
        # program to exit even though that thread is still running. The thread will then be stopped
        # when the program exits
        threading.Thread(target=functools.partial(write_image, frame_queue), daemon=True).start()

        recorder.record_images(num_pics=num_pics)
        frame_queue.join()


if __name__ == "__main__":
    main()