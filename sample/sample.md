@quiz title: asdf
@quiz description: asdf
---
@title: Multiple choice
@points: 4
@type: multiple choice
@question: 1
Which one is LIFO?
@ answer:
* Queue
* > Stack
* List
* Circular Queue
---
@title: Multiple answers
@points: 4
@type: multiple answers
@question: 2
Which one has O(n^2) time complexity?
@answer:
* > Insertion Sort
* > Bubble Sort
* Quick Sort
* Merge Sort
---
@title: Numerical
@points: 4
@type: numerical
@question: 3
What is the value of PI?
@answer:
> 3.141, 0.001
---
@title: Formula
@points: 4
@type: formula
@question: 4
What is 5 + [x] / [y]?
@answer:
- x, 10, 15, 3
- y, 5, 10, 3
* 5 + x / y
> 3, 5%
---
@title: Essay
@points: 4
@type: essay
@question: 5
Explain the best and worst case of Quick sort
---
@title: Fill in the blank
@points: 4
@type: blank
@question: 6
What do you call a fish without an eye?
@answer:
* > fsh
* > FSH
* > Fsh
---
@title: Multiple blanks
@points: 4
@type: multiple blanks
@question: 7
0x is a prefix for [box1] numbers
0o is a prefix for [box2] numbers
0b is a prefix for [box3] numbers
@answer:
+ box1
    * > hex
    * > Hex
    * > HEX
+ box2
    * > oct
    * > Oct
    * > OCT
+ box3
    * > bin
    * > Bin
    * > BIN
---
@group: start
@pick: 1
@points per question: 4

@title: Matching
@points: 8
@type: matching
@question: 5
Which of the following match?
@answer:
+ Sky
    * > Blue
+ Rose
    * > Red
+ Leaf
    * > Green
+ DISTRACTOR
    * Black
    * White
    * Yellow
---
@title: Multiple Dropdown
@points: 4
@type: multiple dropdown
@question: 9
City [box1], State [box2]
@answer:
+ box1
    * > San Jose
    * Texas
    * Arizona
+ box2
    * Los Angeles
    * Seattle
    * > California
---
@title: File Upload
@points: 4
@type: file
@question: 10
Implement Bubble sort and upload your .py file
---
@group: end

@title: Text Only
@points: 0
@type: text
@question: 11
This is a text box
---
@group: start
@pick: 2
@points per question: 2

```{.python3 .run}
import textwrap
for x in range(5, 10):
    print(textwrap.dedent(rf"""
        1.  What is ${x}\times 2$?
        *a) ${x*2}$
        b)  ${x*2-1}$
        """))
```
@group: end