import base64
import json
from datetime import datetime
from bson import ObjectId


def encode_cursor(created_at: datetime, note_id: ObjectId) -> str:
    data = {
        "created_at": created_at.isoformat(),
        "id": str(note_id)
    }

    json_data = json.dumps(data)

    return base64.urlsafe_b64encode(
        json_data.encode()
    ).decode()


def decode_cursor(cursor: str) -> tuple[datetime, ObjectId]:
    json_data = base64.urlsafe_b64decode(
        cursor.encode()
    ).decode()

    data = json.loads(json_data)

    created_at = datetime.fromisoformat(data["created_at"])
    note_id = ObjectId(data["id"])

    return created_at, note_id
