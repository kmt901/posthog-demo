from app import app, db
from models import Movie

with app.app_context():
    db.create_all()  # Ensure all tables are created

    movie1 = Movie(
        title="Movie 1", 
        description="Description for movie 1", 
        youtube_link="https://www.youtube.com/embed/dQw4w9WgXcQ",
        image_url="https://via.placeholder.com/300x450?text=Movie+1"  # Placeholder image URL
    )
    movie2 = Movie(
        title="Movie 2", 
        description="Description for movie 2", 
        youtube_link="https://www.youtube.com/embed/dQw4w9WgXcQ",
        image_url="https://via.placeholder.com/300x450?text=Movie+2"  # Placeholder image URL
    )
    movie3 = Movie(
        title="Movie 3", 
        description="Description for movie 3", 
        youtube_link="https://www.youtube.com/embed/dQw4w9WgXcQ",
        image_url="https://via.placeholder.com/300x450?text=Movie+3"  # Placeholder image URL
    )

    db.session.add(movie1)
    db.session.add(movie2)
    db.session.add(movie3)
    db.session.commit()

    print("Movies added to the database!")
