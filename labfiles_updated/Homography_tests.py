import os
from os.path import join
from glob import glob
import unittest
from random import uniform
from inspect import isclass
from enum import Enum
from scipy.misc import *
import numpy as np
from Homography import *

testFolder = "TestImages"


class HomographyTestSuite(unittest.TestCase):

    targetPoints = np.array([[600, 50], [1550, 500], [50, 400], [800, 1150.0]])
    effectList = ["rotate90", "rotate180", "rotate270", "flipHorizontally", "flipVertically", "transpose"]

    def test_EffectEnumExists(self):
        """
        Test for the existence of the Effect enum.
        """

        self.assertTrue(isclass(Effect))

    def test_EffectEnumMembers(self):
        """
        Test for the existence of the Effect enum members.
        """
        expectedValues = self.effectList

        for expectedValue in expectedValues:

            with self.subTest(expectedValue):
                self.assertIn(expectedValue, Effect.__members__)

    def test_HomographyInitializerWithMatrix(self):
        """
        Test the behavior of the homography initializer with a matrix.
        """
        with self.subTest(key="Good Matrix"):
            mat = np.array([[1.2, 2.3, 4.5], [9.0, 4.4, 5.5], [0.0, 0.0, 1.0]])
            h = Homography(homographyMatrix=mat)
            self.assertIsInstance(h, Homography)

        with self.subTest(key="Bad Matrix 1"):
            # Not a 3 x 3
            mat = np.array([[1.2, 2.3, 4.5], [9.0, 4.4, 5.5]])

            self.assertRaises(ValueError, Homography, homographyMatrix=mat)

        with self.subTest(key="Bad Matrix 2"):
            # Not float.
            mat = np.array([[2, 2, 4], [9, 4, 5], [0, 0, 1]])

            self.assertRaises(ValueError, Homography, homographyMatrix=mat)

        with self.subTest(key="Incorrect Parameter"):
            mat = np.array([[1.2, 2.3, 4.5], [9.0, 4.4, 5.5], [0.0, 0.0, 1.0]])

            self.assertRaises(ValueError, Homography, homographyMat=mat)

    def test_HomographyInitializerWithPoints(self):
        """
        Test the behavior of the homography initializer with points.
        """
        u = lambda : (uniform(1.0, 10.0), uniform(1.0, 10.0))
        s = np.array([u() for _ in range(4)])
        t = np.array([u() for _ in range(4)])

        with self.subTest(key="Good Points"):
            h = Homography(sourcePoints=s, targetPoints=t)

            self.assertIsInstance(h, Homography)

        with self.subTest(key="Incorrect Parameter 1"):

            self.assertRaises(ValueError, Homography, sourcePts=s, targetPoints=t)

        with self.subTest(key="Incorrect Parameter 2"):

            self.assertRaises(ValueError, Homography, sourcePoints=s, targetPts=t)

        with self.subTest(key="Bad Points"):
            s = np.array([u() for _ in range(3)])

            self.assertRaises(ValueError, Homography, sourcePoints=s, targetPoints=t)

    def test_HomographyInitializerWithPointsAndEffect(self):
        """
        Test the behavior of the homography initializer with points and Effects.
        """
        u = lambda: (uniform(1.0, 10.0), uniform(1.0, 10.0))
        s = np.array([u() for _ in range(4)])
        t = np.array([u() for _ in range(4)])

        with self.subTest(key="Good Effect 1"):
            h = Homography(sourcePoints=s, targetPoints=t, effect=None)

            self.assertIsInstance(h, Homography)

        with self.subTest(key="Good Effect 2"):
            h = Homography(sourcePoints=s, targetPoints=t, effect=Effect.rotate90)

            self.assertIsInstance(h, Homography)

        with self.subTest(key="Incorrect Type"):

            self.assertRaises(TypeError, Homography, sourcePoints=s, targetPoints=t, effect="rotate90")

    def test_computeHomography(self):
        """
        Test the homography computation using correspondences.
        """

        sourcePoints = np.array([[0, 0], [1919, 0], [0, 1079], [1919,  1079.0]])
        targetPoints = np.array([[600, 50], [1550, 500], [50, 400], [800, 1150.0]])

        storagePath = join(testFolder, "Variables.npz")
        with np.load(storagePath) as npFile:
            expectedValue = np.round(npFile["homography"], 10)

        h = Homography(sourcePoints = sourcePoints, targetPoints = targetPoints)
        actualValue = np.round(h.forwardMatrix, 10)

        isMatched = np.array_equal(expectedValue, actualValue)

        self.assertEqual(isMatched, True)

    def test_TransformationInitializer(self):
        """
        Test the behavior of the Transformation initializer.
        """
        with self.subTest(key="Good Image 1"):
            img = np.ones([10, 10], dtype="uint8")
            trans = Transformation(img)

            self.assertIsInstance(trans, Transformation)

        with self.subTest(key="Good Image 2"):
            img = np.ones([10, 10], dtype="uint8")
            trans = Transformation(img, None)

            self.assertIsInstance(trans, Transformation)

        with self.subTest(key="Good Homography"):
            img = np.ones([10, 10], dtype="uint8")
            mat = np.array([[1.2, 2.3, 4.5], [9.0, 4.4, 5.5], [0.0, 0.0, 1.0]])
            h = Homography(homographyMatrix=mat)
            trans = Transformation(img, h)

            self.assertIsInstance(trans, Transformation)

        with self.subTest(key="Bad Image"):
            img = [[0, 0], [1, 1]]

            self.assertRaises(TypeError, Transformation, sourceImage=img)

        with self.subTest(key="Bad Homography"):
            img = np.ones([10, 10], dtype="uint8")
            h = np.array([[1.2, 2.3, 4.5], [9.0, 4.4, 5.5], [0.0, 0.0, 1.0]])
            self.assertRaises(TypeError, Transformation, sourceImage=img, homography=h)

    def test_transformImageWhenImageIsBad(self):
        """
        Test the behavior of the transformImage against bad data.
        """
        img = np.ones([10, 10], dtype="uint8")
        mat = np.array([[1.2, 2.3, 4.5], [9.0, 4.4, 5.5], [0.0, 0.0, 1.0]])
        h = Homography(homographyMatrix=mat)
        trans = Transformation(img, h)

        with self.subTest(key="Bad Type"):
            targetImg = [[1.2, 2.3, 4.5], [9.0, 4.4, 5.5], [0.0, 0.0, 1.0]]

            self.assertRaises(TypeError, trans.transformImageOnto, targetImg)

    def test_transformImageGray(self):
        """
        Test the transformation of gray images.
        """
        sourceImage = imread(join(testFolder, "knight.png"))

        with self.subTest(key = "Gray No Effect"):
            transform = Transformation(sourceImage)
            transform.setupTransformation(self.targetPoints)

            containerImage = imread(join(testFolder, "WhiteGray.png"))
            actualValue = transform.transformImageOnto(containerImage)
            expectedValue = imread(join(testFolder, "Target_knight.png"))

            isEqual = np.array_equal(actualValue, expectedValue)

            self.assertEqual(isEqual, True)

        for effect in Effect:
            with self.subTest(key = "Gray " + effect.name):
                transform = Transformation(sourceImage)
                transform.setupTransformation(self.targetPoints, effect)

                containerImage = imread(join(testFolder, "WhiteGray.png"))
                actualValue = transform.transformImageOnto(containerImage)
                expectedValue = imread(join(testFolder, "Target_knight_{}.png".format(effect.name)))

                isEqual = np.array_equal(actualValue, expectedValue)

                self.assertEqual(isEqual, True)

    def test_colorTransformationInitializer(self):
        """
        Test the behavior of the ColorTransformation initializer.
        """
        with self.subTest(key="Good Image 1"):
            img = np.ones([10, 10, 3], dtype="uint8")
            trans = ColorTransformation(img)

            self.assertIsInstance(trans, ColorTransformation)

        with self.subTest(key="Good Image 2"):
            img = np.ones([10, 10, 3], dtype="uint8")
            trans = ColorTransformation(img, None)

            self.assertIsInstance(trans, ColorTransformation)

        with self.subTest(key="Good Homography"):
            img = np.ones([10, 10, 3], dtype="uint8")
            mat = np.array([[1.2, 2.3, 4.5], [9.0, 4.4, 5.5], [0.0, 0.0, 1.0]])
            h = Homography(homographyMatrix=mat)
            trans = ColorTransformation(img, h)

            self.assertIsInstance(trans, ColorTransformation)

        with self.subTest(key="Bad Image Type"):
            img = [[0, 0], [1, 1]]

            self.assertRaises(TypeError, ColorTransformation, sourceImage=img)

        with self.subTest(key="Bad Image Dimensions"):
            img = np.ones([10, 10], dtype="uint8")

            self.assertRaises(ValueError, ColorTransformation, sourceImage=img)

        with self.subTest(key="Bad Homography"):
            img = np.ones([10, 10, 3], dtype="uint8")
            h = [[1.2, 2.3, 4.5], [9.0, 4.4, 5.5], [0.0, 0.0, 1.0]]

            self.assertRaises(TypeError, ColorTransformation, sourceImage=img, homography=h)

    def test_transformImageColor(self):
        """
        Test the transformation of color images.
        """
        sourceImage = imread(join(testFolder, "strange.png"))

        with self.subTest(key = "Color No Effect"):
            transform = ColorTransformation(sourceImage)
            transform.setupTransformation(self.targetPoints)

            containerImage = imread(join(testFolder, "White.png"))
            actualValue = transform.transformImageOnto(containerImage)
            expectedValue = imread(join(testFolder, "Target_strange.png"))

            isEqual = np.array_equal(actualValue, expectedValue)

            self.assertEqual(isEqual, True)

        for effect in Effect:
            with self.subTest(key = "Gray " + effect.name):
                transform = ColorTransformation(sourceImage)
                transform.setupTransformation(self.targetPoints, effect)

                containerImage = imread(join(testFolder, "White.png"))
                actualValue = transform.transformImageOnto(containerImage)
                expectedValue = imread(join(testFolder, "Target_strange_{}.png".format(effect.name)))

                isEqual = np.array_equal(actualValue, expectedValue)

                self.assertEqual(isEqual, True)


