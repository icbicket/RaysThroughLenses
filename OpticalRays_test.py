import OpticalRays
import ThinLens
import unittest
import numpy as np

class OpticalRayTest(unittest.TestCase):
    '''
    Rays parallel to the lens axis should meet the axis at the focal point
    Rays parallel to each other should meet each other at the focal point
    Result should not depend if the lens is located at x=0
    Rays passing through the centre of the lens (y=0) should not be deflected
    Two lenses
    '''
    def testOnAxisRay(self):
        '''
        A ray along the axis should pass straight through
        '''
        ray = OpticalRays.OpticalRay((-10, 0), 0)
        lens = ThinLens.ThinLens(3, 0)
        ray.add_lens(lens)
        expected_outgoing_angle = 0
        expected_path = np.array([[0, 0], [0, 0]])
        expected_path_vertices = np.array([[-10, 0], [0, 0], [100, 0]])
        np.testing.assert_array_almost_equal(ray.paths, expected_path)
        np.testing.assert_array_almost_equal(ray.path_vertices, expected_path_vertices)

    def testUpThroughCentreRay(self):
        '''
        A ray passing up through the centre of the lens should continue straight
        '''
        ray = OpticalRays.OpticalRay((-1, -1), np.pi/4)
        lens = ThinLens.ThinLens(3, 0)
        ray.add_lens(lens)
        expected_angles = np.array([np.pi/4, np.pi/4])
        expected_path = np.array([[1, 0], [1, 0]])
        expected_path_vertices = np.array([[-1, -1], [0, 0], [100, 100]])
        np.testing.assert_array_almost_equal(ray.paths, expected_path)
        np.testing.assert_array_almost_equal(ray.path_vertices, expected_path_vertices)
        np.testing.assert_array_almost_equal(ray.angles, expected_angles)

    def testParallelRay(self):
        '''
        A ray parallel to the optic axis should refract to the focal point on the axis
        '''
        ray = OpticalRays.OpticalRay((-1, 1), 0)
        lens = ThinLens.ThinLens(3, 0)
        ray.add_lens(lens)
        expected_angles = np.array([0, np.arctan(-1/3)])
        expected_path = np.array([[0, 1], [-1/3, 1]])
        expected_path_vertices = np.array([[-1, 1], [0, 1], [100, -100/3+1]])
        np.testing.assert_array_almost_equal(ray.paths, expected_path)
        np.testing.assert_array_almost_equal(ray.path_vertices, expected_path_vertices)
        np.testing.assert_array_almost_equal(ray.angles, expected_angles)

    def testDownThroughCentreRay(self):
        '''
        A ray passing down through the centre of the lens should continue straight
        '''
        ray = OpticalRays.OpticalRay((-1, 1), -np.pi/4)
        lens = ThinLens.ThinLens(3, 0)
        ray.add_lens(lens)
        expected_angles = np.pi/4
        expected_path = np.array([[-1, 0], [-1, 0]])
        expected_path_vertices = np.array([[-1, 1], [0, 0], [100, -100]])
        np.testing.assert_array_almost_equal(ray.paths, expected_path)
        np.testing.assert_array_almost_equal(ray.path_vertices, expected_path_vertices)

    def testUpOffCentreRay(self):
        '''
        A ray passing up outside the centre of the mirror should meet a parallel ray at the focal point
        '''
        f = 3
        x0 = -1
        y0 = -1
        angle0 = np.pi/6
        b0 = y0 - np.tan(angle0)*x0
        x1 = 0
        y1 = np.tan(angle0)*x1 + b0
        x2 = f
        y2 = np.tan(np.pi/6) * f
        ray = OpticalRays.OpticalRay((x0, y0), angle0)
        lens = ThinLens.ThinLens(f, x1)
        ray.add_lens(lens)
        outgoing_slope = (y2-y1)/(x2-x1)
        outgoing_angle = np.arctan(outgoing_slope)
        outgoing_intersect = y2 - outgoing_slope * f
        expected_path = np.array([[np.tan(np.pi/6), b0], [outgoing_slope, outgoing_intersect]])
        expected_path_vertices = np.array([[x0, y0], [x1, y1], [100, 100*outgoing_slope+outgoing_intersect]])
        expected_angles = np.array([np.pi/6, np.arctan(outgoing_slope)])
        np.testing.assert_array_almost_equal(ray.paths, expected_path)
        np.testing.assert_array_almost_equal(ray.path_vertices, expected_path_vertices)
        np.testing.assert_array_almost_equal(ray.angles, expected_angles)

    def testDownOffCentreRay(self):
        '''
        A ray passing down outside the centre of the mirror should meet a parallel ray at the focal point
        '''
        f = 3
        x0 = -1
        y0 = 1
        angle0 = -np.pi/6
        b0 = y0 - np.tan(angle0)*x0
        x1 = 0
        y1 = np.tan(angle0)*x1 + b0
        x2 = f
        y2 = np.tan(angle0) * f
        ray = OpticalRays.OpticalRay((x0, y0), angle0)
        lens = ThinLens.ThinLens(f, x1)
        ray.add_lens(lens)
        outgoing_slope = (y2-y1)/(x2-x1)
        outgoing_angle = np.arctan(outgoing_slope)
        outgoing_intersect = y2 - outgoing_slope * f
        expected_path = np.array([[np.tan(angle0), b0], [outgoing_slope, outgoing_intersect]])
        expected_path_vertices = np.array([[x0, y0], [x1, y1], [100, 100*outgoing_slope+outgoing_intersect]])
        expected_angles = np.array([angle0, np.arctan(outgoing_slope)])
        np.testing.assert_array_almost_equal(ray.paths, expected_path)
        np.testing.assert_array_almost_equal(ray.path_vertices, expected_path_vertices)
        np.testing.assert_array_almost_equal(ray.angles, expected_angles)

    def testOnAxisRayLensAt1(self):
        '''
        A ray along the axis should pass straight through
        Lens is at x=1
        '''
        ray = OpticalRays.OpticalRay((-10, 0), 0)
        lens = ThinLens.ThinLens(3, 1)
        ray.add_lens(lens)
        expected_outgoing_angle = 0
        expected_path = np.array([[0, 0], [0, 0]])
        expected_path_vertices = np.array([[-10, 0], [1, 0], [100, 0]])
        np.testing.assert_array_almost_equal(ray.paths, expected_path)
        np.testing.assert_array_almost_equal(ray.path_vertices, expected_path_vertices)
        
    def testUpOffCentreRayLensAt1(self):
        '''
        A ray passing up outside the centre of the mirror should meet a parallel ray at the focal point
        Lens is at x=1
        '''
        f = 3
        x0 = -1
        y0 = -1
        angle0 = np.pi/6
        b0 = y0 - np.tan(angle0)*x0
        x1 = 1
        y1 = np.tan(angle0)*x1 + b0
        x2 = f+x1
        y2 = np.tan(angle0) * f
        ray = OpticalRays.OpticalRay((x0, y0), angle0)
        lens = ThinLens.ThinLens(f, x1)
        ray.add_lens(lens)
        outgoing_slope = (y2-y1)/(x2-x1)
        outgoing_angle = np.arctan(outgoing_slope)
        outgoing_intersect = y2 - outgoing_slope * x2
        expected_path = np.array([[np.tan(np.pi/6), b0], [outgoing_slope, outgoing_intersect]])
        expected_path_vertices = np.array([[x0, y0], [x1, y1], [100, 100*outgoing_slope+outgoing_intersect]])
        expected_angles = np.array([np.pi/6, np.arctan(outgoing_slope)])
        np.testing.assert_array_almost_equal(ray.paths, expected_path)
        np.testing.assert_array_almost_equal(ray.path_vertices, expected_path_vertices)
        np.testing.assert_array_almost_equal(ray.angles, expected_angles)

    def testTwoLenses(self):
        '''
        A ray passing through two lenses
        '''
        x0 = -1 #origin x
        y0 = -1 #origin y
        angle0 = np.pi/6 # starting angle
        f1 = 3 # focal power of lens 1
        f2 = 2 # focal power of lens 2
        x1 = 1 # location of lens 1
        x3 = 3 # location of lens 2
        x5 = 100 # placeholder point at the end
        y1 = np.tan(angle0)*(x1-x0)+y0 # point of incidence on lens 1
        x2 = f1 + x1 # waypoint x at focal point of lens 1
        y2 = f1 * np.tan(angle0) # waypoint y at focal point of lens 1
        angle1 = np.arctan((y2-y1)/f1) # angle coming out of lens 1
        m1 = np.tan(angle0) # slope of original ray
        b1 = y0 - m1*x0 # intercept of ray original ray
        m2 = np.tan(angle1) # slope of ray going out of lens 1
        b2 = y1 - m2*x1 # intercept of ray going out of lens 2
        y3 = m2 * x3 + b2 # point of incidence on lens 2
        y4 = f2 * np.tan(angle1) # waypoint y at focal point of lens 2
        x4 = x3 + f2 # waypoint x at focal point of lens 2
        angle2 = np.arctan((y4-y3)/f2) # angle of ray refracted from lens 2
        m3 = np.tan(angle2) # slope of ray refracted from lens 2
        b3 = y3 - m3 * x3 # intercept of ray refracted from lens 2
        y5 = m3 * x5 + b3 # y-value of placeholder endpoint
        ray = OpticalRays.OpticalRay((x0, y0), angle0)
        lens1 = ThinLens.ThinLens(f1, x1)
        lens2 = ThinLens.ThinLens(f2, x3)
        ray.add_lens(lens1)
        ray.add_lens(lens2)
        expected_path = np.array([[m1, b1], [m2, b2], [m3, b3]])
        expected_path_vertices = np.array([[x0, x0], [x1, y1], [x3, y3], [x5, y5]])
        expected_angles = [angle0, angle1, angle2]
        np.testing.assert_array_almost_equal(ray.paths, expected_path)
        np.testing.assert_array_almost_equal(ray.path_vertices, expected_path_vertices)
        np.testing.assert_array_almost_equal(ray.angles, expected_angles)

if __name__ == '__main__':
    unittest.main()
