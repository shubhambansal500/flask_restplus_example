{
    "register": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 2, "maxLength": 100},
            "email": {"type": "integer", "format": "email"}
        },
        "required": ["name", "email"]
    }
}