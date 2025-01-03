from app import app, db
from models import Movie, User

with app.app_context():
    db.create_all()  

    # Add movies
    movie1 = Movie(
        title="Code & Quills", 
        genre="Family",
        description="Max, a brilliant hedgehog programmer, embarks on a thrilling journey to create the ultimate app, while navigating the quirks and joys of coding from his cozy home office.", 
        youtube_link="https://www.youtube.com/embed/2jQco8hEvTI",
        image_url="/static/images/hedgehog_developer.png"  
    )
    movie2 = Movie(
        title="Palette of Prickles", 
        genre="Family",
        description="In his vibrant studio, Max, the creative hedgehog, brings his imaginative designs to life with colorful sketches and digital artistry, aiming to win a prestigious design contest.", 
        youtube_link="https://www.youtube.com/embed/TIxxIEEvczM",
        image_url="/static/images/hedgehog_designer.png"  
    )
    movie3 = Movie(
        title="Data Spikes", 
        genre="Family",
        description="Donning his lab coat, Max delves into the world of data analysis, uncovering fascinating insights and solving complex problems, all from his sleek, modern office.", 
        youtube_link="https://www.youtube.com/embed/lYBUbBu4W08?si=b65lgJb43lzHLh5x",
        image_url="/static/images/hedgehog_data_scientist.png"  
    )

    movie4 = Movie(
        title="Fists of Fury", 
        genre="Action",
        description="Max, the underdog hedgehog with a heart of gold, steps into the ring to prove his worth against the toughest opponents. With each punch, he battles not just for victory, but for his place in a world that underestimates him, fighting to rise as the champion of the streets.", 
        youtube_link="https://www.youtube.com/embed/dQw4w9WgXcQ",
        image_url="/static/images/hedgehog_rocky.jpg"  
    )

    movie5 = Movie(
        title="Spikes & Consequences", 
        genre="Action",
        description="In the shadowy underworld of Hedgetown, Max finds himself embroiled in a high-stakes confrontation with some of the most dangerous figures in town. With quick reflexes and a sharper tongue, he navigates a web of crime and chaos, making sure every action has its consequence.", 
        youtube_link="https://www.youtube.com/embed/dQw4w9WgXcQ",
        image_url="/static/images/hedgehog_pulp.jpg"  
    )

    movie6 = Movie(
        title="The Hedge Abides", 
        genre="Action",
        description=" Max, the laid-back but sharp-witted hedgehog, finds himself drawn into a bizarre mystery at the local bowling alley. Armed with nothing but his easy-going charm and a strong sense of right and wrong, he rolls through life’s oddities with style, proving that sometimes, the coolest heroes are the most unexpected.", 
        youtube_link="https://www.youtube.com/embed/dQw4w9WgXcQ",
        image_url="/static/images/hedgehog_dude.jpg"  
    )

    db.session.add_all([movie1, movie2, movie3, movie4, movie5, movie6])

    # Add admin user
    admin_user = User(
        username="admin",
        email="admin@posthog.com",
        plan="Premium",
        is_admin=True,
        is_adult=False
    )
    admin_user.set_password("admin")
    db.session.add(admin_user)

    db.session.commit()

    print("Movies and admin user added to the database! Yay.")