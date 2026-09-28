import json
from os import path
from time import sleep
from translate import Translator

class DataParser:

    def __init__(self):
        self.datas = None
        self.questions = None
        self.file_version = 1
        self.loadjson

    def loadjson(self):
        #загрузка json файла
        self.file_version = 1
        while path.exists(f"v{self.file_version}.json"):
            self.file_version += 1
        self.file_version -= 1

        with open(f"v{self.file_version}.json", "r", encoding="utf-8") as f:
            self.datas = json.load(f)
        with open("../8 class/MathQA/train.json", "r", encoding="utf=8") as f:
            self.questions = json.load(f)

    def savejson(self):
        self.file_version = 1
        while path.exists(f"v{self.file_version}.json"):
            self.file_version += 1

        with open(f"v{self.file_version}.json", "w", encoding="utf-8") as f:
            json.dump(self.datas, f, ensure_ascii=False, indent=2)

    def parser(self):
        for data, question in zip(self.datas, self.questions):
            data["grade"] = 11
            data["question"]["ru"] = question["Problem"]

            a = question["options"].replace("a ) ", "").replace("b ) ", "").replace("c ) ", "").replace("d ) ", "").replace("e ) ", "").replace("[", "").replace("]", "").replace(", ", "\n").split("\n")
            #a,b,c,d,e
            data["options"][0]["text"] = a[0]
            data["options"][1]["text"] = a[1]
            data["options"][2]["text"] = a[2]
            data["options"][3]["text"] = a[3]
            data["options"][4]["text"] = a[4]

            data["explanation"]["ru"] = question["Rationale"]

            if question["correct"] == "a":
                data["correct_letter"] = "A"
                data["correct_text"] = data["options"][0]["text"]
                data["options"][0]["is_correct"] = True
            elif question["correct"] == "b":
                data["correct_letter"] = "B"
                data["correct_text"] = data["options"][1]["text"]
                data["options"][1]["is_correct"] = True
            elif question["correct"] == "c":
                data["correct_letter"] = "C"
                data["correct_text"] = data["options"][2]["text"]
                data["options"][2]["is_correct"] = True
            elif question["correct"] == "d":
                data["correct_letter"] = "D"
                data["correct_text"] = data["options"][3]["text"]
                data["options"][3]["is_correct"] = True
            elif question["correct"] == "e":
                data["correct_letter"] = "E"
                data["correct_text"] = data["options"][4]["text"]
                data["options"][4]["is_correct"] = True
            else:
                print("???", question["correct"])

        self.savejson()

    def ru(self):
        with open("rutexts.txt", "r", encoding="utf-8") as f:
            ruquestions = [line.rstrip("\n") for line in f]
        with open("ruexplanations.txt", "r", encoding="utf-8") as f:
            ruexplanations = [line.rstrip("\n") for line in f]

        for data, que, explanation in zip(self.datas, ruquestions, ruexplanations):
            data["question"]["ru"] = que
            data["explanation"]["ru"] = explanation
        self.savejson()

    def ky(self):
        with open("kyexplanations 1.txt", "r", encoding="utf-8") as f:
            kyexplanations = [line.rstrip("\n") for line in f]

        with open("kyquestions 1.txt", "r", encoding="utf-8") as f:
            kyquestions = [line.rstrip("\n") for line in f]

        for data, exp, que in zip(self.datas, kyexplanations, kyquestions):
            data["explanation"]["ky"] = exp
            data["question"]["ky"] = que
        self.savejson()

    def rutranslate(self):
        translator = Translator(to_lang="ru", from_lang="en")
            
        i = 1
        for data in self.datas:
            if i >= 1:
                data["question"]["ru"] = translator.translate(f"{data['question']['ru']}")
                sleep(5)
                data["explanation"]["ru"] = translator.translate(f"{data['explanation']['ru']}")
        
                print(f"{data['question']['ru']}\n{data['explanation']['ru']}")
                print(i)

                with open(f"v{self.file_version + 1}.json", "w", encoding="utf-8") as f:
                    json.dump(self.datas, f, ensure_ascii=False, indent=2)
        
                sleep(5)
            i += 1

    def kytranslate(self):
        translator = Translator(to_lang="ky", from_lang="ru")
        
        i = 1
        for data in self.datas:
            if data["question"]["ky"] == "" or data["explanation"]["ky"] == "":
                data["question"]["ky"] = translator.translate(f"{data['question']['ru']}")
                sleep(10)
                data["explanation"]["ky"] = translator.translate(f"{data['explanation']['ru']}")

                print(f"{data["question"]["ky"]}\n{data["explanation"]["ky"]}")
                print(i)

                with open(f"v{self.file_version + 1}.json", "w", encoding="utf-8") as f:
                    json.dump(self.datas, f, ensure_ascii=False, indent=2)

                sleep(10)
            i += 1

    def check(self):
        i = 1
        for data in self.datas:
            print(data["question_number"])
            print(data["question"]["ru"])
            print(data["question"]["ky"])
            for k in range(5):
                print(data["options"][k]["text"])
            print(data["correct_text"])
            print(data["explanation"]["ru"])
            print(data["explanation"]["ky"], end="\n")


            i += 1

if __name__ == '__main__':
    parser = DataParser()
