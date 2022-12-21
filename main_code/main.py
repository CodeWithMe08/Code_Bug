from initial import app
from routers import post_routes, auth, user_routes, administrator, custom_error, contact_routes


if __name__=="__main__":
    app.run(debug=True)