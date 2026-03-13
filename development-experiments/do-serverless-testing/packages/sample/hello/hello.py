

def main(args):
	name = args.get("name", "stranger")
	greeting = "Hello " + name + "!!!!!"
	print(args)
	greeting += str(args)
	return {"body": greeting}
