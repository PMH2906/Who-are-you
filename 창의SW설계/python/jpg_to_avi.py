from PIL import Image
import numpy,cv2

image1 = Image.open("m1.jpg")
image2 = Image.open("m2.jpg")

# Grab the stats from image1 to use for the resultant video
height, width, layers =  numpy.array(image1).shape

# Create the OpenCV VideoWriter
video = cv2.VideoWriter("m4.avi", -1, 10,(width,height))

# We'll have 30 frames be the animated transition from image1 to image2. At 10FPS, this is a whole 3 seconds
for i in range(0,30):
    images1And2 = Image.blend(image1, image2, i/30.0)

    # Conversion from PIL to OpenCV from: http://blog.extramaster.net/2015/07/python-converting-from-pil-to-opencv-2.html
    video.write(cv2.cvtColor(numpy.array(images1And2), cv2.COLOR_RGB2BGR))

# And back from image2 to image1...
for i in range(0,30):
    images2and1 = Image.blend(image2, image1, i/30.0)
    video.write(cv2.cvtColor(numpy.array(images2and1), cv2.COLOR_RGB2BGR))

# Release the video for it to be committed to a file
video.release()
