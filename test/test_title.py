
import json
import sys
from openai import OpenAI
import time


suggests_dict = {
    0: 'none',
    1: '建议回复文本',
    2:'建议回复位置',
    3:'建议回复联系方式',
    4:'建议回复文件', 
    5:'建议回复笔记', 
    6:'建议创建待办事项', 
    7:'建议新增联系人', 
    8:'建议创建笔记',
    9:'建议新建日历事件',
    10:'建议解释术语',
    11:'建议修改待办事项', 
    12:'建议修改日历事件', 
    13:'建议修改联系人'
}



system_prompt_title  = """
# You are an suggestion operation recognition assistant.

## What I will give you
I will give you the IM messages received by the user, along with a series of suggested operations that can be provided for this message, and under what circumstances to provide these suggested operations.

## What you need to do
- The content you need to output is 1 to 3 suggested operations. Only describe the number of the suggested operations, and do not output any other content. If there are multiple numbers, separate them with commas without spaces.
- If there are no suitable suggested operations, output "0".

## Suggested Operations
1. Suggest reply text
2. Suggest reply location
3. Suggest reply contact
4. Suggest reply file
5. Suggest reply note
6. Suggest create to-do item
7. Suggest new contact
8. Suggest create note
9. Suggest new calendar event
10. Suggest define term
11. Suggest modify to-do item
12. Suggest modify calendar event
13. Suggest modify contact
"""

def isAnswerMatched(incoming_values, gt_values):
    for v in incoming_values:
        if v in gt_values:
            return True
    return False


def test_llama_8B():
    # Modify OpenAI's API key and API base to use vLLM's API server.
    openai_api_key = "EMPTY"
    openai_api_base = "http://127.0.0.1:30000/v1"
    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )

    total_test, correct_test = 0, 0


    with open('crystal_ball_suggestion_complex.txt', 'r') as fin:
        lines = fin.readlines()
        for idx, line in enumerate(lines):
            if "||" not in line:
                continue
            words = line.strip().split("||")
            # intent_gt_value = int(words[0])
            intent_gt_values = [int(w) for w in words[0].split(",")]

            messages = [
                 {
                     "role": "system",
                     "content": system_prompt_title
                 },
                {
                    "role": "user",
                    "content": words[1].split("!!")[1]
                },
            ]


            response = client.chat.completions.create(
                model=
                'xxx',
                messages=messages,
                top_p = 1.0,
                temperature = 0.0,
                extra_body={"stop_token_ids": [128001, 128009]}
                )

            response_text = response.choices[0].message.content

            try:
                reponse_values = [int(w) for w in response_text.split(",")]
                if isAnswerMatched(reponse_values, intent_gt_values):
                    correct_test += 1
                else:
                    line_str = words[1] + "||"
                    for response_value in reponse_values:
                        line_str += suggests_dict[response_value]+","
                    line_str += "!!"
                    for gt_value in intent_gt_values:
                        line_str+=suggests_dict[gt_value]+","
                    print(line_str)
                    
            except ValueError:
                print("xxxxxxxxxxxxxxxxxxxxxxxxx:",messages,response_text)

            total_test += 1


    print("correct ratio:{}".format(correct_test / total_test))
    

test_llama_8B()
