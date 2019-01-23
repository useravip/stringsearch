from flask import Flask, jsonify, make_response, request, abort
import utils
import time
from operator import itemgetter

app = Flask(__name__)

@app.route('/api/search', methods=['POST'])
def search():
    if not request.json or not 'name' in request.json:
        return abort(400)
    start = time.time()
    trie = utils.Utils.load_data()
    results = utils.Utils.search(request.json.get('name').lower(), 5, trie)
    end = time.time()
    print(end-start)
    # sort the result by ranking
    return jsonify(sorted(results, key=itemgetter(1)))


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)

