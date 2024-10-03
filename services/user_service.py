from models.user_model import User


def search_users(query, page, per_page):
    if query:
        return User.query.filter(
            (User.name.ilike(f"%{query}%")) | (User.email.ilike(f"%{query}%"))
        ).paginate(page=page, per_page=per_page)
    return User.query.paginate(page=page, per_page=per_page)
