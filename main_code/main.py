from initial import app
from routers import post_routes, auth_routes, user_routes, admin_routes, error_routes, contact_routes


if __name__=="__main__":
    app.run(debug=True)