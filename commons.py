from shapely.geometry import Polygon as ShapelyPolygon

'''
The following classes and functions are used to extract lines from aws and azure jsons.
'''

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Polygon:
    def __init__(self, points_list: list[int]):
        # points_list is a list like [x1, y1, x2, y2, x3, y3, ...]
        self.points = []
        assert len(points_list) % 2 == 0
        for i in range(0, len(points_list), 2):
            self.points.append(Point(points_list[i], points_list[i+1]))

    def to_shapely(self):
        return ShapelyPolygon([(p.x, p.y) for p in self.points])

class Line:
    '''
    TODO: I'm using polygons ans spans as lists because maybe in the future we will merge different lines like in the following example:
    "lines": [
        {
            "content": "L",
            "polygon": [...],
            "spans": [...]
        },
        {
            "content": "A COMMISSIONE per l'Energia Atomica",
            "polygon": [...],
            "spans": [...]
        }
    ]
    '''    
    def __init__(self, polygons: list[Polygon], content: str, confidence: float, spans: list = [], is_caption: bool = False):
        self.polygons = polygons
        self.spans = spans # aws doesn't have spans
        self.content = content
        self.confidence = confidence
        self.is_caption = is_caption

    def get_polygon(self):
        return self.polygons[0]

def compute_overlap_percentage(polygon1: Polygon, polygon2: Polygon) -> float:
    shapely_poly1 = polygon1.to_shapely()
    shapely_poly2 = polygon2.to_shapely()
    if not shapely_poly1.is_valid or not shapely_poly2.is_valid:
        return 0
    intersection_area = shapely_poly1.intersection(shapely_poly2).area
    poly1_area = shapely_poly1.area
    if poly1_area == 0:
        return 0
    return intersection_area / poly1_area

def is_line_inside_figure(line_polygon: Polygon, figures_polygons: list[Polygon], threshold: float = 0.8) -> bool:
    for figure_polygon in figures_polygons:
        # TODO: is this the overlap that we want to compute? maybe we want to merge all the polygons of the figure?
        overlap_percentage = compute_overlap_percentage(line_polygon, figure_polygon)
        if overlap_percentage >= threshold:
            return True
    return False

def gpt_is_caption(paragraph: str) -> bool:
    # TODO: implement asking GPT
    return False