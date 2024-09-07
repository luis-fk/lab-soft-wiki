#My-Programs

#### Video Demo: https://www.youtube.com/watch?v=ssJxss6B3cs

#### Description:

The idea behind this website was to take some of the programs that I have written in C in the past year and make

a more user friendly UI so people that are not very experienced with computers can use it, since programs written

in C generaly require a terminal window or a command prompt to be executed, and that does not look very good nor is it

very user friendly.



For this reason, since all programs were written in C, the inputs given by the user in the website get written to or appended

to a text file throught python that then gets read by the C program, which in turn will also write the solution to the same or another text file

that will ultimately get read and processed with python once again.



Another thing I made is a blueprints folder to keep my programs organized and looking nice, so the pages have different css files.

However, that created a problem when executing the C programs and reading from the files, since everything that is being executed

by flask with python assumes it comes from the main app.py folder even though the program currently being run is in another folder.

Once solution for that was to change the directory evey time we need to acess a text file and run one of the C programs.



Additionaly, the program does not use any JavaScript, although I think that for the best implementaiton of my ideas, using JS 

would be the best approach, but since it proved to be a very difficult language to learn and use, I decided to leave it for now.

In the future when I get time to learn more of it I will implement it on this project. For this reason, many of

the implementations seen on this website offer a lot of room for improvement.



Finally, all programs have checks that prevents users giving inputs not accepted by the programs, like characters, negative numbers

or anything that is not allowed. Error messages will appear and prompt the users to comply when that happens.



The first program that I have written is based on the Collatz conjecture, it was very straight forward, but since it was the first

program I implemented, it was not so easy. I guess the most difficult part here was making the check-box to show the details

of the steps for the given number.



The second program was the crossword program, this program proved to be much more difficult to implement. One big issue was how to

display the board layout so the user can submit the layout to the server. At first I planned on diplaying a table where all boxes 

are white and as the user clicks on one of them they turn black, however that would require JS and other implementations that I

just wasn't comfortable and didn't know how to use properly. The final implementation with dropdown boxes was fine enough for me.



Another challenge for the crossword was to print the final board. My idea was to get each character in a different cell of a HTML table, however, although I was sucessful in that, jinja does not accept declarations of variables, so I simply could not iterate through a 2D board with two for loops like we normally do, and that's because the only variables accepted for iterations in jinja are the one that are part of the for loop, so sending an external variable to jinja would not work. The solution for that was to created a dictionary, where we can "create" our own indexes. So in this manner, I created a dictionary with indexes 00, 01, 02, 10, 11, 12... that gets passed to jinja and from there I could concatenate the "i" and "j" for the that represent the rows and columns in the for loops to acess the values from the dictionary.



The final program was Numlee, which is a variation of the game Wordle, where a number from 1 to 99999 is generated and the user has to guess the number whithin 5 tries. The program gives feedback to the user so the answer can be improved on each try. The biggest challenge of this program was the implemenation of the feedback display after each try of the user. I wanted each try to be in a different box, as well as have certain words a different color for correct and incorrect feedback. To get around this problem, I heavily relied upon on the replace feature of jinja, which read key characters from the text file to add lines breaks, create divs and change the color of certain words. It certainly doesn't look pretty on the text file, but it works well on the website.

