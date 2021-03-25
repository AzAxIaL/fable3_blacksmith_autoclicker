import numpy as np
import cv2
from PIL import ImageGrab
from time import time, sleep
from directKeys import PressKey, ReleaseKey, KEY_1, KEY_2

banner = """
╔═╗┌─┐┌┐ ┬  ┌─┐                                                 
╠╣ ├─┤├┴┐│  ├┤                                                  
╚  ┴ ┴└─┘┴─┘└─┘                                                 
╔╗ ┬  ┌─┐┌─┐┬┌─┌─┐┌┬┐┬┌┬┐┬ ┬  ╔═╗┬ ┬┌┬┐┌─┐   ╔═╗┬  ┬┌─┐┬┌─┌─┐┬─┐
╠╩╗│  ├─┤│  ├┴┐└─┐││││ │ ├─┤  ╠═╣│ │ │ │ │───║  │  ││  ├┴┐├┤ ├┬┘
╚═╝┴─┘┴ ┴└─┘┴ ┴└─┘┴ ┴┴ ┴ ┴ ┴  ╩ ╩└─┘ ┴ └─┘   ╚═╝┴─┘┴└─┘┴ ┴└─┘┴└─

Author: AzAxIaL
Website: https://github.com/AzAxIaL
Version: 1.0
"""


def key_press(key):
    """Sends a keystroke"""
    PressKey(key)
    sleep(0.05)
    ReleaseKey(key)


def main():
    """
    Screenshots are taken until a sequence is detected.
    After that, the marker is tracked to the positions of the blocks in the sequence.
    When the marker reaches a block, it sends a key press corresponding to the color.
    The process adapts to the increasing difficulty.
    """

    # Outputs the sequence and key presses when enabled
    console_output = True

    # Screen coords for blacksmith bar
    blacksmith_coords = [280, 870, 1650, 1000]

    # Template images of the numbers
    blue_2 = cv2.imread('2b.png', 0)
    green_1 = cv2.imread('1b.png', 0)
    marker_blue_2 = cv2.imread('2s.png', 0)
    marker_green_1 = cv2.imread('1s.png', 0)

    # Threshold for image similarity
    threshold = 0.7

    # Time limit (in secs) to wait to detect a sequence before auto-exiting
    limit = 20
    previous_time = time()

    # Dimensions of templates
    w_bb, h_bb = blue_2.shape[::-1]
    w_bg, h_bg = green_1.shape[::-1]
    w_sb, h_sb = marker_blue_2.shape[::-1]
    w_sg, h_sg = marker_green_1.shape[::-1]

    print(banner)
    if console_output: print("[!] Waiting for sequence...")

    while True:

        # If the time limit has been reached, exit the script.
        if (time() - previous_time) > limit:
            print("[X] No sequence detected. Exiting...")
            sleep(1)
            break

        # Grab screenshot
        img_rgb = np.array(ImageGrab.grab(bbox=blacksmith_coords))
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        # Match templates to gray image
        res_b = cv2.matchTemplate(img_gray, blue_2, cv2.TM_CCOEFF_NORMED)
        res_g = cv2.matchTemplate(img_gray, green_1, cv2.TM_CCOEFF_NORMED)

        # Initialize the sequence list
        seq = []

        # Locate all blue templates in the screenshot
        loc_b = np.where(res_b >= threshold)
        for pt in zip(*loc_b[::-1]):
            # Add to sequence
            seq.append([2, pt[0]])

        # Locate all green templates in the screenshot
        loc_g = np.where(res_g >= threshold)
        for pt in zip(*loc_g[::-1]):
            seq.append([1, pt[0]])

        # Sort the detected templates into order, removing any close neighbors
        if len(seq) > 0:
            final_seq = []
            prev_pos = 0
            seq_sort = sorted(seq, key=lambda i: i[1])
            for x in seq_sort:
                if x[1] - prev_pos > 10:
                    final_seq.append(x)
                prev_pos = x[1]
            if console_output: print("[+] Sequence Found:", ",".join(str(x[0]) for x in final_seq))

            # Reset the screenshot timer
            previous_time = time()

            # Reset the screenshot to focus only on the marker
            for m in final_seq:
                # Track only green
                if m[0] == 1:
                    keep_loop = True
                    # Loop until we encounter a green block
                    while keep_loop:
                        # Grab screenshot
                        img_rgb = np.array(ImageGrab.grab(bbox=blacksmith_coords))
                        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

                        # Locate green marker (should be only one, but this improves accuracy)
                        res_mg = cv2.matchTemplate(img_gray, marker_green_1, cv2.TM_CCOEFF_NORMED)
                        loc_mg = np.where(res_mg >= threshold)
                        for pt in zip(*loc_mg[::-1]):
                            # The x position in the sequence needs to be less than the marker position
                            if pt[0] > m[1]:
                                # As soon as the marker is in position, send key press
                                key_press(KEY_1)
                                if console_output: print("[+] Sending '1' key press")
                                keep_loop = False
                                break
                        else:
                            continue
                else:
                    keep_loop = True
                    while keep_loop:
                        img_rgb = np.array(ImageGrab.grab(bbox=blacksmith_coords))
                        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                        res_mb = cv2.matchTemplate(img_gray, marker_blue_2, cv2.TM_CCOEFF_NORMED)
                        loc_mb = np.where(res_mb >= threshold)
                        for pt in zip(*loc_mb[::-1]):
                            if pt[0] > m[1]:
                                # As soon as the marker is in position, send key press
                                key_press(KEY_2)
                                if console_output: print("[+] Sending '2' key press")
                                keep_loop = False
                                break
                        else:
                            continue
            # Sleep for a couple of seconds to give enough time to prepare next round.
            sleep(2)
            if console_output: print("[!] Waiting for sequence...")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("[X] Exiting...")
