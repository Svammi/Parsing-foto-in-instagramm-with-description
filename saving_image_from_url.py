



import urllib.request
import requests
from PIL import Image
import re
import json
import pprint
# save image
url = "https://instagram.fiev2-1.fna.fbcdn.net/v/t51.2885-15/e35/c7.0.306.306a/54512442_411420809658132_4188070236825027980_n.jpg?_nc_ht=instagram.fiev2-1.fna.fbcdn.net&_nc_cat=100&_nc_ohc=wg4yfB_AwkcAX9CO_sm&oh=f1196d965b1b92e31270887d3234b615&oe=5E7EA0A8"

out = urllib.request.urlopen(url)
img1 = Image.open(out,'r')
img1 = img1.save('first.jpg')

page = requests.get('https://www.instagram.com/studia_art_web/')
html_text = page.text
reg = 'window._sharedData = .*?</script>'
json_object = re.findall(reg, html_text)[0][21:-10]

json_object = json.loads(json_object)
with open('data.txt', 'w') as outfile:
    outfile.write(json.dumps(json_object, indent=4))
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(json_object)



