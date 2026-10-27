# NIGHT SHIFT - COMP9001 - Final Project

*2:13 AM. You're the only one awake. The hackers aren't.*

<img width="1280" height="640" alt="image" src="https://github.com/user-attachments/assets/6c108087-3a25-44b7-bab0-26fcb57d0d24" />

NIGHT SHIFT is a choose-your-own-adventure game that runs in the terminal. You play a junior cybersecurity analyst, three weeks into the job, working your very first night shift alone at Meridian Freight, a logistics company with 412,000 customers. Your boss Ringo told you nothing ever happens on Tuesdays.

Then five alerts pop up at once.

Your job is to work out what's actually going on, stop the hackers, and make some tough calls along the way, like whether to wake your boss, what to do about the employee who got tricked, and what to say when a senior executive asks you to keep the whole thing quiet.

I made this for my COMP9001 final project. I'm also studying cybersecurity, and I wanted to make something that shows how a real attack usually happens: not someone "hacking into the mainframe" in a hoodie, but a fake email, a tired person tapping "Approve" on their phone at 1am, and a password left in a spreadsheet.

**Who it's for:** students, new staff, or anyone curious about what a security analyst actually does when things go wrong. You don't need to know anything about cybersecurity to play.

---

## How to run it

You only need Python 3. No extra libraries to install.

1. Put `night_shift.py` in a folder.
2. Open a terminal in that folder.
3. Run:

```
python3 night_shift.py
```

On Windows, you might need to type `python night_shift.py` instead.

---

## How to play

- The game asks your name, then whether you want the slow "movie" typing effect (`y` or `n`).
- Most questions are multiple choice. Just type `a`, `b` or `c` and press Enter. If you type something else, it'll ask again.
- A few parts make you type things yourself, like a real analyst would:
  - which alerts are the real attack (type the numbers, e.g. `1 3`)
  - the IP address to block at the firewall
  - which servers to cut off from the network (one at a time, then `done`)
  - a word to search the servers for anything the hackers left behind
- Good decisions get a quiet `[ OK ] Good call.` Bad ones get a big `[!!!] ALERT: WRONG MOVE [!!!]`, and they'll come back to haunt you at the end.

Some scenes only happen because of choices you made earlier, so you might not see everything on your first run. Play it a few times.

---

## The cast

| Character | Who they are |
|---|---|
| **You** | Junior cybersecurity analyst. Week 3. Very much not ready for this. |
| **Ringo** | Your boss, the senior cybersecurity analyst. Currently asleep. |
| **Jess** | Works in Finance. Clicked a link she shouldn't have. |
| **Dev** | The IT guy. Please don't touch his cables. |
| **Marcus** | The CFO. Has some "suggestions" about keeping things quiet. |

---

## Scoring

Every decision is worth 10 points. At the end you get a score out of 100, a grade, an "award", plus a comment from Ringo;)

| Score | Grade | Award |
|---|---|---|
| 100 | S+ | LEGEND. They're naming the server room after you. |
| 90+ | S | Incident Commander material |
| 80+ | A | Calm under pressure |
| 70+ | B | Survived the night (barely) |
| 60+ | C | Needs more coffee |
| 45+ | D | Ringo is "not angry, just disappointed" |
| 30+ | E | HR would like "a quick chat" at 9am |
| below 30 | F | YOU'RE FIRED. |

After your grade, the game explains step by step how the hack actually worked, shows "what happened next" because of any mistakes you made, and lists what you did well and what to do better.

---

## Files the game creates

- `report_<yourname>.txt`: a copy of your results, your feedback and the hack timeline, so you can keep it.
- `scores.txt`: the high score table. Every game gets added to it, and the top 5 show at the end.

You can delete either file whenever you want. The game will make new ones.

---

## Python concepts used

| Concept | Where it is |
|---|---|
| Classes and objects | `Game` class (one object per play-through), `InvalidChoice` exception class |
| Recursion | `search()` looks through folders inside folders to find the hidden ransomware |
| File input and output | `save_report()` writes the report; `show_high_scores()` writes and reads `scores.txt` |
| Exceptions | custom `InvalidChoice` for bad answers; `ValueError` and `FileNotFoundError` when reading scores |
| Loops | a `while` loop for telling Dev which servers to cut off, `for` loops for limited attempts, and a play-again loop |
| Containers | nested dictionaries for the servers, lists for tips and aftermath, a list of tuples for the grades |
| Functions | `say()`, `search()`, `get_choice()`, `get_grade()` and a method for each scene |

---

## The cybersecurity bits

Everything in the game is based on how real attacks tend to go:

- **Phishing:** a fake email that looks like it's from the company, used to steal a password.
- **MFA fatigue:** spamming someone's phone with login pop-ups until they tap "Approve" just to make it stop.
- **Weak permissions:** a folder that should've been IT-only was open to everyone, with passwords saved in a spreadsheet.
- **Data theft:** customer details zipped up and uploaded to the hackers' server.
- **Ransomware:** a hidden program set to lock the files at 3:30am and demand money.

The "right" answers follow normal incident response steps: figure out what's real, call for help, stop the damage, save evidence, clean up, recover carefully, be honest with the people affected, and fix the actual cause instead of blaming someone.

The company, people and IP addresses are all made up. The IPs come from ranges that are reserved for examples, so they don't belong to anyone.

---

## Spoilers

<details>
<summary>Stuck? Click for the S+ answers.</summary>

`2 5`, `c`, `a`, `198.51.100.23`, `b`, `c`, `c`, `b`, then `database`, `file-server`, `truck-app`, `done`, then search `startup`, then `a`, `c`, `b`, `b`, `a`.

</details>

