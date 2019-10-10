#! python
import time
import queue
import mss
import mss.tools
import pyHook
import pyautogui
import pythoncom
import multiprocessing
from dupe import Dupe
from enums import PosTrait
from enums import NegTrait
from enums import Interests

from PIL import Image

COMPARE_SKIP = 1
TRUE_THRESHOLD = 250
SHUFFLE_L_X = 933+10
SHUFFLE_M_X = 1338+10
SHUFFLE_R_X = 1743+10
SHUFFLE_Y = 406+10
SHUFFLE_WIDTH = 133
SHUFFLE_HEIGHT = 36
INTEREST_L_X = 828
INTEREST_M_X = 1233
INTEREST_R_X = 1638
INTEREST_T_Y = 613
INTEREST_M_Y = 634
INTEREST_B_Y = 655
INTEREST_WIDTH = 238
INTEREST_HEIGHT = 21

TRAIT_L_X = 828
TRAIT_M_X = 1233
TRAIT_R_X = 1638
NEG_TRAIT_Y = 521
POS_TRAIT_Y = 543
TRAIT_WIDTH = 238
TRAIT_HEIGHT = 18

print('Press F3 to quit.')


class Clicker(multiprocessing.Process):
    def loadImage(self, filename):
        im = Image.open(filename)
        pixels = []
        for i in im.getdata():
            pixels.append(float((i[0] + i[1] + i[2]))/3)  # set the colour accordingly
        imout = Image.new('L', im.size)
        imout.putdata(pixels)
        return imout

    def __init__(self, queue, interval):
        multiprocessing.Process.__init__(self)
        self.running = True
        self.q = queue
        self.click_interval = interval
        self.moleIm = self.loadImage('assets/positive_traits/molehands.bmp')
        self.quickIm = self.loadImage('assets/positive_traits/learn.bmp')
        self.twinkleIm = self.loadImage('assets/positive_traits/twinkletoes.bmp')
        self.buildIntIm = self.loadImage('assets/interests/build.bmp')
        self.digIntIm = self.loadImage('assets/interests/dig.bmp')
        self.resIntIm = self.loadImage('assets/interests/research.bmp')
        self.cookIntIm = self.loadImage('assets/interests/cook.bmp')
        self.dupel = Dupe()
        self.dupem = Dupe()
        self.duper = Dupe()
        self.dupes = [(self.dupel, TRAIT_L_X, INTEREST_L_X, SHUFFLE_L_X, 0), (self.dupem, TRAIT_M_X, INTEREST_M_X, SHUFFLE_M_X, 1), (self.duper, TRAIT_R_X, INTEREST_R_X, SHUFFLE_R_X, 2)]

    def collectImage(self, x, y, width, height):
        with mss.mss() as sct:
            # The screen part to capture
            monitor = {"top": y, "left": x, "width": width, "height": height}
            # Grab the data
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            return img

    def compareImages(self, im1, im2):
        mse = 0.0
        im1Data = list(im1.getdata())
        im2Data = list(im2.getdata())
        count = 0
        for i in range(0, len(im1Data)-1, COMPARE_SKIP):
            pa = float(im1Data[i][0]+im1Data[i][1]+im1Data[i][2])/3
            mse += (pa - im2Data[i]) ** 2
            count += 1
        mse = (float(mse) / count)
        if(TRUE_THRESHOLD > mse):
            return True
        else:
            return False

    def check_dig_int(self, intX):
        dig = False
        build = False
        w = INTEREST_WIDTH
        h = INTEREST_HEIGHT
        if(self.compareImages(self.collectImage(intX, INTEREST_T_Y, w, h), self.digIntIm)):
            dig = True
        elif(self.compareImages(self.collectImage(intX, INTEREST_M_Y, w, h), self.digIntIm)):
            dig = True
        elif(self.compareImages(self.collectImage(intX, INTEREST_B_Y, w, h), self.digIntIm)):
            dig = True

        if(dig):
            if (self.compareImages(self.collectImage(intX, INTEREST_T_Y, w, h), self.buildIntIm)):
                build = True
            elif(self.compareImages(self.collectImage(intX, INTEREST_M_Y, w, h), self.buildIntIm)):
                build = True
            elif(self.compareImages(self.collectImage(intX, INTEREST_B_Y, w, h), self.buildIntIm)):
                build = True

        print("Build:" + str(build) + " Dig:" + str(dig))
        if(build & dig):
            return True
        else:
            return False

    def check_res_int(self, intX):
        ret = False
        w = INTEREST_WIDTH
        h = INTEREST_HEIGHT
        im = self.collectImage(intX, INTEREST_T_Y, w, h)
        im.save("research.bmp")
        if (self.compareImages(self.collectImage(intX, INTEREST_T_Y, w, h), self.resIntIm)):
            ret = True
        elif (self.compareImages(self.collectImage(intX, INTEREST_M_Y, w, h), self.resIntIm)):
            ret = True
        elif (self.compareImages(self.collectImage(intX, INTEREST_B_Y, w, h), self.resIntIm)):
            ret = True

        print("Research:" + str(ret))
        return ret

    def check_cook_int(self, intX):
        ret = False
        w = INTEREST_WIDTH
        h = INTEREST_HEIGHT
        if (self.compareImages(self.collectImage(intX, INTEREST_T_Y, w, h), self.cookIntIm)):
            ret = True
        elif (self.compareImages(self.collectImage(intX, INTEREST_M_Y, w, h), self.cookIntIm)):
            ret = True
        elif (self.compareImages(self.collectImage(intX, INTEREST_B_Y, w, h), self.cookIntIm)):
            ret = True

        print("Cook:" + str(ret))
        return ret

    def check_pos_trait(self, im):
        ret = PosTrait.UNKNOWN
        if(self.compareImages(im, self.moleIm)):
            ret = PosTrait.MOLE
        elif(self.compareImages(im, self.quickIm)):
            ret = PosTrait.LEARNER
        elif(self.compareImages(im, self.twinkleIm)):
            ret = PosTrait.TWINKLE
        return ret

    def check_interest(self, im):
        ret = Interests.NONE
        if(self.compareImages(im, self.buildIntIm)):
            ret = Interests.BUILD
        elif(self.compareImages(im, self.digIntIm)):
            ret = Interests.DIG
        elif (self.compareImages(im, self.resIntIm)):
            ret = Interests.RESEARCH
        elif (self.compareImages(im, self.cookIntIm)):
            ret = Interests.COOK
        return ret

    def run(self):
        skip = [False, False, False]
        has_mole = False
        has_learner = False
        has_twinkle = False
        while self.running:
            try:
                task = self.q.get(block=False)
                if task == "exit":
                    print("Clicker Exiting")
                    self.q.task_done()
                    self.running = False
            except queue.Empty:
                time.sleep(self.click_interval)
                #check L

                for d in self.dupes:
                    if not skip[d[4]]:
                        d[0].postrait = self.check_pos_trait(self.collectImage(d[1], POS_TRAIT_Y, TRAIT_WIDTH, TRAIT_HEIGHT))

                        if(d[0].postrait == PosTrait.MOLE) and (not has_mole):
                            print("Found Molehands")
                            if not(self.check_dig_int(d[2])):
                                pyautogui.click(x=d[3], y=SHUFFLE_Y)
                            else:
                                has_mole = True
                                skip[d[4]] = True;
                                print("Confirmed")
                        elif (d[0].postrait == PosTrait.LEARNER) and (not has_learner):
                            print("Found Quick Learner")
                            if not(self.check_res_int(d[2])):
                                pyautogui.click(x=d[3], y=SHUFFLE_Y)
                            else:
                                has_learner = True
                                skip[d[4]] = True;
                                print("Confirmed")
                        elif (d[0].postrait == PosTrait.TWINKLE) and (not has_twinkle):
                            print("Found Twinkletoes")
                            if not(self.check_cook_int(d[2])):
                                pyautogui.click(x=d[3], y=SHUFFLE_Y)
                            else:
                                has_twinkle = True
                                skip[d[4]] = True;
                                print("Confirmed")
                        else:
                            pyautogui.click(x=d[3], y=SHUFFLE_Y)

                if has_mole and has_learner and has_twinkle:
                    print("Done!")
        return


def OnKeyboardEvent(event):
    key = event.Key

    if key == "F10":
        print("Starting auto clicker")
        # Start consumers
        clicker = Clicker(queue, 0.001)
        clicker.start()
    elif key == "F4":
        print("Stopping auto clicker")
        # Add exit message to queue
        queue.put("exit")
        # Wait for all of the tasks to finish
        queue.join()

    # return True to pass the event to other handlers
    return True


if __name__ == '__main__':
    # Establish communication queues
    queue = multiprocessing.JoinableQueue()
    # create a hook manager
    hm = pyHook.HookManager()
    # watch for all mouse events
    hm.KeyDown = OnKeyboardEvent
    # set the hook
    hm.HookKeyboard()
    # wait forever
    pythoncom.PumpMessages()
