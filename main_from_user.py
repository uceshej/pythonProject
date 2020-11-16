import matplotlib.pyplot as plt
from plotter import Plotter

def read_polygon():    #get each point of the polygon
    with open('polygon.csv','r') as f:
        plot=f.readlines()[1:]
        polygon_x_all=[]
        polygon_y_all=[]
        polygon_id_all=[]
        for row in plot:
            each_rows=row.strip('\n')
            each_row=each_rows.split(',')
            polygon_id=each_row[0]
            polygon_x=each_row[1]
            polygon_y=each_row[2]
            polygon_id_all.append(polygon_id)
            polygon_x_all.append(float(polygon_x))
            polygon_y_all.append(float(polygon_y))
    return polygon_id_all,polygon_x_all,polygon_y_all

def mbr():     #get the Minimum Bounding Rectangle of the polygon
    p=read_polygon()
    a=p[1]
    b=p[2]
    xmax=max(a)
    xmin=min(a)
    ymax=max(b)
    ymin=min(b)
    return [xmax,xmin,xmin,xmax,xmax],[ymax,ymax,ymin,ymin,ymax]


def main():
    plotter = Plotter()
    print("read polygon.csv")
    read_polygon()
    #get the input point
    print("Insert point information")
    x = float(input("x coordinate: "))
    y = float(input("y coordinate: "))
    point=[x,y,'location']
    print("categorize point")
    #Classify the test points outside and inside the MBR.
    mbr()
    xmax = mbr()[0][0]
    xmin = mbr()[0][1]
    ymax = mbr()[1][0]
    ymin = mbr()[1][2]
    if x< xmin or x > xmax or y < ymin or y > ymax:
        point[2] = 'outside'
    else:
        point[2] = 'inside'
    # Classfily all the points outside,inside and on the boundary
    point_polygon = read_polygon()[1:]
    crosstime = 0
    for n in range(len(point_polygon[0]) - 1):
        x1 = point_polygon[0][n]
        y1 = point_polygon[1][n]
        x2 = point_polygon[0][n + 1]
        y2 = point_polygon[1][n + 1]
        # check whether the point coincides with the vertex of the polygon
        if y1 == y2 == y and x1 == x2 == x:
            point[2] = 'boundary'
        elif (x1 == x and y == y1) or (x2 == x and y2 == y):
            point[2] = 'boundary'
        # check whether the point is on vertical segments
        elif x == x1 == x2 and (y1 < y < y2 or y2 < y < y1):
            point[2] = 'boundary'
        # check whether the point is on horizontal segments
        elif y == y1 == y2 and (x1 < x < x2 or x2 < x < x1):
            point[2] = 'boundary'
        # check the common situation
        elif y1 <= y < y2 or y2 <= y < y1:
            inter = (y - y1) * (x2 - x1) / (y2 - y1) + x1
            if inter == x:
                point[2] = 'boundary'
            elif inter > x:
                crosstime += 1

        if crosstime % 2 == 0 and point[2] != 'boundary':
            point[2] = 'outside'
        elif crosstime % 2 != 0 and point[2] != 'boundary':
            point[2] == 'inside'
    # Draw the polygon and points
    print("plot polygon and point")
    m = mbr()
    p = read_polygon()
    plotter.add_polygon(p[1], p[2])
    plt.plot(m[0], m[1])
    plotter.add_point(x,y,point[2])
    plotter.show()

if __name__ == "__main__":
    main()