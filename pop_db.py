from app import app, db
from models import Movie, User

with app.app_context():
    db.create_all()  

    # Add movies
    movie1 = Movie(
        title="Code & Quills", 
        description="Max, a brilliant hedgehog programmer, embarks on a thrilling journey to create the ultimate app, while navigating the quirks and joys of coding from his cozy home office.", 
        youtube_link="https://www.youtube.com/embed/2jQco8hEvTI",
        image_url="/static/images/hedgehog_developer.png"  
    )
    movie2 = Movie(
        title="Palette of Prickles", 
        description="In his vibrant studio, Max, the creative hedgehog, brings his imaginative designs to life with colorful sketches and digital artistry, aiming to win a prestigious design contest.", 
        youtube_link="https://www.youtube.com/embed/TIxxIEEvczM",
        image_url="/static/images/hedgehog_designer.png"  
    )
    movie3 = Movie(
        title="Data Spikes", 
        description="Donning his lab coat, Max delves into the world of data analysis, uncovering fascinating insights and solving complex problems, all from his sleek, modern office.", 
        youtube_link="https://www.youtube.com/embed/dQw4w9WgXcQ",
        image_url="/static/images/hedgehog_data_scientist.png"  
    )

    db.session.add_all([movie1, movie2, movie3])

    # Add admin user
    admin_user = User(
        username="admin",
        email="admin@posthog.com",
        plan="Premium",
        is_admin=True
    )
    admin_user.set_password("admin")
    db.session.add(admin_user)

    db.session.commit()

    print("Movies and admin user added to the database!")