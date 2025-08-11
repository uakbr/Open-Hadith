import json
import os

from flask import Flask, request, send_from_directory, jsonify
from flask.templating import render_template
from flask_cors import CORS
from flask_sslify import SSLify

from src.local_search import LocalHadithSearch


app = Flask(__name__, static_folder="../../frontend/build", static_url_path="/")
# Disable SSL redirect in development
if os.getenv("FLASK_ENV") != "development":
    sslify = SSLify(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"

# Initialize local search
local_search = LocalHadithSearch()
print("Using local JSON data for search")


@app.route("/api/search", methods=["GET"])
def search_api():
    sr = request.args.get("search")
    if not sr:
        return jsonify([])
    
    try:
        results = local_search.search_hadith(sr)
        return jsonify(results)
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify([])


@app.route("/api/v2/search", methods=["GET"])
def search_api_v2():
    sr = request.args.get("search")
    if not sr:
        return jsonify([])
    
    try:
        # Use local JSON search with advanced features
        results = local_search.search_hadith_advanced(sr)
        return jsonify(results)
    except Exception as e:
        print(f"Search v2 error: {e}")
        return jsonify([])


@app.route("/api/<collection_id>/<book>/<book_ref_no>", methods=["GET"])
def get_hadith_by_book_ref_api(collection_id, book, book_ref_no):
    try:
        result = local_search.get_hadith_by_reference(collection_id, book, book_ref_no)
        return jsonify(result) if result else (jsonify({}), 404)
    except Exception as e:
        print(f"Get hadith error: {e}")
        return jsonify({}), 404


@app.route("/b/<collection_id>/<book>/<book_ref_no>", methods=["GET"])
def get_hadith_by_book_ref(collection_id, book, book_ref_no):
    try:
        s = local_search.get_hadith_by_reference(collection_id, book, book_ref_no)
        
        if s:
            return render_template("single_hadith.html", hadith=s)
        else:
            return render_template("404.html")
    except Exception as e:
        print(f"Template render error: {e}")
        return render_template("404.html")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(app.static_folder + "/" + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
