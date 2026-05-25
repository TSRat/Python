import json
with open("document.txt", "a", encoding = "utf-8") as f:
    f.write("\nHello World Again!")

data = '{"name": "Tom"}'
obj = json.loads(data)
print(obj["name"])

data2 = {"name": "Tommy", "age": 100}
jbo = json.dumps(data2)
print(jbo)

data3 = {"name": "Xavier", "age": 70, "gender": "intersex"}
with open("data.json", "w", encoding = "utf-8") as k:
    json.dump(data3, k)


with open("data.json", "r", encoding = "utf-8") as g:
    job = json.load(g)
print(job["name"])
