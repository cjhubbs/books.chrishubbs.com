from books import Review
import inquirer
import click 
import datetime as dt
import os
import json
from pathlib import Path

INDEX_FILE = Path('./data/index.json')

def load_index():
    """Load the ISBN index from JSON file."""
    if INDEX_FILE.exists():
        with open(INDEX_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_index(index):
    """Save the ISBN index to JSON file."""
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEX_FILE, 'w') as f:
        json.dump(index, f, indent=2)

def update_index(isbn13, title, entry_type):
    """Add a new book to the index."""
    index = load_index()
    index[isbn13] = {
        'title': title,
        'type': entry_type,
        'added': dt.date.today().isoformat()
    }
    save_index(index)

if __name__ == "__main__":

    isbns = load_index()

    questions = [
        inquirer.Text("isbn", "Input the ISBN13:"),
        inquirer.Text("read_date", "Date Read:", default=dt.date.today())
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
        click.echo("ISBN " + response['isbn'] + " already exists: " + isbns[response['isbn']]['title'])
        click.echo("Exiting.")
    else:
        metadata = {'book': {'isbn13': response['isbn']}}
        r = Review(entry_type=entry_type, metadata=metadata)
        r.get_google_info(response['isbn'])
        if 'title' in r.metadata['book'].keys():
            click.echo("Found " + r.metadata['book']['title'])
        if entry_type == 'reviews':
            r.metadata['review'] = {}
            r.metadata['review']['date_read'] =  [dt.datetime.strptime(response['read_date'],'%Y-%m-%d').date()]
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
        update_index(response['isbn'], r.metadata['book'].get('title', 'Unknown'), entry_type)
        r.find_google_cover()
        r.save()
        os.system('vi' + ' "' + str(r.path) + '" </dev/tty >/dev/tty 2>&1')
        click.echo("Record created! Don't forget to write a review before publishing the site!")
