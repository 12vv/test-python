import re
import json
from datasets import load_dataset

dataset = load_dataset('AdaptLLM/finance-tasks', 'Headline')
# print(f"dataset: {dataset.column_names}")
test = dataset['test']


newArr = []
index = 0
for row in test:
  headlines = row['input'].split('\n\n')
  for item in headlines:
    # remove escape marks
    item = item.replace('\\', '')
    # match double quotes
    headline = re.findall(r"(?<=\").*?(?=\")", item)
    question = re.findall(r"Does(.+?)\?", item)

    if len(headline) == 0 :
      headline = item.split('\n')
      # match: no double quotes, but start with "Answer a question about this headline:" 
      if(len(headline) != 0) and headline[0].startswith("Answer"):
        headline = headline[1:]

    answer = item.split(' ')[-1]
    newArr.append({'id': index, 'Headline': headline[0] if len(headline) > 0 else '' , 'Question': "Does" + question[0] if len(question) > 0 else '', 'Answer': "" if answer.endswith("?") else answer})
    index += 1

with open("./output.json","w") as f:      
    json.dump(newArr, f, indent=4)