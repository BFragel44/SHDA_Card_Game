import pyxel

select_box = [96, 4, 65, 33,]

def box_click(x: int, y: int, w: int, h: int):
    """
    Helper function that returns True if
    mouse click is registered within the
    boundaries.

    Args:
        x (int): rectangle x value
        y (int): rectangle y value
        w (int): rectangle width value
        h (int): rectangle height value

    Returns:
        boolean: True if mouse click registers within boundaries
    """    
    x2 = x+w
    y2 = y+h
    if (pyxel.mouse_x > x and 
        pyxel.mouse_x < x2 and 
        pyxel.mouse_y > y and 
        pyxel.mouse_y < y2):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return True
    return False

def phase_box_click():
    """
    Helper function that returns True if
    mouse click is registered within the
    boundaries of the "Phase Box".

    Returns:
        boolean: True if mouse click registers within boundaries
    """
    x = select_box[0]
    y = select_box[1]
    w = select_box[2]
    h = select_box[3]
    x2 = x+w
    y2 = y+h
    if box_click(x, y, w, h):
            return True
    return False