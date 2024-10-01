import groundlight
import cv2
from framegrab import FrameGrabber
import time

gl = groundlight.Groundlight()

detector_name = "Hard Hat"
detector_query = "Is everyone in the frame wearing proper PPE (proper PPE is a hard hat, answer Yes if no one is in frame)"

detector = gl.get_or_create_detector(detector_name, detector_query)

grabber = list(FrameGrabber.autodiscover().values())[0]

WAIT_TIME = 5
last_capture_time = time.time() - WAIT_TIME

while True:
    frame = grabber.grab()

    cv2.imshow('Video Feed', frame)
    key = cv2.waitKey(30)
 
    if key == ord('q'):  # 'q'キーが押されたら終了
        print("Quit key pressed")
        break
    elif key == ord('\r') or key == ord('\n'):  # 'Enter'キーが押されたか確認
        print("Enter key pressed")
        print(f'Asking question: {detector_query}')
        try:
            image_query = gl.submit_image_query(detector, frame)
            print(f'The answer is {image_query.result.label.value}')
        except Exception as e:
            print(f"Error occurred while submitting image query: {e}")
    elif key == ord('y'):  # 'y'キーが押されたか確認
        print("Y key pressed")
        label = 'YES'
        try:
            image_query = gl.ask_async(detector, frame, human_review="NEVER")
            gl.add_label(image_query, label)
            print(f'Adding label {label} for image query {image_query.id}')
        except Exception as e:
            print(f"Error occurred while adding label: {e}")
    elif key == ord('n'):  # 'n'キーが押されたか確認
        print("N key pressed")
        label = 'NO'
        try:
            image_query = gl.ask_async(detector, frame, human_review="NEVER")
            gl.add_label(image_query, label)
            print(f'Adding label {label} for image query {image_query.id}')
        except Exception as e:
            print(f"Error occurred while adding label: {e}")
            
    now = time.time()
    if last_capture_time + WAIT_TIME < now:
            last_capture_time = now

            print(f'Asking question: {detector_query}')
            image_query = gl.submit_image_query(detector, frame)
            print(f'The answer is {image_query.result.label.value}')

grabber.release()
cv2.destroyAllWindows()
