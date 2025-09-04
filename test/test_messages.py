from datetime import datetime


def test_create_message_ok(client):
    payload = {
        "message_id": "msg-2",
        "session_id": "session-abcdef",
        "content": "Hola, ¿cómo puedo ayudarte hoy?",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "user",
        "extra_metadata": {},
    }
    response = client.post("/api/messages", json=payload)
    assert response.status_code == 200  # ✅ reactivado

    data = response.json()
    assert data["message_id"] == payload["message_id"]
    assert data["session_id"] == payload["session_id"]
    assert "extra_metadata" in data
    assert data["extra_metadata"]["word_count"] == len(payload["content"].split())


def test_create_message_invalid_sender(client):
    payload = {
        "message_id": "msg-1",
        "session_id": "session-abcdef",
        "content": "Hola, ¿cómo puedo ayudarte hoy?",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "Juan",  
        "extra_metadata": {"word_count": 2},
    }
    response = client.post("/api/messages", json=payload)
    assert response.status_code == 422 


def test_create_message_banned_word(client):
    payload = {
        "message_id": "msg-3",
        "session_id": "session-abcdef",
        "content": "Hola, ¿cómo puedo ayudarte hoy? malo",  
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "user",
    }
    response = client.post("/api/messages", json=payload)
    assert response.status_code == 400 


def test_get_messages_with_pagination(client):
    # Insertar 3 mensajes
    for i in range(3):
        payload = {
            "message_id": f"msg-{i+10}",
            "session_id": "s2",
            "content": f"Mensaje {i}",
            "timestamp": "2023-06-15T14:30:00Z",
            "sender": "user",
        }
        client.post("/api/messages", json=payload)

    # Obtener solo 2 mensajes
    response = client.get("/api/messages/s2?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_messages_filter_by_sender(client):
    # Insertar mensajes con diferentes sender
    payload_user = {
        "message_id": "msg-19",
        "session_id": "s2",
        "content": "Hola, ¿cómo puedo ayudarte hoy?",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "user",
    }
    payload_system = {
        "message_id": "msg-20",
        "session_id": "s2",
        "content": "claro, ¿en qué puedo ayudarte?",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "system",
    }
    client.post("/api/messages", json=payload_user)
    client.post("/api/messages", json=payload_system)

    # Filtrar solo mensajes de sender=user
    response = client.get("/api/messages/s2?sender=user")
    assert response.status_code == 200
    data = response.json()
    assert all(msg["sender"] == "user" for msg in data)
    assert all(msg["session_id"] == "s2" for msg in data)
