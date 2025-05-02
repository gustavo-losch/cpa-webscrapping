import requests

BASE_URL = "http://127.0.0.1:5000"

#1. Insert
new_game = {
    "title": "Test Game",
    "release_date": "2022-01-01",
    "developer": "Dev Co",
    "publisher": "Pub Co",
    "genres": "Indie",
    "multiplayer_or_singleplayer": "Single-player",
    "price": "100",
    "dc_price": "90",
    "overall_review": "Positive",
    "detailed_review": "Mostly Positive",
    "reviews": "500",
    "percent_positive": "95",
    "win_support": "1",
    "mac_support": "1",
    "lin_support": "0"
}
res = requests.post(f"{BASE_URL}/insert", json=new_game)
print(res.json())

#2. Update
update_data = {
    "title": "Test Game",
    "reviews": "1000"
}
res = requests.patch(f"{BASE_URL}/update", json=update_data)
print(res.json())

#3. Delete
delete_json = {"title": "Test Game"}
res = requests.delete(f"{BASE_URL}/delete", json=delete_json)
print(res.json())

#4. Get n rows
res = requests.get(f"{BASE_URL}/get/5")
print(res.json())

#5. Filter com overall_review = "Positive"
res = requests.get(f"{BASE_URL}/select/Positive")
print(res.json())

# 6. Filter com diversas colunas
filter_fields = {
    "publisher": "Valve",
    "dc_price": "Free to play"
}
res = requests.get(f"{BASE_URL}/select_fields", json=filter_fields)
print(res.json())
