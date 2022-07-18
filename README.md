DataCollection


The DataCollection repo has three scripts; rs_canvas.py’, ‘python_tkinter.py’ and ‘file_var.py’. The  ‘collectionRequirements.txt’ file has the dependencies needed to run the code. You can do a 
‘pip install -r  AnnotationRequirement.txt’ to download them on your machine.



    1. Plug the sensor (we used D435i sensor) and run the ‘rs_canvas.py’ file. The visual window coverage of the sensor will be displayed (Have enough strawberries at a time for image capture – it saves time). 
    2. Hold the sensor at a distance of approximately 15 cm where the depth of the strawberries alone will be most visible (where the depth is red on the strawberries in view). 
    3. Click on the window to save.
    4. Another visual window will be displayed. Move the sensor to about 10 cm of the strawberry
    5. Click to save the window
    6. The last window will appear, move the sensor backwards till the depth contours are about to disappear and click. I think it is about 25cm away from the strawberries 
    7. Click to save windows

After the third click, the tkinter window will pop up for data collection of each strawberries  

When the tkinter screen pops after taking the images, You will type values of the berry ID, the berry height, the berry minumum width, berry maximum width and the weight of the berry. These will be typed with space in between them.  For example, a valid data input is  
1 2.23 1.39 1.6 12

    1. The berry_ID can be integers 1 or 2 or 3…
    2. The height of the berry as measured by the vernier caliper

    ![alt text](./height.png?raw=true "Height measurement")

    3. The minimum width which is the shortest width around the top corner
    4. The maximum width which is the widest width around the top corner of the berry
    5. The weight of the berry
NB: When you make an error of using previous berry_ID. You will be notified. Data collection is also done for just one of the three images you captured. If you have made a mistake during data collection, go to your file system and delete the folder for the berry_ID

Run the script again to collect data for another berry_ID



ANNOTATION

This repo contains scripts for data collection and annotation

The ‘Annotation’ folder has the ‘StrawberryAnnotation.py’ script where you find the script to run. This annotation also incorporates means to detection of the strawberries. 

Before running the ‘StrawberryAnnotation.py’ script, make sure the images are segmented and you have the dependencies.

The ‘AnnotationRequirement.txt’ has the dependencies needed to run the code. 

The RGB Images to be annotated are found in the ‘train/img’ directory while its segmented counterpart are found in ‘train/label’ directory. The annotated data is found in the ‘dump’ directory.

To annotate, run the ‘StrawberryAnnotation.py’ script. For this project, we have 5 ‘annotation points’; the PickingPoint, Top, Bottom, Left grasping point and Right grasping point. We annotate in this exact order. From the figure below (considering the ripe berry), the top end of the cyan colour is the Picking point, the point where the cyan colour ends and the yellow line begins is the Top, the Bottom is indicated by the end of the yellow line; the far left of the blue line is the  Left grasping point and the far right of the blue line is the  Right grasping point.

    ![alt text](./icra.png?raw=true "Images with picking points")

Rules of annotation

    1) Annotate in the order as explained above
    2) Change the data_dir and dump_dir variables in the ‘StrawberryAnnotation.py’ script
    3) To annotate a point, you need to right-click twice
    4) When you double click, you can push any of letter ‘z’, ‘x’, ‘c’, or ‘v’
        1. ‘z’ means the point selected is visible (e.g the bottom of the ripe berry in the figure above)
        2. ‘x’ means the point is blocked by another berry/leaf
        3. ‘c’ means the point is blocked by itself (e.g the top of the ripe berry isn’t visible and blocked by itself)
        4. ‘v’ means point is totally obscure. Probably only a fraction of the berry is in the viewing screen
    5) After obtaining (3) above, push any of letters ‘q’ or ‘w’. ‘q’ means the berry is ripe while ‘w’  means the berry is unripe. The next segmented berry/image will pop up to continue annotation.  
