import matplotlib.pyplot as plt
from plotter import Plotter


def plot_polygon():
    with open('polygon.csv', 'r') as f:
        plot = f.readlines()[1:]
        polygon_x_all = []
        polygon_y_all = []
        polygon_id_all = []
        for row in plot:
            each_rows = row.strip('\n')
            each_row = each_rows.split(',')
            polygon_id = each_row[0]
            polygon_x = each_row[1]
            polygon_y = each_row[2]
            polygon_id_all.append(polygon_id)
            polygon_x_all.append(float(polygon_x))
            polygon_y_all.append(float(polygon_y))
    return polygon_id_all, polygon_x_all, polygon_y_all


def mbr():
    p = plot_polygon()
    a = p[1]
    b = p[2]
    xmax = max(a)
    xmin = min(a)
    ymax = max(b)
    ymin = min(b)
    return [xmax, xmin, xmin, xmax, xmax], [ymax, ymax, ymin, ymin, ymax]


def point_list():
    with open('input.csv', 'r') as f:
        plot1 = f.readlines()[1:]
        point_x_all = []
        point_y_all = []
        point_id_all = []
        location = []
        for row1 in plot1:
            each_rows1 = row1.strip('\n')
            each_row1 = each_rows1.split(',')
            point_id = each_row1[0]
            point_x = each_row1[1]
            point_y = each_row1[2]
            point_id_all.append(point_id)
            point_x_all.append(float(point_x))
            point_y_all.append(float(point_y))
            location.append('null')
    return [point_id_all, point_x_all, point_y_all, location]


def outside_mbr():
    p = point_list()
    xmax = mbr()[0][0]
    xmin = mbr()[0][1]
    ymax = mbr()[1][0]
    ymin = mbr()[1][2]
    for i in range(len(point_list()[1])):
        xi = p[1][i]
        yi = p[2][i]
        if xi < xmin or xi > xmax or yi < ymin or yi > ymax:
            p[3][i] = 'outside'
        else:
            p[3][i] = 'inside'
    return p


def show_polygon():
    m = mbr()
    p = plot_polygon()
    plt.plot(m[0], m[1])


def rca():
    point_polygon = plot_polygon()[1:]

    p = outside_mbr()

    for i in range(len(p[0])):
        x = p[1][i]
        y = p[2][i]
        id = p[0][i]
        crosstime = 0
        for n in range(len(point_polygon[0]) - 1):
            x1 = point_polygon[0][n]
            y1 = point_polygon[1][n]
            x2 = point_polygon[0][n + 1]
            y2 = point_polygon[1][n + 1]

            if y1 == y2 == y and x1 == x2 == x:
                p[3][i] = 'boundary'
            elif (x1 == x and y == y1) or (x2 == x and y2 == y):
                p[3][i] = 'boundary'
            elif x == x1 == x2 and (y1 < y < y2 or y2 < y < y1):
                p[3][i] = 'boundary'
            elif y == y1 == y2 and (x1 < x < x2 or x2 < x < x1):
                p[3][i] = 'boundary'
            elif y1 <= y < y2 or y2 <= y < y1:
                inter = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                if inter == x:
                    p[3][i] = 'boundary'
                elif inter > x:
                    crosstime += 1

        if crosstime % 2 == 0 and p[3][i] != 'boundary':
            p[3][i] = 'outside'
        elif crosstime % 2 != 0 and p[3][i] != 'boundary':
            p[3][i] == 'inside'

    return p


def output():
    p = rca()
    with open('output', 'w') as output:
        output.write('ID' + ',' + 'category' + '\n')
        for i in range(len(p[0])):
            output.write(p[0][i] + ',' + p[3][i] + '\n')


def main():
    plotter = Plotter()
    print('read polygon.csv')
    plot_polygon()
    print('read input.csv')
    point_list()
    print('categorize points')
    rca()
    print('write output.csv')
    output()
    print('plot polygon and points')
    m = mbr()
    p = plot_polygon()
    plotter.add_polygon(p[1], p[2])
    plt.plot(m[0], m[1])
    p = rca()
    for i in range(len(p[0])):
        plotter.add_point(p[1][i], p[2][i], p[3][i])

    plotter.show()


if __name__ == '__main__':
    main()

