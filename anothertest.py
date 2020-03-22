import json
import random

print("This is a change.")

def players_name():
    return input("Welcome! What is your name? ")


def number_of_quesitons_to_play():
    num = -1
    while num < 0 or num > 20:
        num = int(input("How many questions would you like to play? (Must be between 1 and 20) "))
    return num


def categories_to_play():
    category = input("What categories would you like? You may choose one or all. (math, science, history) ").lower()
    while (category != "math") and (category != "science") and (category != "history") and (category != "all"):
        print("You have entered a category we don't have. Please try again.")
        category = input("What categories would you like? You may choose one or all. (math, science, histopry) ").lower()
    return category + ".json"


def clean_up_json_file():
    with open(categories_to_play()) as f:
        data = json.load(f)
    del data["response_code"]

    for i in data['results']:
        del i["category"]
        del i["type"]
        del i["difficulty"]
        i["incorrect_answers"].append(i['correct_answer'])
        i["incorrect_answers"].sort()
    return data


def ask_question_and_find_if_correct(data):
    question_and_answer_list = random.choice(data["results"])
    asked_question = question_and_answer_list["question"] + " " + str(question_and_answer_list["incorrect_answers"])
    correct_answer = question_and_answer_list["correct_answer"]
    response = input(asked_question + "    ")

    if response.lower() == "quit":
        raise NameError
    elif response.lower() == correct_answer.lower():
        data["results"].remove(question_and_answer_list)
        return [True, correct_answer]
    else:
        data["results"].remove(question_and_answer_list)
        return [False, correct_answer]


def tells_user_if_response_is_correct(data):
    correct_statements = ["You got it!", "Correct!", "That's right!"]
    incorrect_statements = ["That's not right.", "Incorrect."]
    values = list(ask_question_and_find_if_correct(data))

    if values[0] == False:
        print(random.choice(incorrect_statements), "The correct answer is:", values[1], "\n")
        return False
    else:
        print(random.choice(correct_statements) + "\n")
        return True


def want_to_stop(name, data, score, num_of_questions_left):
    with open("records.json", "r") as f:
        contents = json.load(f)
        contents[name] = [data, score, num_of_questions_left]
        print(contents)
    with open("records.json", "w") as f:
        json.dump(contents, f)


def already_have_game(name):
    with open("records.json", "r") as f:

        current_players = json.load(f)

        if name in current_players:

            continue_game = input("You already have a game on file! Would you like to continue it? ")

            if continue_game.lower() == "yes":
                print("We'll continue you game then!")

                return [True, current_players[name]]  # want to continue game

            else:  # want to erase previous game
                del current_players[name]
                with open("records.json", "w") as g:
                    json.dump(current_players, g)
                print("I'll create a new game for you then!")  # need to write updated players to json file again

                return [False]

        else:  # dont have game
            return [False]


def game_loop():
    name = players_name()

    is_game = already_have_game(name)

    if is_game[0] is True:
        number_correct = is_game[1][1]
        number_of_questions_left = is_game[1][2]
        data = is_game[1][0]

        for i in range(0, number_of_questions_left):
            if tells_user_if_response_is_correct(data) is True:
                number_correct += 1
            number_of_questions_left -= 1

    else:
        num = number_of_quesitons_to_play()
        data = clean_up_json_file()

        number_correct = 0
        number_of_questions_left = num

        for i in range(0, num):
            if tells_user_if_response_is_correct(data) is True:
                number_correct += 1
            number_of_questions_left -= 1


def main():
    try:
        game_loop()
    except NameError:
        want_to_stop(name, data, number_correct, number_of_questions_left) # todo still need to work on this
        print("Bye!")


if __name__ == "__main__":
    main()
