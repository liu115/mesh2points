import numpy as np
import trimesh
import math
import random
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='input file', required=True)
parser.add_argument('-o', '--output', help='output file', required=True)
parser.add_argument('-n', '--number', help='sample number', default=100, type=int)
parser.add_argument('--normalize', action='store_true', help='normalize to unit ball')
args = parser.parse_args()
print(args)

def triangle_area(v1, v2, v3):

    a = np.array(v2) - np.array(v1)
    b = np.array(v3) - np.array(v1)
    return math.sqrt(np.dot(a, a) * np.dot(b, b) - (np.dot(a, b) ** 2)) / 2.0


def cal_suface_area(mesh):
    areas = []
    for face in mesh.faces:
        v1, v2, v3 = face
        v1 = mesh.vertices[v1]
        v2 = mesh.vertices[v2]
        v3 = mesh.vertices[v3]

        areas += [triangle_area(v1, v2, v3)]
    areas = np.array(areas)
    return np.array(areas)


sample_num = args.number
output_file = args.output
if __name__ == '__main__':

    output = open(output_file, 'w')

    mesh = trimesh.load(args.input)
    print("number of vertices: ", len(mesh.vertices))
    print("number of faces: ", len(mesh.faces))

    areas = cal_suface_area(mesh)
    prefix_sum = np.cumsum(areas)

    total_area = prefix_sum[-1]
    print("total area: ", total_area)

    sample_points = []
    for i in range(sample_num):
        prob = random.random()
        sample_pos = prob * total_area

        # Here comes the binary search
        left_bound, right_bound = 0, len(areas) - 1
        while left_bound < right_bound:
            mid = (left_bound + right_bound) // 2
            if sample_pos <= prefix_sum[mid]:
                right_bound = mid
            else:
                left_bound = mid + 1


        target_surface = right_bound

        # Sample point on the surface
        v1, v2, v3 = mesh.faces[target_surface]

        v1 = mesh.vertices[v1]
        v2 = mesh.vertices[v2]
        v3 = mesh.vertices[v3]

        edge_vec1 = np.array(v2) - np.array(v1)
        edge_vec2 = np.array(v3) - np.array(v1)

        prob_vec1, prob_vec2 = random.random(), random.random()
        if prob_vec1 + prob_vec2 > 1:
            prob_vec1 = 1 - prob_vec1
            prob_vec2 = 1 - prob_vec2

        target_point = np.array(v1) + (edge_vec1 * prob_vec1 + edge_vec2 * prob_vec2)
        # Random picking point in a triangle: http://mathworld.wolfram.com/TrianglePointPicking.html

        sample_points.append(target_point)


    if args.normalize:
        print('Apply normalization to unit ball')
        norms = np.linalg.norm(sample_points, axis=1)
        max_norm = max(norms)
        print('max norm: ', max_norm)
        sample_points /= max_norm

    for points in sample_points:
        output.write( ' '.join(["%.4f" % _ for _ in points]) )
        output.write('\n')
