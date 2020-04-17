from tkinter import Tk,filedialog
import sys
import cv2
import imghdr
class notImage(Exception):
    '''Raised when input is not Image'''
    pass

def accepted():
    ans = input()
    if( ans == 'yes' or ans == 'y' or ans == 'Y' or ans == 'Yes' or ans =='ye' or ans=='YE'):
        return True
    return False

def verify_file(file_path):
    file_type = imghdr.what(file_path)
    if file_type == 'jpeg' or file_type == 'png' or file_type =='bmp' or file_type == 'rgb':
        return True
    else:
        return False

def get_path():
    Tk().withdraw()
    file_path = filedialog.askopenfilename()
    try:
        if verify_file(file_path):
            #print(file_path)
            return file_path
        else:
            print("Selected file may not be a image, do you want to to retry?\n(Yes/No)")
            if accepted():
                return get_path()
            else:
                raise notImage
    except notImage:
        sys.exit()
    except:
        print("Cancelled, do you want to to retry?\n(Yes/No)")
        if accepted():
            return get_path()
        else:
            sys.exit()