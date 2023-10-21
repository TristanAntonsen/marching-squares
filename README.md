# marching-squares

An implementation of Marching Squares. Marching Squares is an algorithm that extracts edges from a function/field or 2D grid of values. This algorithm is useful whenever edge or boundary data is needed (toolpaths, for example).

<img src="sample-images/banner.png">


The size of the sampling grid determines the "resolution" and thus the maximum deviation from the "actual" boundary the resulting edges will have.

Marching Squares is a 2D version of "Marching Cubes", which is common in extracting surfaces as triangle meshes from 3D functions and discrete 3D data such as MRI and CT scans.


---

*Extracting the edges of an implicit circle defined by a signed distance function. The dot colors represent the values at each sampling location and the cyan lines are the extracted boundary.*

**Note: The only output of Marching Squares is the cyan line segments. The rest of what's shown in the images is for visualization only.*

Here is an example of different grid/marching square sizes:

||3|5|20|50|
|:--:|:--:|:--:|:--:|:--:|
|Midpoints only|<img src="sample-images/marched3_nointerp.png">|<img src="sample-images/marched5_nointerp.png">|<img src="sample-images/marched20_nointerp.png">|<img src="sample-images/marched50_nointerp.png">|
|Interpolated|<img src="sample-images/marched3.png">|<img src="sample-images/marched5.png">|<img src="sample-images/marched20.png">|<img src="sample-images/marched50.png">|

---

<img src="sample-images/marched_circle.png">

*The above images uses interpolation to "smooth" the boundary. If only midpoints between sampling locations are used, then the following result is produced:*

<img src="sample-images/marched_no_interp.png">

*Discrete data, such as with an image, can be used as well. This example extracts the boundary of green regions. The image was first box blurred prior to sampling to allow interpolation to smooth the boundary.*

<img src="sample-images/marched_img_red.png">

---

References: 
- http://paulbourke.net/geometry/polygonise/
- https://thecodingtrain.com/challenges/c5-marching-squares
- https://en.wikipedia.org/wiki/Marching_squares