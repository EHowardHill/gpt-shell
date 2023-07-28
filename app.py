import socket
import openai, os

# Put your API key here
openai.api_key = ""

def req(pre, text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": pre + text}
        ]
    )

    result = completion.choices[0].message["content"]
    return result

while True:
    text = input(os.getlogin() + "@" + socket.gethostname() + ":" + os.getcwd() + "$ ")

    category = req("Consider the following text along the lines of the following parameters: If it is a question that requires information about the user's computer, reply with the word BASH; if the question is something that requires information from the internet, reply with the word INTERNET; if you feel as if you are able to able the following questions yourself, reply with the word GPT. Here is the request to parse: ", text)

    if 'BASH' in category:

        context = ""
        content = ""
        complete = False
        while not complete:

            if context == "":
                t = req("My username is " + os.getlogin() + ", and my current working directory is " + os.getcwd() + ". If the following query requires more information about the machine in order to complete it, reply with the word 'YES', otherwise reply 'NO'. Here is the request to parse:", text)
            else:
                t = req("I ran these commands on my machine:\n\n" + context + "\n\nThe output was as follows:\n\n" + content + " . My username is " + os.getlogin() + ", and my current working directory is " + os.getcwd() + ". If the following query requires more information about the machine in order to complete it, reply with the word 'YES', otherwise reply 'NO'. Here is the request to parse:", text)

            if 'YES' in t:
                t = req("Write a response in Bash that, upon running it, will satisfy the parameters of the following text:", text)

                content = os.popen(t.replace("\n", ";")).read()
            
            else:
                if context == "":
                    t = req("Do not echo or write a welcome message. Only write a response in Bash that, upon running it, will satisfy the parameters of the following text:", text)

                else:
                    t = req("I ran these commands on my machine:\n\n" + context + "\n\nThe output was as follows:\n\n" + content + " . Do not echo or write a welcome message. Only write a response in Bash that, upon running it, will satisfy the parameters of the following text:", text)

                if "```" in t:
                    active = False
                    for tt in t.split("\n"):
                        if tt.startswith("```"):
                            if active == False:
                                active = True
                            else:
                                break
                        else:
                            if active:
                                os.system(tt)
                else:
                    for tt in t.split("\n"):
                        os.system(tt)

                complete = True

    elif 'INTERNET' in category:
        os.system("firefox 'https://www.google.com/search?q=" + text.replace(" ", "+").replace("?", "").replace("'", "") + "' &")

    elif 'GPT' in category:
        if len(category) < 5:
            response = req("", text)
        print(response)