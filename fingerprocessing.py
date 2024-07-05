import cv2
import mediapipe as mp
import inspect
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For static images:
IMAGE_FILES = []
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:
  for idx, file in enumerate(IMAGE_FILES):
    # Read an image, flip it around y-axis for correct handedness output (see
    # above).
    image = cv2.flip(cv2.imread(file), 1)
    # Convert the BGR image to RGB before processing.
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Print handedness and draw hand landmarks on the image.
    print('Handedness:', results.multi_handedness)
    if not results.multi_hand_landmarks:
      continue
    image_height, image_width, _ = image.shape
    annotated_image = image.copy()
    for hand_landmarks in results.multi_hand_landmarks:
      print('hand_landmarks:', hand_landmarks)
      print(
          f'Index finger tip coordinates: (',
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
      )
      mp_drawing.draw_landmarks(
          annotated_image,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style())
    cv2.imwrite(
        '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
    # Draw hand world landmarks.
    if not results.multi_hand_world_landmarks:
      continue
    for hand_world_landmarks in results.multi_hand_world_landmarks:
      mp_drawing.plot_landmarks(
        hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)


def avg_coordinate(hand_coordinates=list, x=int):
    try:
        last_hand_coordinates = hand_coordinates[-x:]
    except:
       print("Not enough coordinates to average")
       return None
    
    avgr0 = 0
    avgr1 = 0
    avgr2 = 0
    avgr3 = 0
    avgr4 = 0
    avgr5 = 0
    avgl0 = 0
    avgl1 = 0
    avgl2 = 0
    avgl3 = 0
    avgl4 = 0
    avgl5 = 0

    for y in last_hand_coordinates:
        try:
            avgr0 += y.get("r0")
            avgr1 += y.get("r1")
            avgr2 += y.get("r2")
            avgr3 += y.get("r3")
            avgr4 += y.get("r4")
            avgr5 += y.get("r5")
            avgl0 += y.get("l0")
            avgl1 += y.get("l1")
            avgl2 += y.get("l2")
            avgl3 += y.get("l3")
            avgl4 += y.get("l4")
            avgl5 += y.get("l5")
            
            r0 = avgr0/x
            r1 = avgr1/x
            r2 = avgr2/x
            r3 = avgr3/x
            r4 = avgr4/x
            r5 = avgr5/x
            l0 = avgl0/x
            l1 = avgl1/x
            l2 = avgl2/x
            l3 = avgl3/x
            l4 = avgl4/x
            l5 = avgl5/x
            return {"r0": r0, "r1": r1, "r2": r2, "r3": r3, "r4": r4, "r5": r5, "l0": l0, "l1": l1, "l2": l2, "l3": l3, "l4": l4, "l5": l5}
        except:
           print("fail")
           return None
    
#track hand coords over time
hand_coordinates = []
# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image_height, image_width, _ = image.shape
    

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
            #landmark coordinates - z coordinates

            #require both hands visible to type.
            try:
                hand_index={}
                results.multi_handedness[0]
                results.multi_handedness[1]
            except:
                print("Both hands need to be visible")
            else:
                first_hand_string = str(results.multi_handedness[0].__getstate__().get('serialized'))
                second_hand_string = str(results.multi_handedness[1].__getstate__().get('serialized'))

                #makes dictionary storing positions of each finger at a time
                if first_hand_string[-3:] == "ft'":
                    if first_hand_string[-3:] == "ft'":
                        hand_index['r0'] = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * image_height
                        hand_index['r1'] = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * image_height
                        hand_index['r2'] = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height
                        hand_index['r3'] = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * image_height
                        hand_index['r4'] = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * image_height
                        hand_index['r5'] = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * image_height
                    if second_hand_string[-3:] == "ht'":
                        hand_index['l0'] = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * image_height
                        hand_index['l1'] = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * image_height
                        hand_index['l2'] = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height
                        hand_index['l3'] = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * image_height
                        hand_index['l4'] = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * image_height
                        hand_index['l5'] = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * image_height
                else:
                    if first_hand_string[-3:] == "ht'":
                        hand_index['r0'] = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * image_height
                        hand_index['r1'] = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * image_height
                        hand_index['r2'] = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height
                        hand_index['r3'] = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * image_height
                        hand_index['r4'] = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * image_height
                        hand_index['r5'] = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * image_height
                    if second_hand_string[-3:] == "ft'":
                        hand_index['l0'] = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * image_height
                        hand_index['l1'] = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * image_height
                        hand_index['l2'] = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height
                        hand_index['l3'] = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * image_height
                        hand_index['l4'] = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * image_height
                        hand_index['l5'] = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * image_height

                #adds indexes to a list of hand coordinates over time
                hand_coordinates.append(hand_index)
                last_two_hand_coordinates = avg_coordinate(hand_coordinates, 50)
                print(last_two_hand_coordinates)
                print("\n"+str(hand_index))


        
        
        
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
