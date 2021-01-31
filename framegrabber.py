import win32gui, win32ui
from win32con import SRCCOPY
from numpy import fromstring

'''
https://gist.github.com/AndreVallestero/b08559cdc689d22587f6cf483e87e30f

Optimized to be 6 times faster using the following techniques
- Reuse bitmaps, handles, and device contexts
- Use the application framebuffer instead of the compositor frame buffer(entire desktop)

This is not the fastest method. That would be to directly copy the data from the GPU back buffer
- https://web.archive.org/web/20121205062922/http://www.ring3circus.com/blog/2007/11/22/case-study-fraps/
'''

class FrameGrabber():
    def __init__(self, x: int, y: int, w: int, h: int, windowTitle: str = ""):
        self.pos = (x, y)
        self.w = w
        self.h = h
        
        self.hwnd = win32gui.FindWindow(None, windowTitle) if windowTitle else win32gui.GetDesktopWindow()
        self.hwnddc = win32gui.GetWindowDC(self.hwnd)
        self.hdcSrc = win32ui.CreateDCFromHandle(self.hwnddc)
        self.hdcDest = self.hdcSrc.CreateCompatibleDC()

        self.bmp = win32ui.CreateBitmap()
        self.bmp.CreateCompatibleBitmap(self.hdcSrc, w, h)
        self.hdcDest.SelectObject(self.bmp)

    def grab(self):
        self.hdcDest.BitBlt((0, 0), (self.w, self.h), self.hdcSrc, self.pos, SRCCOPY)
        img = fromstring(self.bmp.GetBitmapBits(True), dtype='uint8')
        img.shape = (self.h ,self.w, 4)

        # To convert to RGB, use cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        # This is often unnecessary if simple image filtering is being done
        return img

    def __del__(self):
        self.hdcSrc.DeleteDC()
        self.hdcDest.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, self.hwnddc)
        win32gui.DeleteObject(self.bmp.GetHandle())
        
