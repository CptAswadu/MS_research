# openai chat complete example


import os
import openai
openai.api_key = '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'

# print openai version
# response = openai.ChatCompletion.create(model="gpt-3.5-turbo", prompt="Say this is a test", temperature=0, max_tokens=7)

# print(models = openai.Model.list())

content2 = 'Can you suggest a list of top 5 possible genes to test?'
content3 = 'Can you suggest a list of top 10 possible genes to test?'
content4 = 'Can you suggest a list of top 50 possible genes to test?'

dx_dict = {}
with open('D:/연구/testing_data/probe_info') as f:
    rows = f.readlines()
    for row in rows:
        source, sample_id, gene = row.strip().split('\t')
        dx_dict[sample_id] = gene #source + '_' +

# go over all files in a directory
source = 'ColumbiaU'
for file in os.listdir('D:/연구/testing_data/ColumbiaU')[0:1]:
    if file.startswith("ColumbiaU"):
        print(os.path.join("D:/연구/testing_data/ColumbiaU", file))

        file_path = os.path.join('D:/연구/testing_data/ColumbiaU/', file + '_chatgpt_output')

        with open(os.path.join("D:/연구/testing_data/ColumbiaU", file), 'r') as f:
            HP_IDs = f.read().splitlines()
            HP_content = ','.join(HP_IDs)
            sample_id = file
            dx_gene = dx_dict[sample_id] #source + '_' + 



        content1 = 'This is the phenotype description of the patients: ' + HP_content
        #completion = openai.ChatCompletion.create(
        #  model="gpt-4",
        #  messages=[
        #    {"role": "user", "content": content1}
        #  ]
        #)

        #print('answer 1: ')
        #print(completion.choices[0].message.content)
        #assistant_response = completion.choices[0].message.content

        completion = openai.ChatCompletion.create(
          model="gpt-4",
          messages=[
            {"role": "user", "content": content1 + content2}
          ]
        )
        print('answer 2: ')
        print(completion.choices[0].message.content)
        top5 = completion.choices[0].message.content
        dx_top5 = str(dx_gene in top5)





        completion = openai.ChatCompletion.create(
          model="gpt-4",
          messages=[
            {"role": "user", "content": content3}
          ]
        )
        print('answer 3: ')
        print(completion.choices[0].message.content)
        top10 = completion.choices[0].message.content
        dx_top10 = str(dx_gene in top10)

       
        completion = openai.ChatCompletion.create(
          model="gpt-4",
          messages=[
            {"role": "user", "content": content4}
          ]
        )
        print('answer 4: ')
        print(completion.choices[0].message.content)
        top50 = completion.choices[0].message.content
        dx_top50 = str(dx_gene in top50)

        try:
            with open(file_path, 'w') as f:
                f.write('\n'.join([top5, top10, top50]))
            with open(file_path + '.result', 'w') as f2:
                f2.write('\t'.join([source, sample_id, dx_gene, dx_top5, dx_top10, dx_top50]))
        except:
            with open(file_path, 'w', encoding = 'cp949') as f:
                f.write('\n'.join([top5, top10, top50]))
            with open(file_path + '.result', 'w', encoding = 'cp949') as f2:
                f2.write('\t'.join([source, sample_id, dx_gene, dx_top5, dx_top10, dx_top50]))