



# 🧰 Upload path helper (global, accessible anywhere)
def get_upload_path(category):
    base = os.path.join(os.getcwd(), 'backend', 'uploads')
    return {
        "pet": os.path.join(base, 'pet_images'),
        "user": os.path.join(base, 'user_images'),
        "data": os.path.join(base, 'data'),
    }.get(category, base)