from src.app import app
from src.models.factory import Factory

@app.route("/instances", methods=["POST"])
def create_an_instance():
	Factory.setup()
	return {"status": "success"}