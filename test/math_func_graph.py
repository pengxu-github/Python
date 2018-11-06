import matplotlib.pyplot as pl
import numpy

"""
        <item>1</item>
        <item>32</item>
        <item>64</item>
        <item>128</item>
        <item>256</item>
        <item>384</item>
        <item>512</item>
        <item>640</item>
        <item>768</item>
        <item>896</item>
        <item>1024</item>
        <item>2048</item>
        <item>4096</item>
        <item>6144</item>
        <item>8192</item>
        <item>10240</item>
        <item>12288</item>
"""
# x = [1, 32, 64, 128, 256, 384, 512, 640, 768, 896, 1024, 2048, 4096, 6144, 8192, 10240, 12288]
x = [1, 32, 64, 128, 256, 384, 512, 640, 768, 896, 1024, 2048]
"""
        <item>32</item>
        <item>64</item>
        <item>98</item>
        <item>104</item>
        <item>110</item>
        <item>116</item>
        <item>122</item>
        <item>128</item>
        <item>134</item>
        <item>182</item>
        <item>255</item>
        <item>255</item>
        <item>255</item>
        <item>255</item>
        <item>255</item>
        <item>255</item>
        <item>255</item>
        <item>255</item>
        <item>255</item>
"""
# y = [1, 32, 64, 98, 104, 110, 116, 122, 128, 134, 182, 255, 255, 255, 255, 255, 255]
y = [1, 32, 64, 98, 104, 110, 116, 122, 128, 134, 182, 255]

pl.plot(x, y)
# show the plot on the screen
# pl.show()
a = numpy.log(80 / 255) / numpy.log(10 / 255)
print('numpy.log(80 / 255) / numpy.log(10 / 255) = {}'.format(a))


