"""
JARVIS Entertainment — jokes, quotes, fun facts, trivia
"""
import random


JOKES = [
    ("Why don't scientists trust atoms?", "Because they make up everything."),
    ("What do you call a bear with no teeth?", "A gummy bear."),
    ("Why did the scarecrow win an award?", "He was outstanding in his field."),
    ("What do you call fake spaghetti?", "An impasta."),
    ("Why can't a bicycle stand on its own?", "It's two-tired."),
    ("What do you call cheese that isn't yours?", "Nacho cheese."),
    ("Why did the math book look so sad?", "Because it had too many problems."),
    ("What do you call a fish without eyes?", "A fsh."),
    ("Why did the programmer quit his job?", "Because he didn't get arrays."),
    ("How does a computer get drunk?", "It takes screenshots."),
    ("Why do Java developers wear glasses?", "Because they don't C#."),
    ("What is a computer's favorite snack?", "Microchips."),
    ("Why was the JavaScript developer sad?", "Because he didn't know how to 'null' his feelings."),
    ("What do you call a sleeping dinosaur?", "A dino-snore."),
    ("Why don't programmers like nature?", "It has too many bugs."),
]

QUOTES = [
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Innovation distinguishes between a leader and a follower.", "Steve Jobs"),
    ("The best way to predict the future is to invent it.", "Alan Kay"),
    ("Any sufficiently advanced technology is indistinguishable from magic.", "Arthur C. Clarke"),
    ("The question of whether a computer can think is no more interesting than whether a submarine can swim.", "Edsger Dijkstra"),
    ("Programs must be written for people to read, and only incidentally for machines to execute.", "Harold Abelson"),
    ("First, solve the problem. Then, write the code.", "John Johnson"),
    ("The most disastrous thing that you can ever learn is your first programming language.", "Alan Kay"),
    ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    ("Experience is the name everyone gives to their mistakes.", "Oscar Wilde"),
    ("The journey of a thousand miles begins with one step.", "Lao Tzu"),
    ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
    ("It does not matter how slowly you go as long as you do not stop.", "Confucius"),
    ("Imagination is more important than knowledge.", "Albert Einstein"),
    ("The only limit to our realization of tomorrow is our doubts of today.", "Franklin D. Roosevelt"),
]

FUN_FACTS = [
    "A group of flamingos is called a 'flamboyance.' Quite fitting for those birds, sir.",
    "Honey never spoils. Archaeologists have found 3000-year-old honey in Egyptian tombs that was still perfectly edible.",
    "The shortest war in history was between Britain and Zanzibar in 1896 — it lasted only 38 to 45 minutes.",
    "Cleopatra lived closer in time to the Moon landing than to the construction of the Great Pyramid.",
    "The Oxford University is older than the Aztec Empire. It was founded around 1096 CE.",
    "There are more stars in the observable universe than grains of sand on all of Earth's beaches combined.",
    "A day on Venus is longer than a year on Venus. It rotates so slowly that it takes longer to spin once than to orbit the Sun.",
    "Octopuses have three hearts, blue blood, and can change color despite being colorblind.",
    "The Eiffel Tower grows about 6 inches taller during summer due to thermal expansion of the iron.",
    "A bolt of lightning contains enough energy to toast 100,000 slices of bread.",
    "The human brain generates about 20 watts of electricity — enough to power a dim light bulb.",
    "Sharks are older than trees. They've been around for at least 450 million years.",
    "It would take about 1.2 million mosquitoes biting simultaneously to drain all the blood from the average human body.",
    "The first computer bug was an actual bug — a moth found in a relay of the Harvard Mark II computer in 1947.",
    "Wi-Fi doesn't stand for 'Wireless Fidelity' — it's actually a made-up phrase coined by a marketing firm.",
]

TRIVIA = [
    {"q": "What does 'HTTP' stand for?", "a": "HyperText Transfer Protocol"},
    {"q": "Which programming language was created by Guido van Rossum?", "a": "Python"},
    {"q": "What year was the first iPhone released?", "a": "2007"},
    {"q": "Who is known as the 'father of computing'?", "a": "Charles Babbage"},
    {"q": "What does 'AI' stand for?", "a": "Artificial Intelligence"},
    {"q": "Which company developed the Python programming language?", "a": "Python was created by Guido van Rossum — not a company, but a single individual"},
    {"q": "What is the capital of France?", "a": "Paris"},
    {"q": "How many bits are in a byte?", "a": "8 bits"},
    {"q": "What does 'RAM' stand for?", "a": "Random Access Memory"},
    {"q": "Which planet is known as the Red Planet?", "a": "Mars"},
    {"q": "What does 'SQL' stand for?", "a": "Structured Query Language"},
    {"q": "Who wrote the theory of relativity?", "a": "Albert Einstein"},
    {"q": "What does 'CPU' stand for?", "a": "Central Processing Unit"},
    {"q": "Which language is primarily used for Android development?", "a": "Java and Kotlin"},
    {"q": "What is the binary representation of the decimal number 10?", "a": "1010"},
]


class Entertainment:
    def __init__(self):
        self._trivia_index = 0
        self._fact_index = 0

    def get_joke(self) -> str:
        setup, punchline = random.choice(JOKES)
        return f"Here's one, sir:\n{setup}\n...{punchline} 😄"

    def get_quote(self) -> str:
        quote, author = random.choice(QUOTES)
        return f'"{quote}"\n\n— {author}'

    def get_quote_short(self) -> str:
        quote, author = random.choice(QUOTES)
        return f'"{quote}" — {author}'

    def get_fun_fact(self) -> str:
        fact = random.choice(FUN_FACTS)
        return f"Interesting fact, sir:\n{fact}"

    def get_trivia(self) -> str:
        item = random.choice(TRIVIA)
        return f"Trivia question:\n{item['q']}\n\n💡 Answer: {item['a']}"

    def get_motivational(self) -> str:
        quotes = [q for q, _ in QUOTES]
        return f"Here's some motivation, sir:\n{random.choice(quotes)}"


entertainment = Entertainment()
