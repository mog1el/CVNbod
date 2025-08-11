def extended(landmarks, tip, pip):
    if tip == 4:
        tip = landmarks[4]
        mcp = landmarks[2]
        indexmcp = landmarks[5]

        disttipmcp2 = (tip.x - indexmcp.x)**2 + (tip.y - indexmcp.y)**2
        disttpimcpind2 = (mcp.x - indexmcp.x)**2 + (mcp.y - indexmcp.y)**2

        return disttipmcp2 > disttpimcpind2
    
    tip = landmarks[tip]
    pip = landmarks[pip]
    wrist = landmarks[0] 

    distip2 = (tip.x - wrist.x)**2 + (tip.y - wrist.y)**2
    distpip2 = (pip.x - wrist.x)**2 + (pip.y - wrist.y)**2

    return distip2 > distpip2

def gesture(landmarks):
    if landmarks == False:
        return "none"
    indtip, indpip = 8, 6
    midtip, midpip = 12, 10
    ringtip, ringpip = 16, 14
    pinkytip, pinkypip = 20, 18

    thumb_open = extended(landmarks, 4, 2)
    index_open = extended(landmarks, indtip, indpip)
    middle_open = extended(landmarks, midtip, midpip)
    ring_open = extended(landmarks, ringtip, ringpip)
    pinky_open = extended(landmarks, pinkytip, pinkypip)

    if thumb_open and index_open and middle_open and ring_open and pinky_open:
        return "all"
    elif thumb_open and not index_open and not middle_open and not ring_open and not pinky_open:
        return "thumb"
    elif not thumb_open and index_open and not middle_open and not ring_open and not pinky_open:
        return "index"
    elif not thumb_open and not index_open and middle_open and not ring_open and not pinky_open:
        return "middle"
    elif not thumb_open and index_open and middle_open and not ring_open and not pinky_open:
        return "out"
    elif not thumb_open and not index_open and not middle_open and not ring_open and pinky_open:
        return "pinky"
    else:
        return "none"