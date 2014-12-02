# import the necessary packages
import cv2

class EyeTracker:
	def __init__(self, path):
		# load the face and eye detector
		self.faceCascade = cv2.CascadeClassifier(path + '/haarcascade_frontalface_default.xml')
		self.eyeCascade = cv2.CascadeClassifier(path + '/haarcascade_mcs_eyepair_big.xml')
		self.mouthCascade = cv2.CascadeClassifier(path + '/Mouth.xml')
		self.noseCascade = cv2.CascadeClassifier(path + '/haarcascade_mcs_nose.xml')
	def track(self, image):
		# detect faces in the image and initialize the list of
		# rectangles containing the faces and eyes
		faceRects = self.faceCascade.detectMultiScale(image,
			scaleFactor = 1.1, minNeighbors = 10,
			minSize = (5, 5), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
		rects = {}

		# loop over the face bounding boxes
		for (fX, fY, fW, fH) in faceRects:

			# extract the face ROI and update the list of
			# bounding boxes
			faceROI = image[fY:fY + fH, fX:fX + fW]
			rects["face"] = (fX, fY, fX + fW, fY + fH)
			
			# detect eyes in the face ROI
			eyeRects = self.eyeCascade.detectMultiScale(faceROI,
				scaleFactor = 1.1, minNeighbors = 20, minSize = (25, 15),
				flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
		
			# detect a mouth in the face ROI
			mouthRects = self.mouthCascade.detectMultiScale(faceROI, 
				scaleFactor = 1.1, minNeighbors = 30, minSize = (25, 15), 
				flags = cv2.cv.CV_HAAR_SCALE_IMAGE)

			# detect a nose in the face ROI
			noseRects = self.noseCascade.detectMultiScale(faceROI, 
				scaleFactor = 1.1, minNeighbors = 10, minSize = (25, 15), 
				flags = cv2.cv.CV_HAAR_SCALE_IMAGE)

			# loop over the eye bounding boxes
			for (eX, eY, eW, eH) in eyeRects:
				# update the list of boounding boxes
				rects["eye"] = (fX + eX, fY + eY, fX + eX + eW, fY + eY + eH)

			# loop over the mouth bounding boxes
			for (eX, eY, eW, eH) in mouthRects:
				# update the list of boounding boxes
				if (eY+eH) > (fH/1.5):
					rects["mouth"] = (fX + eX, fY + eY, fX + eX + eW, fY + eY + eH)					

			# loop over the nose bounding boxes
			for (eX, eY, eW, eH) in noseRects:
				if (eY+eH) > (fH/1.5):
					# update the list of boounding boxes
					rects["nose"] = (fX + eX, fY + eY, fX + eX + eW, fY + eY + eH)
		
		# return the rectangles representing bounding
		# boxes around the faces and eyes
		return rects