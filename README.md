# Scholar Profiling

## Overview

This module is for extract resume information into different sections (personal information, educations, honors, and publications) using ChatGPT API.

## Setup

Versions: Python (3.9.13) and pip (22.0.4).

Note: If you do not have access to "gpt-4" model, use "gpt-3.5-turbo-16k" instead.

The overall breakdown of my repo's file structure.

```
yiming-yin-scholar-profiling/  
    - requirements.txt  
    - src/  
        - resume_pdfs/  
            -- 1.pdf  
            -- 2.pdf  
            -- ...  
        -- resumeScan.py  
```

* `src/resume_pdfs/`: directory that contains ~30 scholar resumes
* `src/resumeScan.py`: main functionalities that use ChatGPT API that output the given resume (pdf) into JSON format

## Functional Design (Usage)

* Takes as input a file, and outputs raw texts in the resume using PyPDF2 reader.
```python
    def extract_text_from_resume(resume_file):
        ... 
        return resume_text
```

* Takes the prompt, number of tokens as maximum limit, and model name for encoding (i.e. gpt-4), and outputs the truncated string.
```python
    def num_tokens(string: str, limit: int, encoding_name: str) -> str:
        ...
        if num_tokens > limit:
            return encoding.decode(encoding.encode(string)[:limit-32])
        else:
            return string
```

* Takes two prompts and feed them into the model one by one, and outputs the answer from ChatGPT.
```python
    def get_completion(prompt, prompt2, model="gpt-4"):
        ...
        return response.choices[0].message.content
```

## Demo video

https://drive.google.com/file/d/1tktVvUg-OCdSHw9BgtavWQsmLIFeJQzI/view?usp=sharing

## Algorithmic Design 

First, I use PyPDF2 to extract texts from the resume. Using the extracted texts, one can construct the prompt for the first pass that can extract different sections (i.e. Personal Info, Education, Publications) from the resume. In addition, the prompts are carefully modified several times to achieve the best accuracy. 

Then, a second prompt is constructed for the second pass to further divide the resume into fields like author, publication name, and year of publication. The two prompts and the output from the first pass are truncated to fit the maximum number of tokens in ChatGPT API. 

Lastly, the desired JSON format is generated. For instance, “educations” is a list of tuples: year range, major, and university name.

## Issues and Future Work

Currently the parser cannot deal with parsing a large number of papers (>20) at a time. Sometimes it will not merge different sections (when we need to merge “Conference Papers” and “Peer-reviewed Journals” with “Publications”). Another problem is when the resume is long (>15 pages), the maximum amount of tokens will be reached. The current solution is to truncate the resume when feeding the prompt into the model, but it is also possible in the future to use the model that supports larger amounts of tokens (for example, gpt-4-32k).

The next step would be to fix current issues when parsing the Publications section. One viable approach would be using a CV model to section the resume first and process each section using ChatGPT. Another method that relies on ChatGPT solely is to try to separate the Publications section. That is to say, run the publication extraction first, and then the rest.

## References 
* vedaant-jain-sectioning-info-extraction Section-Based-IE-From-Academic-Resumes: https://github.com/Forward-UIUC-2023S/vedaant-jain-sectioning-info-extraction.