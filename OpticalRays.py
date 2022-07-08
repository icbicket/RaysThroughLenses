import numpy as np


# TODO calculate required focal length to achieve a fixed crossover point given an input ray


def calculate_outgoing_angle(incoming_angle, y, f):
    y2 = f * np.tan(incoming_angle)
    outgoing_angle = np.arctan((y2 - y) / f)
    return outgoing_angle

def calculate_ray_path(x, y, angle):
    ray_path = np.tan(angle) * -x + y
    return ray_path

class OpticalRay:
    def __init__(self, origin_point, origin_angle):
        self.angles = [origin_angle,] # a single angle (radians)
        #self.angles = np.append(self.angles, origin_angle)
        
        # to contain m and b from y=mx+b for each path the ray travels
        initial_path_slope, initial_path_intercept = self.calculate_linear_equation(origin_angle, origin_point)
        self.paths = np.array([[initial_path_slope, initial_path_intercept]])
        self.path_vertices = np.expand_dims(origin_point, axis=0)
        self.add_placeholder_vertex(origin_point[0] + 10)
        self.lenses = []
    
    def calculate_linear_equation(self, angle, origin):
        # angle: radians
        # origin: (x,y) coordinate pair
        # y=mx+b
        intercept = origin[1] - origin[0] * np.tan(angle) # b = y0 - x0 * m
        slope = np.tan(angle)
        return slope, intercept
    
    def add_lens(self, new_lens):
        # lens_location: x value where the next lens sits
        # account for lenses being added at x-values less than previous lens TODO
        incident_y = self.paths[-1, 0] * new_lens.location + self.paths[-1, 1]
        outgoing_angle = calculate_outgoing_angle(self.angles[-1], incident_y, new_lens.f)
        outgoing_slope, outgoing_intercept = self.calculate_linear_equation(
            outgoing_angle, [new_lens.location, incident_y]
        )
        self.lenses.append(new_lens)
        self.angles.append(outgoing_angle)
        self.path_vertices[-1, :] = np.array([[new_lens.location, incident_y]])
        self.paths = np.append(self.paths, np.array([[outgoing_slope, outgoing_intercept]]), axis=0)
        self.add_placeholder_vertex(new_lens.location+10)

        return
    
    def add_placeholder_vertex(self, x_location):
        # for seeing the ray during plotting
        self.path_vertices = np.append(
            self.path_vertices,
            np.array([[100, self.paths[-1, 0]*100+self.paths[-1, 1]]]),
            axis=0
        )

