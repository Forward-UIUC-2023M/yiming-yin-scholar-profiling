import openai
import PyPDF2
import tiktoken
import json

openai.api_key = "#CHANGE IT TO YOUR API KEY#"

modelName = "gpt-4"

def extract_text_from_resume(resume_file):
    pdf_reader = PyPDF2.PdfReader(resume_file)

    resume_text = ""
    for page in range(len(pdf_reader.pages)):
        resume_text += pdf_reader.pages[page].extract_text()

    return resume_text

def num_tokens(string: str, limit: int, encoding_name: str) -> str:
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    print(num_tokens)

    if num_tokens > limit:
        return encoding.decode(encoding.encode(string)[:limit-32])
    else:
        return string

# def get_completion(prompt, prompt2, model="gpt-3.5-turbo-16k"):
def get_completion(prompt, prompt2, model="gpt-4"):
# def get_completion(prompt, prompt2, model="gpt-4-32k"):
    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )

    previousresponse = num_tokens(response.choices[0].message.content, 3500, modelName)

    messages.append({"role": "user", "content": prompt2})
    messages.append({"role": "assistant", "content": previousresponse})

    print("========= second prompt ===========")

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content


prompt = """
[START OF THE GUIDELINE]
According to the following resume,
1. find out the name, phone number, email, and current institution of the person. 
2. divide the following resume into different sections as Educations, Honors, and Publications only and merge anything related (e.g. merge Publications, Papers, Articles section together as Publications, merge Honors and Awards section together as Honors) while discarding the remaining uncategorised or unused section. 

For 1 and 2, you MUST use [SEP] in each section as a separation between each field in that section and MUST use [LINE] in a separate line as a divider between each section. 

Additional requirements:
1. take into account any title that involves the terms "Publications," "Papers," or "Articles" as part of the Publications section, such as such as "Peer-Reviewed Journal Articles," "Published Conference Papers," or "Five Significant Publications."
2. extract ALL the papers in the Publication section, even if one resume has ~100 papers.

An example you MUST follow is: 

Consider the input resume:
CAN BAYRAM
Department of Computer Science
Princeton University
35 Olden Street,
Princeton, NJ 08540Phone: (217)-123-1234
Email: sdflkka@google.com
Education
Ph.D. Electrical and Computer Engineering, University of Illinois, Urbana-Champaign, 2010.
M.A. South and Southeast Asian Studies, University of California, Berkeley, 2000.
M.E. Electrical Engineering, Indian Institute of Science, India, 1996.

Awards
Finalist, ICROS Best Application Paper Award
Best Manipulation Paper Award. IEEE International Conference on Robotics and Automation.
List of Teachers Ranked as Excellent by Their Students (AE483: Aerospace Decision Algorithms, Fall Semester), with outstanding ratings.

Publications
Peer-Reviewed Journal Articles
1. G.M. Henricks, M. Perry, and S. Bhat. (2021). Gender and Gendered Discourse in Two Online Science College Courses. Computer-Based Learning in Context ,Suma P. Bhat 73 (1), 1{16.
2. Z. Zeng, and S. Bhat. (2021). Idiomatic expression identication using semantic compatibility. Transactions of the Association for Computational Linguistics, 9, 1546{1562.
Published Conference Papers
1. P. Hur, H. Lee, S. Bhat, and N. Bosch. (2022). Using Machine Learning Explainability Methods to Personalize Interventions for Students. In Proceedings of the 15th International Conference on Educational Data Mining (EDM 2022). International Educational Data Mining Society.
2. W. Zhu and S. Bhat (2022). Slow Service"
3. J. Zhou, Z. Zeng, H. Gong, and S. Bhat (2022) Idiomatic Expression Paraphrasing without Strong Supervision. In Proceedings of the AAAI Conference on Artificial Intelligence , Vol. 36, No. 10, pp. 11774-11782.Suma P. Bhat 8
Peer-reviewed Papers and Other Publications
1. J. Zhou, H. Gong, and S. Bhat, PIE: Parallel Idiomatic Expression Corpus for Idiomatic Sentence Generation and Paraphrasing. In Proceedings of the 17th Workshop on Multiword Expressions (MWE 2021) , pp. 33-48.
2. N. Prabhu, M. Perry, R. F. L. Azevedo, L. Angrave, and S. Bhat (2021). Study Partners Matter: Impacts on Inclusion and Outcomes. In 2021 ASEE Virtual Annual Conference Content Access.
Conference Publications
1. A. Akhtar, B. Boyce, and T. Bretl, “The relationship between energy, phase charge, impedance, and perceived sensation in electrotactile stimulation,” in IEEE Haptics Symposium (HAPTICS), Feb. 2014.

YOU SHOULD OUTPUT:

Name:
CAN BAYRAM[LINE]

Phone:
217-123-1234[LINE]

Email:
sdflkka@google.com[LINE]

Current Institution:
Princeton University[LINE]

Educations:
Ph.D. Electrical and Computer Engineering, University of Illinois, Urbana-Champaign, 2010.[SEP]
M.A. South and Southeast Asian Studies, University of California, Berkeley, 2000.[SEP]
M.E. Electrical Engineering, Indian Institute of Science, India, 1996.[LINE]

Honors:
Finalist, ICROS Best Application Paper Award[SEP]
Best Manipulation Paper Award. IEEE International Conference on Robotics and Automation.[SEP]
List of Teachers Ranked as Excellent by Their Students (AE483: Aerospace Decision Algorithms, Fall Semester), with outstanding ratings.[LINE]

Publications:
1. G.M. Henricks, M. Perry, and S. Bhat. (2021). Gender and Gendered Discourse in Two Online Science College Courses. Computer-Based Learning in Context ,Suma P. Bhat 73 (1), 1{16.[SEP]
2. Z. Zeng, and S. Bhat. (2021). Idiomatic expression identication using semantic compatibility. Transactions of the Association for Computational Linguistics, 9, 1546{1562.[SEP]
3. P. Hur, H. Lee, S. Bhat, and N. Bosch. (2022). Using Machine Learning Explainability Methods to Personalize Interventions for Students. In Proceedings of the 15th International Conference on Educational Data Mining (EDM 2022). International Educational Data Mining Society.[SEP]
4. W. Zhu and S. Bhat (2022). Slow Service"[SEP]
5. J. Zhou, Z. Zeng, H. Gong, and S. Bhat (2022) Idiomatic Expression Paraphrasing without Strong Supervision. In Proceedings of the AAAI Conference on Artificial Intelligence , Vol. 36, No. 10, pp. 11774-11782.Suma P. Bhat 8[SEP]
6. J. Zhou, H. Gong, and S. Bhat, PIE: Parallel Idiomatic Expression Corpus for Idiomatic Sentence Generation and Paraphrasing. In Proceedings of the 17th Workshop on Multiword Expressions (MWE 2021) , pp. 33-48.[SEP]
7. N. Prabhu, M. Perry, R. F. L. Azevedo, L. Angrave, and S. Bhat (2021). Study Partners Matter: Impacts on Inclusion and Outcomes. In 2021 ASEE Virtual Annual Conference Content Access.[SEP]
8. A. Akhtar, B. Boyce, and T. Bretl, “The relationship between energy, phase charge, impedance, and perceived sensation in electrotactile stimulation,” in IEEE Haptics Symposium (HAPTICS), Feb. 2014.[LINE]

[END OF THE GUIDELINE]

Explaination:
We merge Peer-Reviewed Journal Articles, Published Conference Papers, Peer-Reviewed and Other Publications, and Conference Publications as a single section Publications. There are no honors or awards shown in the resume so the field is N/A.

Now let's begin with the following resume (You should mimic the above example but the information should be presented in the following resume):
[START OF THE RESUME YOU NEED TO PROCESS]
"""

