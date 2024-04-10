from requests import post

print(post(f'http://localhost:8080/api/users', json={'login': "None2",
                                                     'description': "NONO",
                                                     'hashed_password': "1234"}).json()["message"])
