import requests
def main(args):
	google_body = requests.get("https://www.google.com")
	return {"body": str(google_body.content)}
