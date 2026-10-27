# NIGHT SHIFT - a cybersecurity choose-your-own-adventure
# --------------------------------------------------------------------------------------------------------

import time # --> to use time.sleep() --> typing effect

typing_speed = 0  # global variable --> instant typing

# dictionary inside a dictionary  as if its a company's computer
SERVERS = { #we're using capitals for the variable name indicating it is fixed data
    "file-server": {"finance": {"payroll.xlsx": "file"},
                    "it": {"admin_passwords.xlsx": "file"},
                    "startup": {"update_helper.exe": "file"}},
    "truck-app": {"routes": {"sydney.csv": "file"},
                  "startup": {"update_helper.exe": "file"}},
    "database": {"temp": {"customers.zip": "file"}},
    "website": {"pages": {"home.html": "file"}},
    "login-server": {"logs": {"logins.txt": "file"}},
}

HACKED_SERVERS = ["database", "file-server", "truck-app"] # a list of hacked servers 

HOW_THE_HACK_WORKED = [ # a list of text lines at the end
    "Mon 4:42pm  Jess gets a fake 'payroll' email. The link opens a fake login page, and she types in",
    "            her real password. The hackers now have it. (This is called phishing.)",
    "Tue 1:31am  The hackers log in as Jess. The company makes you approve new logins on your phone,",
    "            so they keep trying until her phone gets 14 pop-ups. Half asleep, she taps Approve.",
    "            (This is called MFA fatigue.)",
    "Tue 1:46am  Now inside as Jess, they connect through the company VPN, the secure 'work from home'",
    "            connection, so it looks like a normal employee working late.",
    "Tue 1:58am  They look around the shared folders. The IT folder wasn't locked, so they open",
    "            admin_passwords.xlsx and get the password for the all-powerful backup account.",
    "Tue 2:05am  Using the backup account, they copy every customer's details into customers.zip.",
    "Tue 2:11am  They delete the file server's backups, so the company can't easily recover.",
    "Tue 2:30am  They upload customers.zip to their own server. The data is now stolen.",
    "Tue 2:40am  They hide ransomware (update_helper.exe) set to start at 3:30am, to lock the files",
    "            and demand money. Stealing data AND locking files is called double extortion.",
] 

# list of tuples
GRADES = [
    (100, "S+", "LEGEND. They're naming the server room after you.",
     "I... I think I'm going to cry. Take tomorrow off. Actually, take my job."),
    (90, "S", "Incident Commander material",
     "Three weeks in and you handled that better than I would have. Don't tell anyone I said that."),
    (80, "A", "Calm under pressure",
     "Solid work. A couple of wobbles, but the company's still standing. Coffee's on me."),
    (70, "B", "Survived the night (barely)",
     "We made it. Mostly. Let's never speak of the bits we didn't make."),
    (60, "C", "Needs more coffee",
     "I've ordered you a bigger coffee machine. And a training course. Maybe two."),
    (45, "D", "Ringo is 'not angry, just disappointed'",
     "I'm not angry. I'm just... going to sit here quietly for a minute."),
    (30, "E", "HR would like 'a quick chat' at 9am",
     "I've put a meeting in your calendar. It's with HR. Bring a pen. And maybe a tissue."),
    (0, "F", "YOU'RE FIRED. Security walks you out holding a cardboard box.",
     "I said nothing EVER happens on Tuesdays. You made something happen. Please return your badge."),
]


class InvalidChoice(Exception): #in case player types something that isnt in the options
    """Our own error type, raised when the player types an answer that isn't an option."""
    pass # nothing to add

# --------------------------------------------------------------------------------------------------------

def say(text=""): #creates function say()
    """Print each text, type letter by letter if slow typing is on, otherwise instant."""
    for letter in text: # for loop goes thru text 1 character at a time
        print(letter, end="", flush=True)
        time.sleep(typing_speed)
    print()


