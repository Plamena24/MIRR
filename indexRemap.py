import rhinoscriptsyntax as rs

reordered = []


for diamond in diamonds:
    for index, point in enumerate(points):
        if rs.Distance(diamond, point) < 4.0:
            reordered.append(index)

print reordered

a = reordered