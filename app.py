from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


@app.route(
    "/",
    # We need to tell Flask to accept POST requests on this route, so the user can post the form
    methods=["GET", "POST"],
)
def home():
    # HTTP requests can be either GET or POST. If that’s a POST request it means
    # the comment form was posted (because of the `method="post"` in the
    # home.html file), and in that case we save the comment. If that’s not a
    # POST request, it means that’s a GET request and in that case we display
    # the page normally
    if request.method == "POST":
        # `request.form` contains the data of the posted form. The keys `author`
        # and `comment` match the field names of the form (eg. `<input
        # name="author">`)
        add_guestbook_comment(request.form["author"], request.form["comment"])
        # When doing a POST request it’s a good practice to redirect the user
        # somewhere. If you don’t do that, when the user reloads the page, they
        # might resubmit the form!
        return redirect(url_for("home"))

    guestbook_entries = get_guestbook_entries()

    return render_template("home.html", guestbook=guestbook_entries)


def get_guestbook_entries():
    """
    Return the list of guestbook entries as a list of dictionaries. Each
    dictionary has the keys "author", "comment" and "posted_at".
    """
    import datetime
    import json

    try:
        with open("guestbook.json", "r") as fp:
            guestbook = [
                {
                    **entry,
                    "posted_at": datetime.datetime.fromisoformat(entry["posted_at"]),
                }
                for entry in json.load(fp)
            ]
    except (IOError, ValueError):
        guestbook = []

    return guestbook


def add_guestbook_comment(author, comment):
    """
    Add a new comment by author in the guestbook.
    """
    import datetime
    import json

    entries = [
        {**entry, "posted_at": entry["posted_at"].isoformat()}
        for entry in get_guestbook_entries()
    ]
    new_entry = {
        "author": author,
        "comment": comment,
        "posted_at": datetime.datetime.now().isoformat(),
    }

    with open("guestbook.json", "w") as fp:
        json.dump([new_entry] + entries, fp)
