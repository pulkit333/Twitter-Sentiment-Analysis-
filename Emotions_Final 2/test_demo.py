import sentiment_modJ as s

while (True):
    sent = input("Text to Analyze (At least two coherent sentences) or 1 to exit :")
    if sent == "1":
        break
    print(s.sentiment(sent))
