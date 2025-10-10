# tests/test_users.py
import pytest

def user_payload(name="Johannan", email="js@atu.ie", age=25, sid="S1234567"):
 return {"name": name, "email": email, "age": age, "student_id": sid}

#testing to see if user is created properly
def test_create_user_ok(client):
 r = client.post("/api/users", json=user_payload())
 assert r.status_code == 201
 data = r.json()
 assert data["name"] == "Johannan"
 assert data["email"] == "js@atu.ie"
 assert data["age"] == 25

def test_user_id_generated(client):
 r1 = client.post("/api/users", json=user_payload(name="Sean"))
 r2 = client.post("/api/users", json=user_payload(name="Mary"))
 assert r1.status_code == 201
 assert r2.status_code == 201
 assert r1.json()["user_id"] != r2.json()["user_id"]

#Tests to see if there is duplicate user ids
def test_duplicate_user_id_conflict(client):
 client.post("/api/users", json=user_payload(name = "Ava"))
 existing_id = user.json()["user_id"]

 duplicate_payload = user_payload(name="Liam")
 duplicate_payload["user_id"] = existing_id
 r = client.post("/api/users", json=duplicate_payload)

 assert r.status_code == 409 # duplicate id -> conflict
 assert "exists" in r.json()["detail"].lower()



# COME BACK TO THIS, WE NEED TO MAKE A PASSPORT TYPE CHECK
# #testing for bad student ids using parameterized test
# @pytest.mark.parametrize("bad_sid", ["BAD123", "s1234567", "S123", "S12345678"])
# def test_bad_student_id_422(client, bad_sid):
#  r = client.post("/api/users", json=user_payload(uid=3, sid=bad_sid))
#  assert r.status_code == 422 # pydantic validation error




#testing to see if users can be got
def test_get_user_404(client):
 r = client.get("/api/users/999")
 # pydantic validation error
 assert r.status_code == 404 

#testing to see if user can be deleted
def test_delete_then_404(client):
 r1 = client.post("/api/users", json=user_payload(name="Deleteme"))
 user_id = r1.json()["user_id"]

 r2 = client.delete(f"api/users/{user_id}")
 assert r2.status_code == 204

 r3 = client.delete(f"/api/users/{user_id}")
 assert r3.status_code == 404
 
 #Testing Put(Update)
def test_update_then_404(client):
 r1 = client.post("/api/users", json=user_payload(name="Sean"))
 user_id = r1.json()["user_id"]

 update_payload = user_payload(name = "UpdatedSean")
 r2 = client.put(f"/api/users/{user_id}", json=update_payload())
 assert r2.status_code == 200

 r3 = client.put("/api/users/BA999999", json=user_payload())
  # pydantic validation error
 assert r3.status_code == 404

 #testing for bad student names using parameterized test
 @pytest.mark.parametrize("bad_name",["ab","Johan","A" * 51]) #Multiplys by 51 to make it too long
 def test_bad_student_id_422(client,bad_name):
  r = client.post("/api/user",json=user_payload(name = bad_name))
  #pydantic validation
  assert r.status_code == 422 