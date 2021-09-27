from src.app import app, logger, config

if __name__ == "__main__":
	logger.info(f"APP_ENV={config['APP_ENV']}")
	if config["APP_ENV"] == "prd":
		app.run(host="0.0.0.0")
	else:
		app.run(host="127.0.0.1")