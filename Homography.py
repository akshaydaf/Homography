import numpy as np
import scipy
import scipy.misc
import scipy.interpolate
from enum import Enum
class Effect(Enum):
    rotate90 = 1
    rotate180 = 2
    rotate270 = 3
    flipHorizontally = 4
    flipVertically = 5
    transpose = 6
class Homography:
    def __init__(self, **kwargs):
        if "homographyMatrix" in kwargs.keys():
            self.forwardMatrix = kwargs["homographyMatrix"]
            if (type(self.forwardMatrix) != np.ndarray):
                raise ValueError("The Matrix is not an array")
            if (self.forwardMatrix.dtype != np.float64):
                raise ValueError("The data type is not float64")
            if (self.forwardMatrix.shape != (3,3)):
                raise ValueError("The size is not 9")
            self.inverseMatrix = np.linalg.inv(self.forwardMatrix)
        elif "sourcePoints" in kwargs.keys() and "targetPoints" in kwargs.keys():
            sourcePoints = kwargs["sourcePoints"]
            targetPoints = kwargs["targetPoints"]
            effect = None
            if (sourcePoints.shape != (4,2)):
                raise ValueError("Shape of source is incorrect.")
            if (targetPoints.shape != (4,2)):
                raise ValueError("Shape of target is incorrect.")
            if sourcePoints.dtype != np.float64 or type(sourcePoints) != np.ndarray:
                raise ValueError("Data type of source is incorrect.")
            if targetPoints.dtype != np.float64 or type(targetPoints) != np.ndarray:
                raise ValueError("Data type of target is incorrect")
            if ("effect" in kwargs.keys()):
                effect = kwargs["effect"]
                if effect not in Effect and not effect is None:
                    raise TypeError("The effect is not in the Effect class.")
            self.computeHomography(sourcePoints,targetPoints,effect)
        else:
            raise ValueError("Expected key missing")
    def computeHomography(self, sourcePoints, targetPoints, effect):
        sourcepts = sourcePoints
        if (effect==None):
            sourcepts = sourcePoints
        elif (effect == Effect.rotate90):
            sourcepts = np.array([sourcePoints[2],sourcePoints[0],sourcePoints[3],sourcePoints[1]])
        elif (effect == Effect.rotate180):
            sourcepts = np.array([sourcePoints[3],sourcePoints[2],sourcePoints[1],sourcePoints[0]])
        elif (effect == Effect.rotate270):
            sourcepts = np.array([sourcePoints[1],sourcePoints[3],sourcePoints[0],sourcePoints[2]])
        elif (effect == Effect.flipHorizontally):
            sourcepts = np.array([sourcePoints[2],sourcePoints[3],sourcePoints[0],sourcePoints[1]])
        elif (effect == Effect.flipVertically):
            sourcepts = np.array([sourcePoints[1],sourcePoints[0],sourcePoints[3],sourcePoints[2]])
        elif (effect == Effect.transpose):
            sourcepts = np.array([sourcePoints[0],sourcePoints[2],sourcePoints[1],sourcePoints[3]])
        A = np.zeros(shape=(8,8), dtype=np.float64)
        b = targetPoints.reshape(8,1)
        for i in range(4):
            s = sourcepts[i]
            t = targetPoints[i]
            A[i * 2] = np.array([s[0],s[1],1,0,0,0,-1 * t[0]*s[0],-1 * t[0]*s[1]])
            A[i * 2 + 1] = np.array([0,0,0,s[0],s[1],1,-1 * t[1]*s[0],-1 * t[1]*s[1]])
        h = np.linalg.solve(A,b)
        self.forwardMatrix = np.append(h,np.float64(1)).reshape(3,3)
        self.inverseMatrix = np.linalg.inv(self.forwardMatrix)

class Transformation:
    def __init__(self, sourceImage, homography=None):
        self.im = sourceImage
        self.hom = homography
        self.targetPoints = None
        self.sourcePoints = None
        self.max_x = None
        self.max_y = None

        if type(self.im) != np.ndarray:
            raise TypeError("Source image is not an ndarray.")
        elif (type(self.hom) != Homography and not homography is None):
            raise TypeError("Homography not of type Homography.")
    def setupTransformation(self, targetPoints,effect=None):
        if self.hom == None:
            self.max_x = self.im.shape[0] - 1
            self.max_y = self.im.shape[1] - 1
            self.sourcePoints = np.float64(np.array([[0,0],[0,self.max_y], [self.max_x,0],[self.max_x,self.max_y]]))
            self.hom = Homography(sourcePoints=self.sourcePoints, targetPoints=targetPoints, effect=effect)
        else:
            self.hom = self.hom
        self.targetPoints = targetPoints
    def transformImageOnto(self, containerImage):
        if type(containerImage) != np.ndarray:
            raise TypeError("Container Image not of correct type")
        else:
            #optimize later
            bound_x_min, bound_y_min = np.amin(self.targetPoints,axis=0)
            bound_x_max, bound_y_max = np.amax(self.targetPoints, axis=0)
            spline = scipy.interpolate.RectBivariateSpline(np.arange(0, self.max_x + 1,1), np.arange(0,self.max_y + 1,1), self.im, kx=1,ky=1)

            for i in np.arange(bound_x_min,bound_x_max + 1):
                for j in np.arange(bound_y_min, bound_y_max + 1):
                    srcarr = np.matmul(self.hom.inverseMatrix, np.array([i,j,1]))
                    srcarr = srcarr / srcarr[2]
                    srcarr = np.round(srcarr,3)
                    if 0 <= srcarr[0] <= self.max_x and 0 <= srcarr[1] <= self.max_y:
                        containerImage[j][i]= np.round(spline(srcarr[0],srcarr[1]))
                    else:
                        pass
            return(containerImage)
