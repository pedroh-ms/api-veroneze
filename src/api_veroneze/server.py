from api_veroneze import make_app
import waitress

waitress.serve(make_app(), port=5000)
