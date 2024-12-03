from shapely.geometry import Polygon as ShapelyPolygon

'''
The following classes are used to extract lines from azure jsons.
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
    """
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
    """
    def __init__(self, polygons: list[Polygon], content: str, confidence: float, spans: list = [], is_caption: bool = False):
        self.polygons = polygons
        self.spans = spans
        self.content = content
        self.confidence = confidence
        self.is_caption = is_caption

    def get_polygon(self):
        return self.polygons[0]