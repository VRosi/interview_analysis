

def transcriptParser(path, Q, question):
    return 1
    # import pandas as pd
    # df = pd.read_csv(path,
    #                  error_bad_lines=False,
    #                  encoding='utf8',
    #                  delimiter=':',
    #                  engine='python',
    #                  skip_blank_lines=True)
    # # Dictionnarization
    # Transcript = df.to_dict()
    # # Separation of number and answers into 2 dictionaries
    # Speak = Transcript['QR']
    # print(Speak)
    # Text = Transcript['T']
    # # Prep of dictionary result that get all answers for the 6 questions.
    # k = 0
    # strTemp = ""
    # result = {}
    # for index, i in enumerate(Speak.items()):
    #     if i[1] == 'R' or i[1] in Q:
    #         if Text[index] is not None:
    #             strTemp += Text[index]
    #         else:
    #             if k > 0:
    #                 strTemp = strTemp.replace('\xa0', '')
    #                 strTemp = strTemp.replace('\\', '')
    #                 result[k] = strTemp
    #                 strTemp = ""
    #             k += 1
    #
    # strTemp = strTemp.replace('\xa0', '')
    # strTemp = strTemp.replace('\\', '')
    # result[k] = strTemp
    # loc = Q.index(question)
    # print("loc=", loc)
    # return 1
