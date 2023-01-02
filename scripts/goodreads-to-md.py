import csv
import os 
import re
import shutil 
import sys
from unidecode import unidecode
import frontmatter 


def slugify(text):
    """Convert Unicode string into blog slug."""
    # https://leancrew.com/all-this/2014/10/asciifying/
    text = re.sub("[–—/:;,.]", "-", text)  # replace separating punctuation
    ascii_text = unidecode(text).lower()  # best ASCII substitutions, lowercased
    ascii_text = re.sub(r"[^a-z0-9 -]", "", ascii_text)  # delete any other characters
    ascii_text = ascii_text.replace(" ", "-")  # spaces to hyphens
    ascii_text = re.sub(r"-+", "-", ascii_text)  # condense repeated hyphens
    ascii_text = ascii_text.rstrip("-")
    return ascii_text

if __name__ == "__main__":

    base_path = "/Users/chris/goodreads-to-md/data"
    reviews_path = base_path + "/reviews"
    to_read_path = base_path + "/to-read"
    shutil.rmtree(base_path, ignore_errors=True)
    os.mkdir(base_path)
    os.mkdir(reviews_path)
    os.mkdir(to_read_path)

    with open(sys.argv[1]) as csvfile:
        reader = csv.reader(csvfile,quotechar='"',delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True)

        for l in reader:
            data_path = base_path
            if 'reads' in l[17]:
                data_path = reviews_path
            elif 'to-read' in l[17]:
                data_path = to_read_path
            else:
                continue
            metadata = {
                'book': {},
                'plan': {},
                'review': {}
            }
            author_slug = slugify(l[2])

            long_title = l[1]
            series_match = re.search("\((.+),\s\#(\d+)\)",long_title)
            series = ""
            series_num = ""
            if series_match:
                series = series_match[1]
                series_num = series_match[2]
                long_title = re.sub("\(.*\)","",long_title).strip()
            title_slug = slugify(long_title)
            long_title = re.sub("\'","\\\'",long_title)
            print(author_slug, title_slug)

            outdir = data_path + "/" + author_slug
            bookdir = outdir + "/" + title_slug 
            if not os.path.exists(outdir):
                os.mkdir(outdir)
            if not os.path.exists(bookdir):
                os.mkdir(bookdir)
            filename = bookdir + "/" + "index.md"
            date_added = re.sub("/","-",l[15])
            date_read = re.sub("/","-",l[16])

            metadata['book']['author'] = re.sub("\s+"," ",l[2])
            metadata['book']['goodreads'] = l[0]
            metadata['book']['isbn9'] = re.sub("=|\"","",l[5])
            metadata['book']['isbn13'] = re.sub("=|\"","",l[6])
            metadata['book']['owned'] = ''
            metadata['book']['pages'] = l[11]
            metadata['book']['publication_year'] = l[12]
            metadata['book']['series'] = series 
            metadata['book']['series_position'] = l[12]
            metadata['book']['spine_color'] = ''
            metadata['book']['tags'] = ''
            metadata['book']['title'] = long_title
            metadata['book']['cover_image_url'] = ''
            metadata['review']['date_read'] = date_added 
            metadata['review']['rating'] = l[7]
            metadata['plan']['date_added'] = ''

            with open(filename, "wb") as out_file:
                frontmatter.dump(
                    frontmatter.Post(content=l[19], **metadata), out_file
                )
                out_file.write(b"\n")

# Book Id	
# Title	
# Author	
# Author l-f	
# Additional Authors	
# ISBN	
# ISBN13	
# My Rating	
# Average Rating	
# Publisher	
# Binding	
# Number of Pages	
# Year Published	
# Original Publication Year	
# Date Read	
# Date Added	
# Bookshelves	
# Bookshelves with positions	
# Exclusive Shelf	
# My Review	
# Spoiler	
# Private Notes	
# Read Count	
# Owned Copies


        
        