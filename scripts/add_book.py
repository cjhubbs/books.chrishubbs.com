from books import Review
import inquirer
import click 
import glob
import datetime as dt


reviews = []
isbns = {}

if __name__ == "__main__":

    review_files = glob.glob('./data/reviews/**/index.md', recursive=True)
    to_read_files = glob.glob('./data/to-read/**/index.md', recursive=True)
    datafiles = review_files + to_read_files
    for d in datafiles:
        r = Review(path=d)
        reviews.append(r)
        isbns[r.metadata['book']['isbn13']] = r 

    questions = [
        inquirer.Text("isbn", "Input the ISBN13:")
    ]
    entry_type = inquirer.list_input(
        message="What type of book is this?",
        choices=[
            ("One I’ve read", "reviews"),
            ("One I want to read", "to-read"),
        ],
        carousel=True,
    )
    response = inquirer.prompt(questions)
    if response['isbn'] in isbns.keys():
        click.echo("ISBN " + response['isbn'] + " already exists: " + isbns[response['isbn']].metadata['book']['title'])
        click.echo("Exiting.")
    else:
        metadata = {'book': {'isbn13': response['isbn']}}
        r = Review(entry_type=entry_type, metadata=metadata)
        r.get_google_info(response['isbn'])
        if 'title' in r.metadata['book'].keys():
            click.echo("Found " + r.metadata['book']['title'])
        if entry_type == 'reviews':
            r.metadata['review'] = {}
            r.metadata['review']['date_read'] =  [dt.date.today()]
            rating = inquirer.list_input(
                message="What’s your rating?",
                choices=[("⭐⭐⭐⭐⭐", 5), ("⭐⭐⭐⭐", 4), ("⭐⭐⭐", 3), ("⭐⭐", 2), ("⭐", 1)],
                default=0,
                carousel=True,
            )
            r.metadata['review']['rating'] = rating
            owned = inquirer.list_input(
                message="Do you own this book?",
                choices=[("Yes", True), ("No", False)],
                default=False,
                carousel=True,
            )
            r.metadata['book']['owned'] = owned
        r.save()
        r.find_google_cover()
        r.save()
        click.echo("Record created! Don't forget to write a review before publishing the site!")
