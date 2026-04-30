import re

text = "Python 3.0 was released on 12-03-2008."

information = re.search(r'(\d{1,2})-(\d{2})-(\d{4})\.', text)
# print(information.group(0))

text = "Austin, 78701"
cities = re.search(r"(?P<city>[A-Za-z]+).*? (?P<zipcode>\d{5})", text)
# print(f"The city: {cities.group('city')}")
# print(f"The zipcode: {cities.group('zipcode')}")

sentence = "I wish you a happy happy birthday!"
matches = re.findall(r"(\w+)\s\1", sentence)
fixed_sentence = re.sub(r"(\w+)\s\1", r"\1", sentence)
# print(f"Fixed sentence: {fixed_sentence}")

# Find all matches of the same number
sentence = "Your new code number is 23434. Please, enter 23434 to open the door."
find_matching_number = re.findall(r"(?P<code>\d{5}).*?(?P=code)", sentence)
# print(f"Matching numbers: {find_matching_number}")

# Using named capturing groups to reference back
sentence = "This app is not working! It's repeating the last word word."
fixed_sentence = re.sub(r"(?P<word>\b\w+\b)\s(?P=word)", r"\g<word>", sentence)
# print(f"Fixed sentence: {fixed_sentence}")

contract = """
           Provider will invoice Client for Services performed within 30 days of performance. 
           Client will pay Provider as set forth in each Statement of Work within 30 days of 
           receipt and acceptance of such invoice. It is understood that payments to Provider 
           for services rendered shall be made in full as agreed, without any deductions for 
           taxes of any kind whatsoever, in conformity with Provider’s status as an independent 
           contractor. Signed on 03/25/2001.
            """
regex_dates = re.findall(r"Signed\son\s(\d{2})/(\d{2})/(\d{4})", contract)
# print(f"Dates found in contract: {regex_dates}")

# html_tags = ['<body>Welcome to our course! It would be an awesome experience</body>', '<article>To be a data scientist, you need to have knowledge in statistics and mathematics</article>', '<nav>About me Links Contact me!']
# for string in html_tags:
#     # Complete the regex and find if it matches a closed HTML tags
#     print(string)
#     match_tag = re.match(r"<([a-z]+)>.*?</\1>", string)
#
#     if match_tag:
#         # If it matches print the first group capture
#         print("Your tag {} is closed".format(match_tag.group(1)))
#     else:
#         # If it doesn't match capture only the tag
#         notmatch_tag = re.match(r"<([a-z]+)>.*?", string)
#         # Print the first group capture
#         print("Close your {} tag!".format(notmatch_tag.group(1)))

# sentiment_analysis = ['@marykatherine_q i know! I heard it this morning and wondered the same thing. Moscooooooow is so behind the times', 'Staying at a friends house...neighborrrrrrrs are so loud-having a party', 'Just woke up an already have read some e-mail']
#
# # Complete the regex to match an elongated word
# regex_elongated = r"([A-Za-z]*)([A-Za-z])\2{2,}[A-Za-z]*"
# # This works too:
# # regex_elongated = r"\w*(\w)\1\w*"
# for tweet in sentiment_analysis:
#     print(tweet)
#     # Find if there is a match in each tweet
#     match_elongated = re.search(regex_elongated, tweet)
#     #print(match_elongated)
#     #print(" ")
#
#     if match_elongated:
#         # Assign the captured group zero
#         elongated_word = match_elongated.group(0)
#
#         # Complete the format method to print the word
#         print("Elongated word found: {word}".format(word=elongated_word))
#     else:
#        print("No elongated word found")


sentiment_analysis = "You need excellent python skills to be a data scientist. Must be! Excellent python"
# Positive lookahead
# look_ahead = re.findall(r"\w+(?=\spython)", sentiment_analysis)

# Print out
# print(look_ahead)

cellphones = ['4564-646464-01', '345-5785-544245', '6476-579052-01']

# for phone in cellphones:
#     # Get all phone numbers not preceded by area code
#     print(f"Phone number: {phone}")
#     regex_lookbehind = re.findall(r"(?<!\d{3}-)\d{4}-\d{6}-\d{2}", phone)
#     print(regex_lookbehind)
#     print("")

for phone in cellphones:
    # Get all phone numbers not followed by optional extension
    number = re.findall(r"\d{3}?-\d{4}-\d{6}(?!-\d{2})", phone)
    print(number)
