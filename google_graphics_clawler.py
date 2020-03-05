import threading
import urllib
import os
import argparse
import requests
import bs4

GOOGLE_GRAPHICS_REQUEST_QUERY = "https://www.google.com/search?q=%s&tbm=isch&start=%d"

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-q", "--query", required=True, help="Query for searching images")
arg_parser.add_argument("-o", "--output", required=True, help="Directory used to store downloaded images")
arg_parser.add_argument("-n", "--number", type=int, required=True, help="Minimum number of photos")
args = arg_parser.parse_args()

query = args.query.split(' ')
query = '+'.join(query)

print("Start fetching your images ...")

images_urls = []
while len(images_urls) < args.number:
    request = requests.get(GOOGLE_GRAPHICS_REQUEST_QUERY % (query, len(images_urls)))
    soup = bs4.BeautifulSoup(request.text, features="html.parser")
    images = soup.body.find_all('img', attrs={'style':'border:1px solid #ccc;padding:1px'})
    for image in images:
        images_urls.append(image.attrs["src"])

print("Images urls successfully fetched!")

if not os.path.exists(args.output):
    os.makedirs(args.output)

def retrive_image(url, index):
    urllib.request.urlretrieve(url, "%s/retrived_%d.jpg" % (args.output, index))

print("Start downloding %d images ..." % len(images_urls))
threads = []
for index, image_url in enumerate(images_urls):
    thread = threading.Thread(target=retrive_image, args=(image_url, index))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("Done!")