class MoreHomographyTestSuite(unittest.TestCase):

    parameterList = [(100, 0, 0), (0, 50, 50), (100, 50, 0), (100, 0, 50), (100, 50, 50)]

    def test_advancedTransformationInitializer(self):
        """
        Test the behavior of the AdvancedTransformation initializer.
        """
        with self.subTest(key="Good Image"):
            img = np.ones([10, 10, 3], dtype="uint8")
            trans = AdvancedTransformation(img, 0, 0, 0)

            self.assertIsInstance(trans, AdvancedTransformation)

        with self.subTest(key="Bad Image 1"):
            img = [[0, 0], [1, 1]]

            self.assertRaises(TypeError, AdvancedTransformation, img, 0, 0, 0)

        with self.subTest(key="Bad Image 2"):
            img = np.ones([10, 10], dtype="uint8")

            self.assertRaises(ValueError, AdvancedTransformation, img, 0, 0, 0)

        with self.subTest(key="Bad Image 3"):
            img = np.ones([10, 11, 3], dtype="uint8")

            self.assertRaises(ValueError, AdvancedTransformation, img, 0, 0, 0)

    def test_applyEffectV(self):
        """
        Test the Effect V application.
        """
        sourceImagePath = join(testFolder, "Ring.png")
        sourceImage = imread(sourceImagePath)

        for v, h1, h2 in self.parameterList:
            with self.subTest(key=(v, h1, h2)):

                transformer = AdvancedTransformation(sourceImage, v, h1, h2)
                actualValue = transformer.applyEffectV()

                resultImagePath = join(testFolder, "Ring_EffectV_{0:03d}_{1:03d}_{2:03d}.png".format(v, h1, h2))
                expectedValue = imread(resultImagePath)

                isEqual = np.array_equal(actualValue, expectedValue)

                self.assertEqual(isEqual, True)

    def test_applyEffectA(self):
        """
        Test the Effect A application.
        """
        sourceImagePath = join(testFolder, "Ring3.png")
        sourceImage = imread(sourceImagePath)

        for v, h1, h2 in self.parameterList:
            with self.subTest(key=(v, h1, h2)):

                transformer = AdvancedTransformation(sourceImage, v, h1, h2)
                actualValue = transformer.applyEffectA()

                resultImagePath = join(testFolder, "Ring_EffectA_{0:03d}_{1:03d}_{2:03d}.png".format(v, h1, h2))
                expectedValue = imread(resultImagePath)

                isEqual = np.array_equal(actualValue, expectedValue)

                self.assertEqual(isEqual, True)


if __name__ == "__main__":
    unittest.main()
