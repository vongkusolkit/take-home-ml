import numpy as np
from flask import Flask, request, jsonify, send_file
import matplotlib
import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route('/points', methods=['POST'])
def get_points():
    """
    A method to calculates pixel coordinate values for an image
    that is to be displayed on a two dimensional surface given
    the dimensions of the image and the corner points of the
    image as it is to be displayed.

    params:
    - dimensions: a tuple defining the height and width of the image in terms of pixel counts.
                - Format example of image dimensions of 3x3: (3, 3)

    - corner_points: a list of two-element tuples defining the x and y coordinates of the
                     image corner points of the displayed image.
                - Format example of four corner points to display image: (1, 1), (3, 1), (1, 3), (3, 3)
    """
    try:
        body = request.get_json()
        dimensions = eval(body["dimensions"])
        corner_points = eval(body["corner_points"])
        assert type(dimensions) is tuple
        assert (dimensions[0] > 0 and dimensions[1] > 0) and (type(dimensions[0]) is int and type(dimensions[1]) is int)
        assert type(corner_points) is list
        assert len(corner_points) == 4

    except AssertionError:
        return jsonify({'error': '"dimensions" must be a string of tuple consisting of positive int; '
                                 '"corner_points" must be a string of list of tuple (4 coordinates)'}), 400
    except KeyError:
        return jsonify({'error': 'Invalid key in request body'}), 400

    except Exception:
        return jsonify({'error': 'Invalid request'}), 400

    return get_points_helper(corner_points, dimensions)


@app.route('/plot', methods=['POST'])
def plot_points():
    """
    A method to calculates pixel coordinate values for an image
    that is to be displayed on a two dimensional surface given
    the dimensions of the image and the corner points of the
    image as it is to be displayed.

    params:
    - dimensions: a tuple defining the height and width of the image in terms of pixel counts.
                - Format example of image dimensions of 3x3: (3, 3)

    - corner_points: a list of two-element tuples defining the x and y coordinates of the
                     image corner points of the displayed image.
                - Format example of four corner points to display image: (1, 1), (3, 1), (1, 3), (3, 3)
    """
    try:
        body = request.get_json()
        dimensions = eval(body["dimensions"])
        corner_points = eval(body["corner_points"])

    except Exception:
        jsonify({'error': 'Invalid request'}), 400
    return get_points_helper(corner_points, dimensions, plot=True)


def get_points_helper(corner_points, dimensions, plot=False):
    """
        A method to the get the x and y coordinates which are evenly spaced
        according to the dimensions within the rectangle defined by the corner points.

        params:
            - list of two-element tuples defining the x and y coordinates
                  of the image corner points of the displayed image
                  (e.g., four (x, y) pairs)
            - a tuple defining the height and width of the image in terms of pixel counts
                  defined by (rows, columns).
        return:
            - array of x coordinate points
            - array of y coordinate points
            - list of coordinates of the four corners in the following order:
              bottom left, top left, bottom right, top right
    """

    max_x = max(corner_points)[0]
    max_y = max(corner_points)[1]
    min_x = min(corner_points)[0]
    min_y = min(corner_points)[1]
    corner_list = [(min_x, min_y), (min_x, max_y), (max_x, min_y), (max_x, max_y)]
    x_coord = np.round(np.linspace(min_x, max_x, dimensions[0]), 2)
    y_coord = np.round(np.linspace(min_y, max_y, dimensions[1]), 2)
    x, y = np.meshgrid(x_coord, y_coord)
    if plot:
        return plot_points_helper(x, y, corner_list)
    coord = np.array((x.ravel(), y.ravel())).T
    coord_reshape = coord.reshape(dimensions[0], dimensions[1], 2)  # shape mxnx2

    return jsonify(coord_reshape.tolist()), 200


def plot_points_helper(x, y, corner_list):
    """
        A method to plot each pixel in the input image such that
        the pixels are evenly spaced within the rectangle
        defined by the corner points.

        params: list of x and y coordinates (x, y)
    """
    matplotlib.use('Agg')
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    #     if want to annotate every coordinate points
    #     for xy in zip(x.ravel(), y.ravel()):
    #        ax.annotate('(%.2f, %.2f)' % xy, xy=xy, ha='center', va='bottom')

    # add coordinate points to plot for corner points
    ax.text(corner_list[0][0], corner_list[0][1], "{}".format(corner_list[0]), ha='center', va='bottom')
    ax.text(corner_list[1][0], corner_list[1][1], "{}".format(corner_list[1]), ha='center', va='bottom')
    ax.text(corner_list[2][0], corner_list[2][1], "{}".format(corner_list[2]), ha='center', va='bottom')
    ax.text(corner_list[3][0], corner_list[3][1], "{}".format(corner_list[3]), ha='center', va='bottom')

    # set the frame of the plot
    ax.set(xlim=(min(x[0]) - 0.5, max(x[0]) + 0.5), ylim=(min(y[0]) - 0.5, max(y[-1]) + 0.5))

    plt.savefig('plot.png', format='png')
    plt.close()
    return send_file('plot.png', mimetype='image/png')
    # return jsonify({"success": "Successfully created plot.png"}), 200


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)
