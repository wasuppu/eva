# eva

eva is the name of a programming language implemented in the course. 

I found this excellent series by Dmitry Soshnikov online, which mostly uses JavaScript implementations. For better practice, I reimplemented it in Python.

Completed the four courses in the series: Building an Interpreter from Scratch, Building a Parser from Scratch, Building a Transpiler from Scratch, and Building a Typechecker from Scratch.

In the course, the author used [syntax: parser generator](https://github.com/DmitrySoshnikov/syntax) for S-expression parsing. 
I found [this](https://gist.github.com/DmitrySoshnikov/2a434dda67019a4a7c37#file-s-expression-parser-js) code snippet in the author's gist, which appeared to work. 
Therefore, I implemented this recursive descent parser for a simplified subset of S-expressions in python and applied it to the course with some modifications.
