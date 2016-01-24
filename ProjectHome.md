Source code has moved to github: https://github.com/LouisPlisso/pytomo

Bundle downloads have moved to sourceforge: http://sourceforge.net/projects/pytomo/


---


We first select an initial list of videos that we would like to start the analysis with (most popular of the day/week/month/year/all\_time).

For the videos in this list the Pytomo tool first finds the IP address of the cache servers on which these videos are located. The cache server is pinged to obtain the RTT values.

Then we try to download the video for a limited amount of time to calculate the different statistics of the download (including a model of the number of interruptions seen by the user).


---


To contribute execute the program for how long you want (12 hours is a good value), and send me the log and database files by e-mail (pytomo@gmail.com).

Please tell me you country and your ISP so that I can correlate according to other data.


---


If you have a http proxy, launch the program from the command line (on Windows execute program `cmd`), change directory (`cd`) to the Pytomo code, and run
```
./start_crawl --http-proxy='http://my_proxy.my_adress.my_ext:8080'
```
assuming your proxy is named `my_proxy.my_adress.my_ext` and uses port 8080


---


Contributors:

  * Parikshit Juluri (modelisation and calibration of video playback)
  * Ana Oprea (visualisation interface)