prompt += extract_text_from_resume("./resume_pdfs/short1.pdf")

prompt = num_tokens(prompt, 6000 - 355, modelName) # truncate the prompt to appropriate tokens

prompt += "\n[END OF THE RESUME YOU NEED TO PROCESS]\n"

prompt2 = """
regarding the given information, please
1. further divide the Educations section into year range, major, and university name.
Example 1:
If the processed Educations section contains the line 
1995-1999 B.S., Engineering / B.S., Mathematics, Swarthmore College.[SEP]
This step modifies it to the following
1995-1999[SEP2]B.S., Engineering / B.S., Mathematics[SEP2]Swarthmore College.[SEP]
Example 2:
If the processed Educations section contains the line 
B.S., Engineering / B.S., Mathematics, Swarthmore College, 2019.[SEP]
This step modifies it to the following
2019[SEP2]B.S., Engineering / B.S., Mathematics[SEP2]Swarthmore College.[SEP]

2. further divide the Honors section into year and name.
Example:
If the processed Honors section contains the line 
2010, 2011 Ph.D. Excellent Research Award, KAIST[SEP]
This step modifies it to the following
2010, 2011[SEP2]Ph.D. Excellent Research Award, KAIST[SEP]

3. further divide the Publications section into authors, publication name, and year.
Example:
If the processed Publications section contains the line 
A. Akhtar, N. Aghasadeghi, L. Hargrove, and T. Bretl, “Estimation of for transhumeral prostheses,” Journal of Electromyography and Kinesiology , vol. 35, pp. 86-94, Aug. 2017.[SEP]
This step modifies it to the following
A. Akhtar, N. Aghasadeghi, L. Hargrove, and T. Bretl[SEP2]Estimation of for transhumeral prostheses[SEP2]Aug. 2017.[SEP]

4. have ALL the other fields (name, email, phone number, current institution) unchanged.
"""

