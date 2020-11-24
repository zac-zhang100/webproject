from app import create_app

s = create_app()
s.run("127.0.0.1", 5000, True)
