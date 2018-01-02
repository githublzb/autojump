# autojump
An autojump script for wechat game

Device: Redmi 4x (script is Android only)
## The main idea of the script is:
### 1. Get the screenshot
Using adb toolkit to fetch the screenshot and pull it to computer.
### 2. Get chessman's position
The chessman has a specific color, maybe purple. So we can get the position of chessman's left down corner and estimate the start point for jump.
### 3. Get destination's position
First, we convert the image to HSV model and use Canny edge detection.<br>
Second, since objects seem place on a 30 degree straight line, we can simplify the problem. Just get the crossover point of the line and the object edge.
### 4. Jump
Calculate the distance between two points.</br>
We assume that the relationship between press time and distance is linear.The coefficient (press time/distance) is determineed by your screen size.</br> 
Use adb tookit to control the phone and JUMP!
