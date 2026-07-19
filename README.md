Live demo : https://pythongame-6a4ecgxhgn5uaznj3yabev.streamlit.app/
 

# 🎯 Number Guessing Game — Python CLI

A simple yet fun **Number Guessing Game** built using pure Python.  
No libraries, no frameworks — just core Python logic running straight in your terminal.

---

## 🎮 How It Works

The program secretly picks a random number between **1 and 100**.  
Your job is to guess it. After every guess, you get a hint:

- 📉 **Too Low** → guess higher
- 📈 **Too High** → guess lower
- 🎉 **Correct** → you win! Your total attempts are shown.

---

## ▶️ How to Run

**1. Clone the repository**
```bash
git clone https://github.com/your-username/number-guessing-game-python.git
cd number-guessing-game-python
```

**2. Run the game**
```bash
python number_guess.py
```

> ✅ No installation needed. Just Python 3.

---

## 💻 Sample Output

enter the number: 50
too high, guess low
enter the number: 25
too low, guess high
enter the number: 37
you won man
you took 3 to win!


---

## 🧠 Concepts Used

| Concept | Usage |
|--------|-------|
| `random` module | Generate secret number |
| `while` loop | Keep game running until correct guess |
| `if / elif` | Compare guess to secret number |
| `int(input())` | Take user input from terminal |
| Counter variable | Track number of attempts |

---

## 📁 Project Structure



