import os



# 🧰 Upload path helper (global, accessible anywhere)
def get_upload_path(category):
    base = os.path.join(os.getcwd(), 'backend', 'uploads')
    return {
        "pet": os.path.join(base, 'pet_images'),
        "user": os.path.join(base, 'user_images'),
        "medical": os.path.join(base, 'medical'),
    }.get(category, base)