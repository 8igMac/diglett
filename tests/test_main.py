from diglett.main import app
from fastapi.testclient import TestClient
import json

client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"msg": "Hello World"}

def test_embed():
    filename = "tests/data/homer.wav"
    with open(filename, "rb") as f:
        # NOTE: key should be "file".
        res = client.post("/embed", files={"file": f})
        assert res.status_code == 200
    json_data = res.json()
    assert "speaker_name" in json_data
    assert json_data["avg_db"] == 562.2520378076098
    with open("tests/data/emb.json") as f:
      emb = json.load(f)
      assert json_data["speaker_embedding"] == emb["homer_emb"]


def test_speaker_verification():
    pass