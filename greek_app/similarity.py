import numpy as np
from scipy.spatial.distance import directed_hausdorff
import similaritymeasures


def create_xy_coords(key,sketchpadJSON):
    xy_coords = []
    pos = (0,0)
    #read through the data and create x,y tuples
    for stroke in sketchpadJSON["strokes"]:
        for line in stroke['lines']:
            xy_coords.append((line['start']['x'] - pos[0], line['start']['y'] - pos[1]))

            xy_coords.append((line['end']['x'] - pos[0], line['end']['y'] - pos[1]))
            pos = (line['end']['x'], line['end']['y'])
     
    x = [x[0] for x in xy_coords]
    y = [y[1] for y in xy_coords]
    return (x,y)

def similarity(sketch, other_sketch):
    """
    sketch = sketchpad json output
    other_sketch = saved json output from Django 
    """
    result = {}
    x,y = create_xy_coords('search',sketch)
    P = np.array([x, y]).T
    
    key = other_sketch.id
    x1,y1 = create_xy_coords(key,other_sketch)
    Q = np.array([x1, y1]).T
    dh, ind1, ind2 = directed_hausdorff(P, Q)
    df = similaritymeasures.frechet_dist(P, Q)
    dtw, d = similaritymeasures.dtw(P, Q)
    pcm = similaritymeasures.pcm(P, Q)
    area = similaritymeasures.area_between_two_curves(P, Q)
    cl = similaritymeasures.curve_length_measure(P, Q)

    result[key] = {"dh":dh, "df":df, "dtw":dtw, "pcw":pcm, "cl":cl, "area":area}
    return result
