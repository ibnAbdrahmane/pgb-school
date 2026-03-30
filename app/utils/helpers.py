def generate_matricule(user_id):
    from datetime import datetime
    year = datetime.now().year
    return f"PGB{year}{user_id:04d}"


def generate_numero_carte(user_id):
    from datetime import datetime
    year = datetime.now().year
    return f"C{year}{user_id:05d}"
