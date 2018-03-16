import ocv
import io


def find(img):
    output = io.BytesIO()
    img.save(output, format='JPEG')
    imgBuf = output.getvalue()
    
    output.close()

    rects = ocv.analyze(imgBuf, debug=True)

    return rects