"""
Comment this so no fee involved
"""
print(prompt)

response = get_completion(prompt, prompt2)
with open("resume_response4.txt", "w", encoding="utf8") as fw:
    fw.write(response)
"""
End of Comment this so no fee involved
"""

"""
    extract info from gpt response
"""
with open("resume_response4.txt", "r", encoding="utf8") as fr:
    gptResponse = fr.read()

# process each section and output according to json format
name = ""
phone = ""
email = ""
current_institution = ""
educations = []
honors = []
publications = []
gptResponse = gptResponse.replace("\n", "")
sections = gptResponse.split("[LINE]")

name = sections[0][len("Name:") :]
phone = sections[1][len("Phone:") :]
email = sections[2][len("Email:") :]
current_institution = sections[3][len("Current Institution:") :]

for section in sections:
    if section.find("Educations:") != -1:
        educations = section[len("Educations:") :].split("[SEP]")
    elif section.find("Honors:") != -1:
        honors = section[len("Honors:") :].split("[SEP]")
    elif section.find("Publications:") != -1:
        publications = section[len("Publications:") :].split("[SEP]")

print("================================")
print("Educations:\n", educations)
print("")
print("Honors:\n", honors)
print("")
print("Publications:\n", publications)
print("================================")

educations_json = []
for education in educations:
    if education == "N/A":
        continue
    year_range, major, university = education.split("[SEP2]")
    educations_json.append({"yearRange": year_range, "major": major, "university": university})

honors_json = []
for honor in honors:
    if honor == "N/A":
        continue
    year, honor_name = honor.split("[SEP2]")
    honors_json.append({"year": year, "honorName": honor_name})

publications_json = []
for publication in publications:
    if publication == "N/A":
        continue
    authors, pub_name, year = publication.split("[SEP2]")
    publications_json.append({"authors": authors, "publicationName": pub_name, "year": year})

resume_data = {
    "name": name,
    "email": email,
    "phoneNumber": phone,
    "currentInstitution": current_institution,
    "educations": educations_json,
    "honors": honors_json,
    "publications": publications_json
}

# convert Python data to JSON format
json_data = json.dumps(resume_data, indent=4)

# print the JSON data
print(json_data)

with open("resume_output", "w") as output_file:
    json.dump(json_data, output_file, indent=4)