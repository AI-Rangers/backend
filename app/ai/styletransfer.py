import imutils
import cv2
import os
# import numpy as np

# source, destination, 
def styleTransfer(src_folder, dest_folder, filename, selected_style):
	# load the neural style transfer model from disk
	target = 'app/ai/style_model/'
	net = cv2.dnn.readNetFromTorch(target + selected_style)

	# load the input image, resize it to have a width of 600 pixels, and
	# then grab the image dimensions
	image = cv2.imread(src_folder+filename)
	image = imutils.resize(image, width=600)
	(h, w) = image.shape[:2]

	# construct a blob from the image, set the input, and then perform a
	# forward pass of the network
	blob = cv2.dnn.blobFromImage(image, 1.0, (w, h),
		(103.939, 116.779, 123.680), swapRB=False, crop=False)
	net.setInput(blob)

	output = net.forward()

	# reshape the output tensor, add back in the mean subtraction, and
	# then swap the channel ordering
	output = output.reshape((3, output.shape[2], output.shape[3]))
	output[0] += 103.939
	output[1] += 116.779
	output[2] += 123.680
	#uncomment this for imshow etc to display (if running as a script)
	#output /= 255.0
	output = output.transpose(1, 2, 0)

	#cv2.imshow('image',output)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
	
	#output = (output * 255).astype(np.uint8)

	filename, file_extension = os.path.splitext(filename)
	print(filename)
	newFileName = 'processedImg'+ '_' + filename + file_extension
	cv2.imwrite(dest_folder + newFileName, output)
	print(newFileName)
	print(dest_folder)

	return newFileName
