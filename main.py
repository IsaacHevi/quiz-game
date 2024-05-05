import tkinter as tk
import json
import random

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")

        # Load questions from JSON files
        self.questions = {}
        categories = ["science", "history", "geography"]
        difficulties = ["easy", "medium", "hard"]
        for category in categories:
            for difficulty in difficulties:
                filename = f"{category}_{difficulty}.json"
                with open(filename, "r") as file:
                    self.questions[(category, difficulty)] = json.load(file)

        # Initialize variables
        self.score = 0
        self.questions_answered = 0
        self.current_question = None
        self.selected_questions = None  # Store selected questions here

        # Configure background
        self.root.configure(bg="#fff9c4")

        # Create welcome message
        self.label_welcome = tk.Label(root, text="Welcome to the Quiz Game!", font=("Arial", 24), bg="#fff9c4", fg="#333333")
        self.label_welcome.pack()

        # Create category selection
        self.label_category = tk.Label(root, text="Choose a category:", font=("Arial", 18), bg="#fff9c4", fg="#333333")
        self.label_category.pack()
        self.category_var = tk.StringVar(root)
        self.category_var.set(categories[0])  # Default value
        self.optionmenu_category = tk.OptionMenu(root, self.category_var, *categories)
        self.optionmenu_category.config(font=("Arial", 14), bg="#ffffff", fg="#333333")
        self.optionmenu_category.pack()

        # Create difficulty selection
        self.label_difficulty = tk.Label(root, text="Choose a difficulty level:", font=("Arial", 18), bg="#fff9c4", fg="#333333")
        self.label_difficulty.pack()
        self.difficulty_var = tk.StringVar(root)
        self.difficulty_var.set(difficulties[0])  # Default value
        self.optionmenu_difficulty = tk.OptionMenu(root, self.difficulty_var, *difficulties)
        self.optionmenu_difficulty.config(font=("Arial", 14), bg="#ffffff", fg="#333333")
        self.optionmenu_difficulty.pack()

        # Create start button
        self.button_start = tk.Button(root, text="Start", command=self.start_game, font=("Arial", 16), bg="#4caf50", fg="#ffffff", padx=20, pady=10)
        self.button_start.pack()

        # Create score label
        self.label_score = tk.Label(root, text="", font=("Arial", 18), bg="#fff9c4", fg="#333333")
        self.label_score.pack()

        # Create timer label
        self.label_timer = tk.Label(root, text="Time Remaining: 60", font=("Arial", 18), bg="#fff9c4", fg="#333333")
        self.label_timer.pack()

        # Initialize timer
        self.remaining_time = 60  # 60 seconds

    def start_game(self):
        # Reset score and questions answered
        self.score = 0
        self.questions_answered = 0

        # Remove welcome message, category selection, difficulty selection, and start button
        self.label_welcome.pack_forget()
        self.label_category.pack_forget()
        self.optionmenu_category.pack_forget()
        self.label_difficulty.pack_forget()
        self.optionmenu_difficulty.pack_forget()
        self.button_start.pack_forget()

        # Display score label
        self.label_score.config(text=f"Score: {self.score} / {self.questions_answered}", bg="#fff9c4", fg="#333333")

        # Generate questions based on user selection
        category = self.category_var.get()
        difficulty = self.difficulty_var.get()
        questions = self.questions[(category, difficulty)]

        # Randomly select 10 questions
        self.selected_questions = random.sample(questions, 10)  # Store selected questions

        # Display the first question
        self.display_question(self.selected_questions[0])

        # Start timer
        self.start_timer()

    def start_timer(self):
        self.update_timer()

    def update_timer(self):
        if self.remaining_time <= 0:
            self.end_game()
        else:
            self.remaining_time -= 1
            self.label_timer.config(text=f"Time Remaining: {self.remaining_time}", bg="#fff9c4", fg="#333333")
            self.root.after(1000, self.update_timer)

    def display_question(self, question):
        self.current_question = question

        # Create question label
        self.label_question = tk.Label(self.root, text=question["question"], font=("Arial", 20), bg="#fff9c4", fg="#333333")
        self.label_question.pack()

        # Create answer buttons
        self.answer_var = tk.StringVar()
        self.buttons = []
        for i, answer in enumerate(question["incorrect_answers"] + [question["correct_answer"]]):
            button = tk.Button(self.root, text=answer, command=lambda ans=answer: self.submit_answer(ans), font=("Arial", 16), bg="#ffffff", fg="#333333", padx=20, pady=10)
            button.pack(anchor="w", padx=10, pady=5)
            self.buttons.append(button)

    def submit_answer(self, selected_answer=None):
        # Disable all buttons
        for button in self.buttons:
            button.config(state="disabled")

        # Check if an answer is selected
        if selected_answer is None:
            selected_answer = self.answer_var.get()

        # Check if the selected answer is correct
        if selected_answer == self.current_question["correct_answer"]:
            self.score += 1
            self.label_score.config(text=f"Score: {self.score} / {self.questions_answered + 1} (Correct)", bg="#fff9c4", fg="#333333")
            # Proceed to the next question
            self.next_question()
        else:
            # Highlight incorrect answer in red
            for button in self.buttons:
                if button.cget("text") == selected_answer:
                    button.config(bg="#f44336", fg="#ffffff")
                elif button.cget("text") == self.current_question["correct_answer"]:
                    button.config(bg="#4caf50", fg="#ffffff")
            self.label_score.config(text=f"Score: {self.score} / {self.questions_answered + 1} (Incorrect)", bg="#fff9c4", fg="#333333")
            # Proceed to the next question
            self.root.after(1000, self.next_question)

    def next_question(self):
        # Remove current question
        self.label_question.pack_forget()
        for button in self.buttons:
            button.pack_forget()

        # Proceed to the next question or end the game
        self.questions_answered += 1
        if self.questions_answered < 10:
            self.display_question(self.selected_questions[self.questions_answered])
        else:
            self.end_game()

    def end_game(self):
        # Display "Game Over"
        self.label_timer.pack_forget()
        self.label_score.config(text=f"Final Score: {self.score} / 10", bg="#fff9c4", fg="#333333")
        if self.score > 5:
            message = "Congratulations! You passed the quiz!"
        else:
            message = "Sorry, you failed the quiz."
        self.label_game_over = tk.Label(self.root, text=message, font=("Arial", 24), fg="#333333", bg="#fff9c4")
        self.label_game_over.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
