from diglett.main import app
from fastapi.testclient import TestClient
import json

client = TestClient(app)

def test_ping():
    res = client.get("/ping")
    assert res.status_code == 200
    assert res.json() == {"msg": "pong"}

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
      assert len(json_data["speaker_embedding"]) == len(emb["homer_emb"])
      for i in range(len(emb["homer_emb"])):
        assert abs(json_data["speaker_embedding"][i] - emb["homer_emb"][i]) < 0.001 


def test_speaker_verification():
    pass