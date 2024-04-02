import cv2
import numpy as np

def region(image):
    height, width = image.shape
    #isolate the gradients that correspond to the lane lines
    triangle = np.array([
                       [(300, height-200), (1020, 620), (width-500, height-200)]
                       ])
    #create a black image with the same dimensions as original image
    mask = np.zeros_like(image)
    #create a mask (triangle that isolates the region of interest in our image)
    mask = cv2.fillPoly(mask, triangle, 255)
    mask = cv2.bitwise_and(image, mask)
    return mask

def display_lines(image, lines, tx1, tx2):
    xi=xii=0
    
    lines_image = np.zeros_like(image)
    #make sure array isn't empty
    if lines is not None:
        x=0
        for line in lines:
            x+=1
            x1, y1, x2, y2 = line

            try:
                print(tx1,tx2)
                if x==1 and x1<700 and x1 > -50:
                    tx1 = x1, x2
                elif x==1 and (x1>700 or x1<-50):
                    x1,x2 = tx1
                if x==2 and x1<1700 and x1 > -1200:
                    tx2 = x1, x2
                elif x==2 and (x1>1700 or x1<-1200):
                    x1,x2 = tx2

                

                #draw lines on a black image
                cv2.line(lines_image, (x1, y1), (x2, y2), (0, 255, 0), 10)

                xi+=x1
                xii+=x2

            except cv2.error:
                pass
        xi = int(xi/2)
        xii = int(xii/2)
        if xi-xii>250:
            # Using cv2.putText() method 
            image = cv2.putText(image, 'Left Turn', (50,150), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 5, cv2.LINE_AA) 
        if xi-xii<-250:
            # Using cv2.putText() method 
            image = cv2.putText(image, 'Right Turn', (50,150), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 5, cv2.LINE_AA) 
        else:
            image = cv2.putText(image, 'Straight', (50,150), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 5, cv2.LINE_AA) 
            # Drawing the center line with the slope
        try:
            cv2.line(lines_image,(xi,y1),(xii,y2),(0,0,255),10)
        except cv2.error:
            image = cv2.putText(image, 'Left Turn', (50,150), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 5, cv2.LINE_AA) 
        

    return lines_image, tx1, tx2

def average(image, lines):
    left = []
    right = []

    if lines is not None:
        for line in lines:
            #print(line)
            x1, y1, x2, y2 = line.reshape(4)
            #fit line to points, return slope and y-int
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            #print(parameters)
            slope = parameters[0]
            y_int = parameters[1]
            #lines on the right have positive slope, and lines on the left have neg slope
            if slope < 0:
                left.append((slope, y_int))
            else:
                right.append((slope, y_int))
            
    #takes average among all the columns (column0: slope, column1: y_int)
    right_avg = np.average(right, axis=0)
    left_avg = np.average(left, axis=0)
    #create lines based on averages calculates
    left_line = make_points(image, left_avg)
    right_line = make_points(image, right_avg)
    return np.array([left_line, right_line])

def make_points(image, average):
    #print(average)
    try:
        slope, y_int = average
    except TypeError:
        slope, y_int = 1,0

    y1 = image.shape[0]
    #how long we want our lines to be --> 3/5 the size of the image
    y2 = int(y1 * (3/5))
    #determine algebraically
    try:
        x1 = int((y1 - y_int) // slope)
        x2 = int((y2 - y_int) // slope)
    except:
        x1 = x2 = 0
    return np.array([x1, y1, x2, y2])