class ColorTransformation(Transformation):
    def __init__(self, sourceImage, homography=None):
        super(ColorTransformation,self).__init__(sourceImage,homography)
        if sourceImage.dtype != np.uint8 or sourceImage.ndim != 3:
            raise ValueError("Image is not a color image!")
    def transformImageOnto(self, containerImage):
        #print(self.targetPoints)
        if type(containerImage) != np.ndarray:
            raise TypeError("Container Image not of correct type")
        bound_x_min, bound_y_min = np.amin(self.targetPoints,axis=0)
        bound_x_max, bound_y_max = np.amax(self.targetPoints, axis=0)
        spliner = scipy.interpolate.RectBivariateSpline(np.arange(0, self.max_x + 1,1), np.arange(0,self.max_y + 1,1), self.im[:,:,0], kx=1,ky=1)
        splineg = scipy.interpolate.RectBivariateSpline(np.arange(0, self.max_x + 1,1), np.arange(0,self.max_y + 1,1), self.im[:,:,1], kx=1,ky=1)
        splineb = scipy.interpolate.RectBivariateSpline(np.arange(0, self.max_x + 1,1), np.arange(0,self.max_y + 1,1), self.im[:,:,2], kx=1,ky=1)
        for i in np.arange(bound_x_min,bound_x_max + 1):
            for j in np.arange(bound_y_min, bound_y_max + 1):
                srcarr = np.matmul(self.hom.inverseMatrix, np.array([i,j,1]))
                srcarr = srcarr / srcarr[2]
                srcarr = np.round(srcarr,3)
                if 0 <= srcarr[0] <= self.max_x and 0 <= srcarr[1] <= self.max_y:
                    containerImage[j][i][0]= np.round(spliner(srcarr[0],srcarr[1]))
                    containerImage[j][i][1]= np.round(splineg(srcarr[0],srcarr[1]))
                    containerImage[j][i][2]= np.round(splineb(srcarr[0],srcarr[1]))
                else:
                    pass
        return(containerImage)
class AdvancedTransformation:
    def __init__(self, sourceImage, v, h1, h2):
        if type(sourceImage) != np.ndarray:
            raise TypeError("Source image not an ndarray")
        elif sourceImage.ndim != 3:
            raise ValueError("Source image is not color")
        self.im = sourceImage
        self.max_x = self.im.shape[0] - 1
        self.max_y = self.im.shape[1] - 1
        if (self.max_y + 1) % 2 != 0:
            raise ValueError("Image passed does not have even columns")
        self.n = ((self.max_y + 1)/ 2) - 1
        self.v = v
        self.h1 = h1
        self.h2 = h2
if __name__ == "__main__":
    sourcept = np.array([[3,12],[10,5],[4,7],[2,6]], dtype=np.float64)
    targetpt = np.array([[16,2],[14,7],[0,9],[10,11]],dtype=np.float64)
    dict1 = dict()
    dict1["sourcePoints"] = sourcept
    dict1["targetPoints"] = targetpt
    dict1["effect"] = Effect.rotate90
    obj1 = Homography(**dict1)
    sourcePoints = np.array([[0, 0], [1919, 0], [0, 1079], [1919,  1079.0]])
    targetPoints = np.array([[600, 50], [1550, 500], [50, 400], [800, 1150.0]])


    sourceImage = scipy.misc.imread("TestImages/knight.png")

    transform = Transformation(sourceImage)
    transform.setupTransformation(targetPoints = np.array([[600, 50], [1550, 500], [50, 400], [800, 1150.0]]))
    containerImage = scipy.misc.imread("TestImages/WhiteGray.png")
    actualValue = transform.transformImageOnto(containerImage)
    expectedValue = scipy.misc.imread("TestImages/Target_knight.png")
    for i in range(0,len(actualValue[0])):
        for j in range(0,i):
            if (actualValue[j][i] != expectedValue[j][i]):
                print("UGH")
    isEqual = np.all(actualValue == expectedValue)
