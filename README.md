# Minesweeper

Simple game of minesweeper where you have to avoid the bombs and reveal all hidden squares.

<img width="442" alt="Screen Shot 2022-01-04 at 1 14 05 AM" src="https://user-images.githubusercontent.com/39889137/148036766-753d5e9c-f5df-41e1-9891-71a905c4a540.png">

**How to run:**

run the main.py followed by the board size and bomb count. e.g.

```
python3 main.py 10 5
```

where the board is a 10 by 10 with 5 bombs

**Requirements:**

PyQt5

**How to win:**

You win when all the squares are revealed (turn lighter grey), except the bomb squares

You lose when you hit a bomb

You can place flags down on the squares that you suspect to be a bomb by clicking the flag button. This puts you in flag mode. Select the button agian to go back to normal mode.
