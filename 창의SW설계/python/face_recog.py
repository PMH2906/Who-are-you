# face_recog.py
#from vibration import *
from tts import *
from openpyxl import load_workbook
import face_recognition
import cv2
import camera
import serial
import os
import numpy as np
from PIL import Image
from glob import glob
import PIL
import sys
path = 'C:/face_recognition/'
path_originals = 'C:/out/'

if not os.path.exists(path):
    os.makedirs(path)

def compress_image(image, infile):
    size = 1920, 1080
    width = 1920
    height = 1080
    listing = os.listdir(path_originals)

    name = infile.split('.')
    first_name = path+'/'+name[0] + '.jpg'
    if image.size[0] > width and image.size[1] > height:
        image.thumbnail(size, Image.ANTIALIAS)
        image.save(first_name, quality=85)
    elif image.size[0] > width:
        wpercent = (width/float(image.size[0]))
        height = int((float(image.size[1])*float(wpercent)))
        image = image.resize((width,height), PIL.Image.ANTIALIAS)
        image.save(first_name,quality=85)
    elif image.size[1] > height:
        wpercent = (height/float(image.size[1]))
        width = int((float(image.size[0])*float(wpercent)))
        image = image.resize((width,height), PIL.Image.ANTIALIAS)
        image.save(first_name, quality=85)
    else:
        image.save(first_name, quality=85)


def processImage():
    listing = os.listdir(path_originals)
    for infile in listing:
        img = Image.open(path_originals+infile)
        name = infile.split('.')
        first_name = path+'/'+name[0] + '.jpg'

        if img.format == "JPEG":
            image = img.convert('RGB')
            compress_image(image, infile)
            img.close()

        elif img.format == "GIF":
            i = img.convert("RGBA")
            bg = Image.new("RGBA", i.size)
            image = Image.composite(i, bg, i)
            compress_image(image, infile)
            img.close()

        elif img.format == "PNG":
            try:
                image = Image.new("RGB", img.size, (255,255,255))
                image.paste(img,img)
                compress_image(image, infile)
            except ValueError:
                image = img.convert('RGB')
                compress_image(image, infile)
            img.close()

        elif img.format == "BMP":
            image = img.convert('RGB')
            compress_image(image, infile)
            img.close()

processImage()

class FaceRecog():
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.camera = camera.VideoCamera()

        self.known_face_encodings = []
        self.known_face_names = []

        # Load sample pictures and learn how to recognize it.
        dirname = 'knowns'
        files = os.listdir(dirname)
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext == '.jpg':
                self.known_face_names.append(name)
                pathname = os.path.join(dirname, filename)
                img = face_recognition.load_image_file(pathname)
                face_encoding = face_recognition.face_encodings(img)[0]
                self.known_face_encodings.append(face_encoding)

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

    def __del__(self):
        del self.camera

    def get_frame(self):
        # Grab a single frame of video
        frame = self.camera.get_frame()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                min_value = min(distances)

                # tolerance: How much distance between faces to consider it a match. Lower is more strict.
                # 0.6 is typical best performance.
                name = "Unknown"
                if min_value < 0.6:
                    index = np.argmin(distances)
                    name = self.known_face_names[index]

                self.face_names.append(name)

        self.process_this_frame = not self.process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            fw=open('sample.txt','w')
            fw.write(name)
            fw.close()
        return frame

    def get_jpg_bytes(self):
        frame = self.get_frame()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()


if __name__ == '__main__':
    face_recog = FaceRecog()
    print(face_recog.known_face_names)
    while True:
        frame = face_recog.get_frame()

        # show the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        tempEx=load_workbook(filename='people.xlsx')
        arduino=serial.Serial('COM6',9600)
        arduino1=serial.Serial('COM1',9600)
        sheet1 = tempEx['Sheet1']
        f=open('sample.txt','r')
        x=[]
        x=f.read()
        

        temps = []

        for i in sheet1.rows:
            k=i[0].value
            
            if k in x:
                my_str= i[0].value
                my_str1=i[1].value
                my_str2=i[2].value
                my_str3=i[3].value
                my_str_bytes = str.encode(my_str)
                type(my_str_bytes) 
                print(my_str_bytes)
                my_str_bytes2 =str.encode(my_str2)
                type(my_str_bytes2)
                print(my_str_bytes2)
                my_str_bytes3=str.encode(my_str3)
                type(my_str_bytes3)
                print(my_str_bytes3)
                my_str4= i[4].value
                my_str_as_bytes4=str.encode(my_str4)
                type(my_str_as_bytes4)
                print(my_str4)
                while True:
                    arduino.write(my_str_as_bytes4)
                    arduino1.write(my_str_bytes+b'/'+my_str_bytes2+b'/'+my_str_bytes3+b'\0')
                    

        
        #do_vibration(x)
      
        break
        # if the `q` key was pressed, break from the loop
        #if t==1:
            #break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    print('finish')
