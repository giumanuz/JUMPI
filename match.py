from itertools import combinations
import matplotlib.pyplot as plt
import random

def merge_bounding_boxes(boxes):
    """
    Funzione per unire bounding box rappresentati da 4 punti (ognuno con coordinate x, y).
    """
    if not boxes:
        return None
    x_min = min(point[0] for box in boxes for point in box)
    y_min = min(point[1] for box in boxes for point in box)
    x_max = max(point[0] for box in boxes for point in box)
    y_max = max(point[1] for box in boxes for point in box)
    return [(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)]

def generate_combinations(bounding_boxes):
    """
    Genera tutte le combinazioni possibili di bounding box.
    """
    all_combinations = []
    for i in range(1, len(bounding_boxes) + 1):
        all_combinations.extend(combinations(bounding_boxes, i))
    return all_combinations

def calculate_area(box):
    """
    Calcola l'area di un bounding box rappresentato da 4 punti (ognuno con coordinate x, y).
    """
    width = box[1][0] - box[0][0]
    height = box[2][1] - box[0][1]
    return width * height

def find_minimal_bounding_box_match(set1, set2):
    """
    Trova l'accoppiamento tra bounding box di set1 e set2 che forma il riquadro più piccolo.
    """
    set1_combinations = generate_combinations(set1)
    set2_combinations = generate_combinations(set2)
    
    min_area = float('inf')
    best_match = None
    
    # Trova il bounding box minimo combinando set1 e set2
    for comb1 in set1_combinations:
        for comb2 in set2_combinations:
            merged_box1 = merge_bounding_boxes(comb1)
            merged_box2 = merge_bounding_boxes(comb2)
            
            # Calcola il bounding box che copre sia merged_box1 che merged_box2
            combined_box = merge_bounding_boxes([merged_box1, merged_box2])
            area = calculate_area(combined_box)
            
            # Aggiorna il match migliore se l'area è minore
            if area < min_area:
                min_area = area
                best_match = (merged_box1, merged_box2)
    
    return best_match, min_area

def plot_bounding_boxes(set1, set2, best_match):
    """
    Funzione per disegnare i bounding box di due insiemi con colori diversi e evidenziare il match migliore.
    """
    colors = ["red", "blue", "green", "orange", "purple", "brown"]
    plt.figure()

    # Disegna i bounding box del primo insieme
    for box in set1:
        color = random.choice(colors)
        x_coords = [point[0] for point in box] + [box[0][0]]
        y_coords = [point[1] for point in box] + [box[0][1]]
        plt.plot(x_coords, y_coords, color=color, label="Set 1")

    # Disegna i bounding box del secondo insieme
    for box in set2:
        color = random.choice(colors)
        x_coords = [point[0] for point in box] + [box[0][0]]
        y_coords = [point[1] for point in box] + [box[0][1]]
        plt.plot(x_coords, y_coords, color=color, linestyle="--", label="Set 2")

    # Disegna il match migliore
    if best_match:
        merged_box1, merged_box2 = best_match
        combined_box = merge_bounding_boxes([merged_box1, merged_box2])
        x_coords = [point[0] for point in combined_box] + [combined_box[0][0]]
        y_coords = [point[1] for point in combined_box] + [combined_box[0][1]]
        plt.plot(x_coords, y_coords, color="black", linewidth=2, label="Best Match")

    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")
    plt.title("Bounding Boxes degli Insiemi 1 e 2 con il Match Migliore")
    plt.legend()
    plt.grid()
    plt.show()

# Test case
def test_find_minimal_bounding_box_match():
    set1 = [
        [(0, 0), (2, 0), (2, 2), (0, 2)],
        [(3, 3), (5, 3), (5, 5), (3, 5)]
    ]
    set2 = [
        [(1, 1), (4, 1), (4, 4), (1, 4)],
        [(6, 6), (8, 6), (8, 8), (6, 8)]
    ]
    best_match, min_area = find_minimal_bounding_box_match(set1, set2)
    print("Best Match:", best_match)
    print("Minimal Area:", min_area)
    plot_bounding_boxes(set1, set2, best_match)

test_find_minimal_bounding_box_match()
