# Raspberry Pi SPL meter
* Sound Pressure Level meter with RPI implemented with Python.
* Author: Seyoung Park
* E-mail: seyoung.arts.park@protonmail.com
* Date: 2016 Feb. 23rd



## Filter: A-weighting
I applied A-weighting to filter to filter the stream. A-weighting results frequencies which average person can hear. For further information read: [Frequency Weightings - A-Weighted, C-Weighted or Z-Weighted?](https://www.noisemeters.com/help/faq/frequency-weighting.asp)
For the actual programmatic implementation I borrowed the code from [endolith](https://gist.github.com/endolith/148112) and is saved as /spl_lib.py. A-weighting() is translated from [MATLAB script](: http://www.mathworks.com/matlabcentral/fileexchange/69).
