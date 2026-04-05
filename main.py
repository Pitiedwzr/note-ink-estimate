import fitz  # PyMuPDF
import math

def point_dist(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def cubic_bezier_length(p0, p1, p2, p3, segments=10):
    """Approximates the length of a cubic Bezier curve."""
    length = 0
    prev_p = p0
    for i in range(1, segments + 1):
        t = i / segments
        # cubic bezier formula
        x = (1-t)**3 * p0.x + 3*(1-t)**2 * t * p1.x + 3*(1-t) * t**2 * p2.x + t**3 * p3.x
        y = (1-t)**3 * p0.y + 3*(1-t)**2 * t * p1.y + 3*(1-t) * t**2 * p2.y + t**3 * p3.y
        curr_p = fitz.Point(x, y)
        length += point_dist(prev_p, curr_p)
        prev_p = curr_p
    return length

def calculate_notes_metrics(doc):
    total_length_points = 0

    for page in doc:
        paths = page.get_drawings()
        for path in paths:
            for item in path["items"]:
                # line
                if item[0] == "l":
                    total_length_points += point_dist(item[1], item[2])

                # curve
                elif item[0] == "c":
                    total_length_points += cubic_bezier_length(item[1], item[2], item[3], item[4])

                # rectangles
                elif item[0] == "re":
                    r = item[1] # perimeter
                    total_length_points += (abs(r.width) + abs(r.height)) * 2

    # 1 pt = 1/72 inch, 1 inch = 25.4 mm
    total_length_meters = total_length_points * (25.4 / 72) / 1000
    return total_length_meters

file_path = "Assignment 1 2026S1.pdf"

try:
    pdf = fitz.open(file_path)
except Exception as e:
    raise f"Error opening file: {e}"

meters = calculate_notes_metrics(pdf)
pen_standard = 1000

print(f"Total pages: {pdf.pages_count}")
print(f"Total writing distance: {meters:.2f} meters")
print(f"Equivalent in pens:     {meters / pen_standard:.4f} pens")