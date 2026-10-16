from app import app
c = app.test_client()
assert c.get("/").status_code == 200
r = c.post("/analyze", data={"name":"Anjali Reddy","city":"Warangal","skills":"MS Excel, typing, Communication, html, canva","interests":"marketing, data","education":"B.Com, Kakatiya University, 2025","experience":"Managed college fest social media\nData entry intern at local firm"})
assert r.status_code == 200 and b"fit" in r.data
r = c.post("/resume", data={"name":"Anjali Reddy","city":"Warangal","skills":"excel, typing, communication","target_role":"Data Entry Operator","education":"B.Com"})
assert r.status_code == 200 and r.data[:4] == b"%PDF"
assert c.post("/analyze", data={"skills":""}).status_code == 400
print("all tests passed")