def search(folder, word, path=""): #recursion 
    """Look through folders inside folders for names containing word."""
    found = [] # empty list to collect matches
    for name in folder: #loops thru the folder
        full_path = path + "/" + name
        if word in name.lower():
            found.append(full_path)
        if type(folder[name]) == dict: #check if its another folder
            found += search(folder[name], word, full_path)
    return found


def get_choice(answer, options):
    """Cleans up the player's answer and raises InvalidChoice if it isn't one of the options."""
    answer = answer.strip().lower() #removes spaces if user enter space 
    if answer not in options:
        raise InvalidChoice # our custom exception.. pass
    return answer


def get_grade(score):
    """finding your grade through looping the GRADES list from top to bottom"""
    for minimum, letter, title, comment in GRADES:
        if score >= minimum:
            return letter, title, comment

# --------------------------------------------------------------------------------------------------------

class Game: # one play through of the game
    """One play-through of the game. Remembers the points, tips and choices for this game."""
    def __init__(self, name): # setting up a new game
        """Sets up a new game: player name, 0 points, empty lists, and the flags set to False."""
        self.name = name # player's name
        self.points = 0 # points earned from correct choices
        self.max_points = 0 # possible points
        self.tips = []           # (good?, tip) shown at the end
        self.aftermath = []      # what went wrong because of ur mistakes
        self.virus_removed = False # whether found the ransomware
        self.cover_up = False #whether agree to hide the hack

    def ask(self, question, options):
        """Ask a question with a/b/c options and return the letter picked."""
        say("\n" + question)
        for letter in options: 
            say(f"  {letter}) {options[letter]}")
        while True:
            try:
                return get_choice(input("> "), options)
            except InvalidChoice:
                say("Please type " + ", ".join(options) + ".")

    def good(self, tip):
        """A right answer: adds 10 points, saves a good tip, and prints [ OK ]."""
        self.points += 10
        self.max_points += 10
        self.tips.append((True, tip))
        say("  [ OK ] Good call.")

    def bad(self, what_happens, tip, later):
        """A wrong answer: no points, prints the ALERT, and saves a tip and an aftermath line for the end."""
        self.max_points += 10
        self.tips.append((False, tip))
        self.aftermath.append(later) # what happened next
        say("\n  [!!!] ALERT: WRONG MOVE [!!!]")
        say("  " + what_happens)

    def talk(self, person, words):
        """Shortcut to print a character's line as 'Name: words'."""
        say(f"{person}: {words}")

    # ----------------------------------------------- the story -----------------------------------------------

    def play(self):
        """plays the intro, calls each scene in order, then the ending."""
        say("\n=== NIGHT SHIFT ===\n")
        say("Meridian Freight is a logistics company. Its trucks and warehouses move parcels across")
        say("Australia and three other countries, and it stores the details of 412,000 customers.")
        say(f"\nYou are {self.name}, a junior cybersecurity analyst. You started three weeks ago, and")
        say("tonight is your first night shift ALONE. Your job: watch the security alerts while")
        say("everyone else sleeps.")
        say("\nYour boss Ringo, the senior analyst, went home at 10pm. His last words:")
        say("'Call me if anything big happens. But relax, nothing ever happens on Tuesdays.'")
        say("\nIt's 2:13am. You're halfway through a cold coffee, hoping for a quiet night...")
        say("Then your screen lights up. Five alerts at once.\n")
        self.alerts()
        self.jess()
        self.call_boss()
        self.stop_upload()
        self.lock_account()
        self.evidence()
        self.contain()
        self.find_virus()
        self.phone_call()
        self.passwords()
        self.ransomware()
        self.backups()
        self.tell_customers()
        self.lessons()
        self.ending()

    def alerts(self):
        """Scene 1: shows 5 alerts and the player types which ones are the real hack (2 and 5)."""
        say("ALERTS")
        say("  1. Someone tried to hack the customer website 37 times. The firewall blocked them all.")
        say("  2. Jess from Finance logged in from overseas, but she's asleep in Sydney.")
        say("  3. The CEO logged in from Singapore. (HR says she's at a meeting there this week.)")
        say("  4. Mark's laptop downloaded a huge 4 GB file. (IT scheduled the monthly Windows update tonight.)")
        say("  5. The backup account just copied every customer's details (412,000 people).")
        answer = input("\nWhich alerts are the real hack? Type the numbers (e.g. 1 3): ")
        if "2" in answer and "5" in answer and "1" not in answer and "3" not in answer and "4" not in answer:
            self.good("You ignored the false alarms and found the real problem.")
        else:
            self.bad("Alert 1 was already blocked, 3 is the CEO on a work trip, and 4 is just the "
                     "Windows update. The real hack is 2 and 5.", # what happens
                     "Not every alert is a hack. Check the facts before you act.", # tip
                     "You spent 20 minutes chasing false alarms while the real hackers kept going.") # what happended next

    def jess(self):
        """Scene 2: shows the fake email and pop-up spam, and asks what happened (answer c)."""
        say("\nYou check the logs. Yesterday Jess got an email from 'payroll@meridian-freight-hr.example'")
        say("saying 'URGENT: verify your account'. She clicked it. Then at 1am her phone got 14")
        say("'approve this login?' pop-ups. At 1:44am she tapped Approve.")
        choice = self.ask("What do you think happened?", {
            "a": "Jess is secretly a hacker",
            "b": "It's just a computer glitch",
            "c": "Jess was tricked by a fake email, then spammed with pop-ups until she tapped yes"})
        if choice == "c":
            self.good("You saw the hackers tricked a person instead of breaking a computer.")
        else:
            self.bad("That email wasn't from the real company website. It was a fake to steal her password.",
                     "Fake emails (phishing) are the most common way hackers get in.",
                     "Nobody warned staff about the fake email, so two more people clicked it the next day.")

    def call_boss(self):
        """Scene 3: asks whether to wake up Ringo (answer a)."""
        choice = self.ask("Hackers are copying customer data. What now?", {
            "a": "Call Ringo and wake him up",
            "b": "Handle it yourself, you don't want to bother him",
            "c": "Wait until morning"})
        if choice == "a":
            self.talk("Ringo", "Mmm... hello? Okay, I'm up. Keep going, I'll be on the call in a sec.")
            self.good("You called your boss. Big problems need more than one person.")
        else:
            self.bad("This is way too big to handle alone. You end up calling Ringo 20 minutes later anyway.",
                     "Always wake your boss when customer data is being stolen.",
                     "Ringo's first words at the review: 'Why did nobody call me?'")

    def stop_upload(self):
        """Scene 4: the player types the IP address to block, with 2 attempts."""
        say("\n[!!!] NEW ALERT: A huge file called customers.zip is uploading to 198.51.100.23!")
        for attempt in range(2): # two attempts
            ip = input("Type the IP address to block at the firewall: ").strip()
            if ip == "198.51.100.23":
                say("Blocked! The upload stops before most of the data gets out.")
                self.good("You blocked the upload fast and saved most of the customer data.")
                return
            say("  [!!!] Wrong address! The upload is still going... check the alert again.")
        self.bad("Too slow. Most of the customer data is gone.",
                 "Block the hacker's upload as quickly as you can.",
                 "300,000 customers' details turned up for sale online a week later.")

    def lock_account(self):
        """Scene 5: asks how to handle Jess's hacked account (answer b)."""
        choice = self.ask("The hackers are using Jess's account. What do you do?", {
            "a": "Lock her account and report her to HR",
            "b": "Lock her account, reset her password, and talk to her kindly in the morning",
            "c": "Leave it, it's not her fault"})
        if choice == "b":
            self.talk("Ringo", "Good. She was tricked at 1am. That's our system's fault, not hers.")
            self.good("You locked the hacked account and treated Jess as a victim.")
        elif choice == "a":
            self.bad("Ringo: 'Bit harsh. She got tricked while half asleep.'",
                     "Blaming the person who got tricked doesn't stop it happening again.",
                     "Jess quit. Now nobody in Finance will admit it when they click something dodgy.")
        else:
            self.bad("The hackers are still logged in as Jess...",
                     "Always lock a hacked account so the hackers get kicked out.",
                     "The hackers came back the next night through Jess's account.")

    def evidence(self):
        """Scene 6: asks what to do before fixing anything (answer c: save evidence)."""
        choice = self.ask("Before you fix anything, what do you do?", {
            "a": "Restart the hacked servers to kick the hackers out",
            "b": "Nothing, just start fixing",
            "c": "Save copies of the logs and the hacked servers' memory"})
        if choice == "c":
            self.good("You saved the evidence before changing anything.")
        else:
            self.bad("All the clues about what the hackers did are wiped. Nobody can prove what was stolen.",
                     "Save evidence first, or you can't prove what happened.",
                     "With no evidence, the company had to tell ALL 412,000 customers to assume the worst.")

    def contain(self):
        """Scene 7: asks how to stop the hackers spreading. Only answer c leads to call_it_guy()."""
        choice = self.ask("How do you stop the hackers spreading to other servers?", {
            "a": "Turn off the WHOLE company network (every warehouse in 4 countries stops)",
            "b": "Watch the hackers for a while to learn more",
            "c": "Cut off just the hacked servers"})
        if choice == "a":
            self.bad("Trucks line up at every warehouse. It works, but it costs the company a fortune.",
                     "Shutting down everything is a last resort, and the boss's call to make.",
                     "Trucks sat lined up at the warehouse gates for 3 days. Two big customers left.")
            return
        if choice == "b":
            self.bad("While you watch, the hackers keep stealing data and spread to more servers.",
                     "Watching is risky when data is actively being stolen.",
                     "The hackers reached two more servers while you were 'learning more'.")
            return
        self.good("You chose to cut off only the hacked servers, so the business keeps running.")
        self.call_it_guy()

    def call_it_guy(self):
        """Scene 7b: choose who to call, then a while loop where the player types servers for Dev to cut off."""
        choice = self.ask("You don't have access to unplug servers. What do you do?", {
            "a": "Go into the server room and start pulling cables yourself",
            "b": "Call Dev, the IT guy who looks after the network",
            "c": "Email the CEO for permission"})
        if choice == "b":
            self.talk("Dev", "*yawn* Dev here. Hackers? Oh no. Okay, tell me which servers to cut off.")
            self.good("You called the right person for the job.")
        elif choice == "a":
            self.bad("You pull the wrong cable. The customer website goes down. Dev arrives anyway, furious.",
                     "Don't touch things you don't have access to. Call the person who does.",
                     "The customer website was down for 6 hours because of a cable you pulled.")
            self.talk("Dev", "Please never touch my cables again. Which servers do you ACTUALLY want cut off?")
        else:
            self.bad("The CEO is asleep in Singapore. Nobody answers. You finally call Dev an hour later.",
                     "In an emergency, call the people who can actually help.",
                     "The hackers had an extra hour because you emailed the CEO instead of calling IT.")
            self.talk("Dev", "An hour late, but I'm here. Which servers do you want cut off?")

        self.talk("Dev", "Here's every server the hacked accounts touched tonight:")
        say("  1:46am  Jess's account          -> login-server  (signed in through the VPN)")
        say("  1:58am  Jess's account          -> file-server   (opened the IT folder)")
        say("  2:05am  the backup account      -> database      (copied every customer's details)")
        say("  2:39am  the backup account      -> truck-app     (logged in... nobody knows why)")
        say("  website: only normal customer visits")
        self.talk("Dev", "Heads up: the login-server is how EVERY staff member signs in. Jess's account is")
        self.talk("Dev", "already locked, so cutting that off would just lock everyone else out.")
        say("\nServers: " + ", ".join(SERVERS))
        say("Type one server at a time. Type 'done' when you're finished.")
        cut_off = []
        while True:
            server = input("Cut off: ").strip().lower()
            if server == "done":
                break
            if server not in SERVERS:
                self.talk("Dev", "That's not one of our servers. Check the list.")
            elif server in cut_off:
                self.talk("Dev", "Already done that one.")
            else:
                cut_off.append(server)
                self.talk("Dev", f"Okay, {server} is off the network.")

        missed = [s for s in HACKED_SERVERS if s not in cut_off] #make a list of every server s in HACKED_SERVERS that is not in cut_of
        extra = [s for s in cut_off if s not in HACKED_SERVERS] # cut off by mistake
        if not missed and not extra:
            self.good("You cut off exactly the three hacked servers.")
        elif missed:
            self.bad(f"You missed {', '.join(missed)}. The hackers are still on it!",
                     "Cut off every server the hackers touched.",
                     f"The hackers kept using {', '.join(missed)} for another two days.")
        else:
            self.bad(f"{', '.join(extra)} wasn't hacked, but now it's offline for nothing.",
                     "Only cut off servers that were actually hacked.",
                     f"Customers couldn't use the {', '.join(extra)} all morning for no reason.")

    def find_virus(self):
        """Scene 8: the player types search words (3 attempts) to find the hidden ransomware using search()."""
        say("\nRingo: 'Hackers often hide a program that runs when a server starts up.")
        say("        Search the servers and see if they left anything behind.'")
        for attempt in range(3): # 3 attempts
            word = input("Type a word to search every server for: ").strip().lower()
            if len(word) < 3:
                say("  Search words need at least 3 letters.")
                continue
            results = []
            for server in SERVERS:
                for path in search(SERVERS[server], word):
                    results.append(server + path)
                    say("  found: " + server + path)
            suspicious = False
            for r in results:
                if "startup" in r or "update_helper" in r or ".exe" in r:
                    suspicious = True
            if suspicious:
                say("There's a program called update_helper.exe set to run on startup. That isn't ours!")
                say("You delete it from every server.")
                self.virus_removed = True
                self.good("You found and removed the hidden ransomware.")
                return
            if not results:
                say("  nothing found.")
            say("Hint: try searching for 'startup'.")
        self.bad("You didn't find anything... but something is still hiding on the servers.",
                 "Search for anything hackers might have left behind.",
                 "The ransomware you missed locked up the file server and truck app at 3:30am.")

    def phone_call(self):
        """Scene 9: Marcus asks you to hide the hack (answer a: refuse). Agreeing sets cover_up to True."""
        self.talk("Ringo", "This is big. Company rules say the bosses have to be told about any serious hack,")
        self.talk("Ringo", "so I'm ringing the executives now. Expect some calls.")
        say("\nTen minutes later your phone rings. It's Marcus, the CFO. Ringo just woke him up.")
        self.talk("Marcus", "We announce our profits on Thursday. Don't write down that we got hacked.")
        self.talk("Marcus", "Fix it quietly and we'll decide later if anyone needs to know.")
        choice = self.ask("What do you say?", {
            "a": "Sorry, I can't hide this. I'm writing it down and telling Ringo and Legal",
            "b": "Okay, I'll keep it quiet",
            "c": "I'll think about it"})
        if choice == "a":
            self.talk("Marcus", "...Fine. Keep me updated.")
            self.good("You stayed honest even when a senior boss asked you to hide it.")
        elif choice == "b":
            self.cover_up = True
            self.bad("Marcus: 'Good. You'll go far here.' ...Will you, though?",
                     "Never hide a hack. Write down the request and tell someone.",
                     "Three months later the cover-up leaked to the news. Your name was in the emails.")
        else:
            self.bad("He hangs up. Nobody else knows he asked you to hide it.",
                     "If someone asks you to hide a hack, write it down and tell someone.",
                     "When the truth came out, people asked why you never mentioned Marcus's call.")

    def passwords(self):
        """Scene 10: explains the password spreadsheet and asks how to fix it (answer c)."""
        say("\nYou look at how the hackers got from Jess's account to the database.")
        say("The 'it' folder on the file server was meant to be for IT staff only, but someone set it")
        say("so EVERYONE in the company could open it. Logged in as Jess, the hackers opened")
        say("'admin_passwords.xlsx'. Inside was the password for the backup account, a super-powerful")
        say("account that can get into every server. That's how they reached the customer database.")
        choice = self.ask("How do you fix the password problem?", {
            "a": "Change only Jess's password",
            "b": "Rename the file to something less obvious",
            "c": "Change all the passwords, put them in a password manager, and lock the IT folder to IT staff only"})
        if choice == "c":
            self.good("You changed every stolen password and got rid of the password spreadsheet.")
        else:
            self.bad("The hackers still know every other password in that spreadsheet.",
                     "Passwords should never be kept in a spreadsheet.",
                     "The hackers logged back in a week later with a password from that spreadsheet.")

    def ransomware(self):
        """Scene 11: if the virus wasn't found, it goes off and the player decides about the ransom (answer c)."""
        if self.virus_removed:
            say("\n3:30am comes and goes. Nothing happens. The ransomware you deleted would have gone off now!")
            return
        say("\n[!!!] 3:30am: the screens on the file server and truck app go black.")
        say("  'YOUR FILES ARE LOCKED. PAY 50 BITCOIN IN 48 HOURS OR WE POST YOUR CUSTOMERS' DATA.'")
        choice = self.ask("What do you do?", {
            "a": "Pay it with the company card to make it stop",
            "b": "Ignore it",
            "c": "Don't pay. Pass it to the bosses, Legal and the police"})
        if choice == "c":
            self.good("You didn't pay the hackers yourself and passed it to the people in charge.")
        else:
            self.bad("Paying isn't your decision, and hackers often don't unlock anything anyway.",
                     "Ransom demands go straight to the bosses and the police.",
                     "The company card got declined at 50 Bitcoin. The hackers posted the data anyway.")

    def backups(self):
        """Scene 12: asks whether to trust the green backup screen or check first (answer b)."""
        say("\nTime to turn everything back on. The backup screen shows all green ticks.")
        choice = self.ask("What do you do?", {
            "a": "Restore everything straight away, it's all green",
            "b": "Check the backups actually exist first"})
        if choice == "b":
            say("Good thing you checked! The hackers deleted the file server's backups.")
            say("The green screen only showed the backups RAN, not that they still EXIST. You use an older copy.")
            self.good("You checked the backups yourself instead of trusting the screen.")
        else:
            self.bad("The file server restore fails. The hackers had deleted its backups!",
                     "A green tick isn't proof. Always check backups really exist.",
                     "Finance lost a whole week of invoices because the backups were gone.")

    def tell_customers(self):
        """Scene 13: asks whether to tell customers their data was stolen (answer b)."""
        self.talk("Legal", "Some customer names, addresses and licence numbers were stolen.")
        choice = self.ask("Do we tell the customers?", {
            "a": "Wait until after Thursday's profit announcement",
            "b": "Yes, tell them now, honestly and in simple words",
            "c": "Say nothing was stolen"})
        if choice == "b":
            self.talk("Legal", "Agreed. The law says we have to tell them and the privacy regulator.")
            self.good("You told customers quickly so they can protect themselves.")
        else:
            self.bad("Legal: 'We can't do that. By law, people must be told when their data is stolen.'",
                     "When customer data is stolen, the law says you must tell them.",
                     "The privacy regulator fined the company for telling customers too late.")

    def lessons(self):
        """Scene 14: asks for the most important fix for next time (answer a)."""
        say("\nThe next morning, everyone meets to stop this happening again.")
        choice = self.ask("What's the most important fix?", {
            "a": "Better login pop-ups (type a number, not just tap yes) and fake-email training for staff",
            "b": "Fire Jess",
            "c": "Buy new computers"})
        if choice == "a":
            self.good("You fixed the real cause instead of blaming someone.")
        else:
            self.bad("That doesn't stop the next fake email or pop-up spam from working.",
                     "Fix the system that let the hackers in, not the person who got tricked.",
                     "Six months later, the exact same trick worked on someone else.")

    # ---------------------------------------------- the end -----------------------------------------------

    def ending(self):
        """Works out the score and grade, then prints the results, the hack timeline, the aftermath and the tips."""
        score = self.points * 100 // self.max_points # whole number division
        letter, title, comment = get_grade(score)
        if self.cover_up:
            story = "THE COVER-UP: the hack leaked, and your name was on it."
        elif score == 100:
            story = "PERFECT NIGHT: Ringo says 'not bad for your first solo shift!'"
        elif score >= 70:
            story = "GOOD WORK: a few bumps, but you saved the night."
        elif score >= 40:
            story = "ROUGH NIGHT: the company survived, just."
        else:
            story = "DISASTER: the hackers got almost everything."

        say("\n" + "=" * 100)
        say(story)
        say(f"SCORE: {score}/100")
        say(f"GRADE {letter}: {title}")
        say(f"\nRingo: \"{comment}\"")
        say("=" * 100)

        say("\nHOW THE HACK ACTUALLY WORKED")
        for line in HOW_THE_HACK_WORKED:
            say("  " + line)

        if self.aftermath:
            say("\nWHAT HAPPENED NEXT...")
            for event in self.aftermath:
                say("  * " + event)

        say("\nWhat you did well:")
        for good, tip in self.tips:
            if good:
                say("  + " + tip)
        say("What to do better:")
        for good, tip in self.tips:
            if not good:
                say("  - " + tip)
        self.save_report(story, score, letter, title, comment)
        self.show_high_scores(score, letter)

    def save_report(self, story, score, letter, title, comment):
        """Writes the player's results to report_<name>.txt (file output)."""
        filename = f"report_{self.name}.txt"
        with open(filename, "w") as file:
            file.write(f"HACK REPORT by {self.name}\n")
            file.write(f"{story}\nScore: {score}/100   Grade {letter}: {title}\n")
            file.write(f"Ringo says: \"{comment}\"\n\n")
            for good, tip in self.tips:
                if good:
                    file.write("GOOD: " + tip + "\n")
                else:
                    file.write("IMPROVE: " + tip + "\n")
            file.write("\nHOW THE HACK WORKED\n")
            for line in HOW_THE_HACK_WORKED:
                file.write("  " + line + "\n")
            if self.aftermath:
                file.write("\nWHAT HAPPENED NEXT\n")
                for event in self.aftermath:
                    file.write("  * " + event + "\n")
        say(f"\nReport saved to {filename}")

    def show_high_scores(self, score, letter):
        """Adds this score to scores.txt, reads every score back, and prints the top 5 (file input and output)."""
        with open("scores.txt", "a") as file:
            file.write(f"{self.name},{score},{letter}\n")
        scores = []
        try:
            with open("scores.txt") as file:
                for line in file:
                    try:
                        name, points, grade = line.strip().split(",")
                        scores.append((int(points), name, grade))
                    except ValueError:
                        pass  # skip broken lines
        except FileNotFoundError:
            say("No scores yet.")
        scores.sort(reverse=True)
        say("\nHIGH SCORES")
        for points, name, grade in scores[:5]:
            say(f"  {points:>3}  {grade:<2}  {name}")


if __name__ == "__main__": # starting code
    name = input("What's your name? ").strip() or "analyst"
    if input("Slow typing effect, like a movie? (y/n) ").strip().lower().startswith("y"):
        typing_speed = 0.02
    while True:
        Game(name).play()
        if not input("\nPlay again? (y/n) ").strip().lower().startswith("y"):
            say("Thanks for playing NIGHT SHIFT!")
            break
