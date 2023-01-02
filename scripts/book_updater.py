import glob
from books import Review
import click

reviews = []


if __name__ == "__main__":
    datafiles = glob.glob('./data/**/index.md', recursive=True)
    for d in datafiles:
        r = Review(path=d)
        reviews.append(r)
    
    for r in reviews:
        if r.metadata['book']['cover_image_url'] == '':
            click.echo("Finding cover for " + r.metadata['book']['title'])
            r.find_google_cover()
            r.save()
