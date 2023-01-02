import glob
from books import Review
import click
import datetime as dt

reviews = []


if __name__ == "__main__":
    datafiles = glob.glob('./data/**/index.md', recursive=True)
    for d in datafiles:
        r = Review(path=d)
        reviews.append(r)
    
    for r in reviews:
        # if r.metadata['book']['cover_image_url'] == '':
        #     click.echo("Finding cover for " + r.metadata['book']['title'])
        #     r.find_google_cover()
        #     r.save()
        # if isinstance(r.metadata['review']['date_read'],str):
        #     date = dt.datetime.strptime(r.metadata['review']['date_read'], "%Y-%m-%d").date()
        #     r.metadata['review']['date_read'] = [date]
        #     r.save()
        # if isinstance(r.metadata['review']['rating'],str):
        #     r.metadata['review']['rating'] = int(r.metadata['review']['rating'])
        #     r.save()
        if r.metadata['book']['pages'] == None:
            r.metadata['book']['pages'] = 0
            r.save()
