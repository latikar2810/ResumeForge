QUESTION_BANK = {

    "Java": [
        "Explain OOP principles.",
        "Difference between HashMap and Hashtable?",
        "What is multithreading?"
    ],

    "Python": [
        "What are decorators?",
        "Explain list vs tuple.",
        "What is a lambda function?"
    ],

    "Flask": [
        "Explain Flask routing.",
        "What is Jinja2?",
        "How do you handle forms in Flask?"
    ],

    "SQL": [
        "Difference between DELETE, TRUNCATE and DROP?",
        "Explain SQL JOINs.",
        "What is normalization?"
    ],

    "React": [
        "What is Virtual DOM?",
        "Explain React Hooks.",
        "Difference between state and props?"
    ],

    "Git": [
        "Difference between Git and GitHub?",
        "Explain merge and rebase.",
        "What is a pull request?"
    ],

    "HTML": [
        "Difference between HTML and HTML5?",
        "What are semantic tags?"
    ],

    "CSS": [
        "Difference between Flexbox and Grid?",
        "Explain CSS specificity."
    ]
}
def generate_questions(skills):

    questions = {}

    for skill in skills:

        if skill in QUESTION_BANK:
            questions[skill] = QUESTION_BANK[skill]

    return questions