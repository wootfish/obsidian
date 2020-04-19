import drawSvg as draw

def arrow(scale, color):
    marker = draw.Marker(-0.1, -0.5, 0.9, 0.5, scale=scale, orient='auto')
    marker.append(draw.Lines(-0.1, -0.5, -0.1, 0.5, 0.9, 0, fill=color, close=True))
    return marker
