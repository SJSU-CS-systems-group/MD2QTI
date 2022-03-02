# MD2QTI - Markdown Syntax

## Setting
'@' is used to set options. The format should be:
```
@[option]: [content]
```
Some may not require \[content\].

## Quiz and Group Setting
* Quiz title and description
```
@quiz title: Quiz 1
@quiz description: Chapter 1
```
It can be followed by an empty line or Thematic Break.

* Group
```
@group: start
@pick: 2
@points per question: 4
// questions or code fence
@group: end
```
Populate questions between start and end into one group. `pick` is to set how many questions will be pulled from the group. `points per question` won't overwrite the points in each question, but the points in each question will be ignored and `points per question` will be applied. `pick` and `points per question` are required for each group.

## Question Setting
Any text after `@question:` on the same line won't be parsed. This space can be used for some memo such as question numbers or comments. The lines between `@question` and `@answer` will be parsed as question instruction. Markdown syntax can be used here to format the text. Some question types may not require `@answer` such as text-only, file upload, and essay questions.
```
@question: -text here not parsed-
This text will be parsed.
You can use Markdown syntax to format this text.
**bold text**
*italic text*

    // This is code block
    // 4 spaces; empty lines before/after
    int main() {
        printf("hello world\n");
        return 0;
    }

Answer should come after question
@answer:
* > True
* False
```

## Answers and Correct Answer
Answers should be listed with bullet point(`*`) or plus sign(`+`). Bullet point is for single answers and plus sign is for key-value pair such as Matching and Multiple Blanks. `>` is used to indicate the correct answer. If the question has multiple answers, then put `>` for each correct answer.
```
// one answer
* wrong answer
* wrong answer
* > correct answer

// multiple answer
* wrong answer
* > correct answer
* wrong answer
* > correct answer

// matching
+ box1
    * > item1
+ box2
    * > item2
+ DISTRACTOR
    * item3
```

## Feedback
`@feedback: text` can be added into question and each answer. Some question types support feedback for the selected answers. This is an optional setting.
```
@title: Simple Question
@points: 1
@type: multiple choice
@question: #1, easy
What is 3 + 6?
@answer:
* > 9
    * @feedback: this is **correct** answer.
* 6
    * @feedback: this is *wrong* answer
@feedback: this is a `simple` question.
```
Feedback for each selected question should be in a sub-list with bullet point(`*`). Feedback text can be formatted with Markdown syntax.


## Thematic Break (Horizontal Line)
Thematic Break(Horizontal Line) is used to indicate the end of a question. It should be placed at the end of each question otherwise an error may occur.
```
// question 1
---
// question 2
---
```

## Executable Code Blocks (Code Fence)
MD2QTI can execute the code in backtick-fenced code blocks. The output(written to stdout) will be included in the quiz. It can be used to generate multiple questions or a question instruction.

    ```{.python3 .run}
    import textwrap
    for x in range(5, 10):
        print(textwrap.dedent(rf"""
            1.  What is ${x}\times 2$?
            *a) ${x*2}$
            b)  ${x*2-1}$
            """))