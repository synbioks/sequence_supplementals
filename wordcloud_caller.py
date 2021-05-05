import os, csv
import matplotlib.pyplot as plt
from wordcloud import WordCloud

cwd = os.getcwd()

reader = csv.reader(open(os.path.join(cwd, 'Species Names in iGem long descriptions.csv'), newline='\n'))
d={}

with open(os.path.join(cwd, 'Species Names in iGem long descriptions.csv'), newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    for freq, name in csv_reader:
        if len(name)>0:
            d[name] = float(freq)


# for line in reader:
#     print(line)
    # d[key] = float(value)

wordcloud = WordCloud().generate_from_frequencies(d)
fig = plt.figure()
fig.set_figwidth(400)
fig.set_figheight(100)

plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
fig.savefig(os.path.join(cwd, 'wordcloud.png'), pad_inches=0)