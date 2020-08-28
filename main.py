import pymongo
import time
import flask
from flask import jsonify, Flask, request, redirect, render_template, flash

# Initialising Flask and MongoDB
app = Flask(__name__)
app.secret_key = "&_LS9::#-/:2w)G|j2;GI~zYu];fH$"
app.config["JSON_SORT_KEYS"] = False

db_client = pymongo.MongoClient(host="db" , port=27017, username="root", password="rootpassword", authMechanism="SCRAM-SHA-256")
db = db_client["Games-Library"]
col = db["ReleasedGames"]


@app.route("/", methods=["GET","POST"])
def index_page():
    return render_template("index.html")


@app.route("/add_game", methods=["GET","POST"])
def add_game_page():
    if request.method == "POST":
        # game_form = request.form["gameform"]
        user_title = request.form["title"]
        user_title_release_date = request.form["release"]
        user_title_platform = request.form["platform"]
        user_title_starrating = request.form["starrating"]
        insert_into_db(user_title, user_title_release_date, user_title_platform, user_title_starrating)
        flash("Inserted record " + str(user_title) + " into our DB, thanks for your input!")
        return render_template("add_game.html")
    return render_template("add_game.html")


# @app.route("/api/hiragana", methods=["GET"])
# def api_hiragana():
#     return {
#         "hiragana": {
#             "Hiragana": hiragana_list,
#             "Romaji": romaji_list
#             }
#     }


@app.route("/about", methods=["GET"])
def about_page():
    return render_template("about.html")


@app.route("/search_games", methods=["GET", "POST"])
def search_games_page():
    if request.method == "POST":
        result_title = request.form["searchedtitle"]
        db_result = retrieve_from_db(result_title)
        if db_result == None:
            print("There are no records of this game.")
            return "0"
        else:
            game_title = db_result.get("name")
            release_date = db_result.get("release_date")
            platform = db_result.get("platform")
            star_rating = db_result.get("star_rating")
            return render_template("search_results.html", game_title=game_title, release_date=release_date, game_platform=game_platform, star_rating=star_rating)
    return render_template("search_games.html")


@app.route("/search_results")
def search_results():
    pass


@app.route("/api/", methods=["GET"])
def api_games():
    games_list = []
    game_titles = []
    game_releases = []
    game_platform = []
    game_starrating = []
    for document in col.find():
        games_list += document
        game_titles.append(document.get("name"))
        game_releases.append(document.get("release_date"))
        game_platform.append(document.get("platform"))
        game_starrating.append(document.get("star_rating"))
        
    return {        
        "games": {
                "title": game_titles, 
                "release": game_releases,
                "platform": game_platform,
                "starrating": game_starrating
        }
    }

def insert_into_db(title, release, platform, starrating):
    col.insert_one({"name": title, "release_date": release, "platform": platform, "star_rating": starrating})
    print("Inserted into DB")


def retrieve_from_db(name):
    name_variable = name
    result = col.find_one({"name": name_variable})
    print(result)
    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
