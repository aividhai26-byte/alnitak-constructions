"""
Database Initialization Script
Creates database tables and inserts seed data for development
"""

from app import create_app, db
from app.services.auth_service import hash_password
from datetime import datetime, date


def init_database():
    """
    Initialize database with seed data
    """
    app = create_app('development')
    
    with app.app_context():
        # Import models within app context
        from app.models import User, Project, ProjectPhoto, Service, Testimonial, ContactMessage, TeamMember, ImageGallery
        from app.models import Base
        
        # Create all tables using Base metadata
        Base.metadata.create_all(bind=db.engine)
        
        print("Database tables created successfully.")
        
        # Check if admin user already exists
        admin = db.session.query(User).filter_by(username='admin').first()
        
        if not admin:
            # Create admin user
            admin = User(
                username='admin',
                email='alnitakconstructions@gmail.com',
                password_hash=hash_password('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            print("Admin user created (username: admin, password: admin123)")
        else:
            admin.email = 'alnitakconstructions@gmail.com'
            print("Admin user already exists. Email updated.")
        
        # Check if sample projects exist
        if db.session.query(Project).count() == 0:
            # Create sample projects using local images
            projects = [
                Project(
                    title='Tiruppur Residential Villa',
                    short_description='Premium contemporary villa featuring double height ceilings and customized styling details.',
                    description='A landmark residential villa featuring a sleek double-height foyer, premium granite finishes, and highly efficient architectural design. Crafted for maximum ventilation and light, this home sits in the heart of Tiruppur and has been completed to the absolute highest quality standards.',
                    category='completed',
                    client='Mrs. Kavitha Arumugam',
                    location='Tiruppur, Tamil Nadu',
                    area_sqft='3,200 sq.ft',
                    floors='G+2',
                    project_type='Residential Villa',
                    start_date=date(2023, 1, 15),
                    completion_date=date(2024, 2, 28),
                    image='images/exteriors/kavitha_elevation_3.png',
                    youtube_url='https://youtu.be/pQo_NwYYL4Y?si=HOruPJfat-YzSnjp',
                    status='active',
                    display_order=1
                ),
                Project(
                    title='Modern Commercial Elevation',
                    short_description='A state-of-the-art multi-storey commercial complex built for premium business and retail suites.',
                    description='Featuring a sharp glass facade, column-free floor plans, and a custom steel-reinforced structure, this commercial building in Mettupalayam represents modern civil construction at its finest. Equipped with multi-car basement parking and modular retail divisions.',
                    category='current',
                    client='Magesh Builders',
                    location='Mettupalayam, Tiruppur',
                    area_sqft='18,500 sq.ft',
                    floors='G+4',
                    project_type='Commercial Complex',
                    start_date=date(2024, 3, 1),
                    completion_date=date(2025, 8, 31),
                    image='images/exteriors/ansath_building_elevation.jpg',
                    youtube_url='https://youtu.be/pQo_NwYYL4Y?si=HOruPJfat-YzSnjp',
                    status='active',
                    display_order=2
                ),
                Project(
                    title='Uthukuli Modern Home',
                    short_description='Vibrant minimalist residential structure built in Uthukuli using natural stones and bricks.',
                    description='A beautiful single-family residence designed around traditional Vaastu principles. Built with premium reinforced cement concrete and adorned with natural slate stone highlights, this completed home boasts a premium modular kitchen and smart automation systems.',
                    category='completed',
                    client='Mr. Ponnusamy',
                    location='Uthukuli, Tamil Nadu',
                    area_sqft='2,400 sq.ft',
                    floors='G+1',
                    project_type='Residential Villa',
                    start_date=date(2022, 6, 1),
                    completion_date=date(2023, 5, 15),
                    image='images/exteriors/ponnusamy_uthukuli_elevation_1.1.jpg',
                    youtube_url='https://youtu.be/pQo_NwYYL4Y?si=HOruPJfat-YzSnjp',
                    status='active',
                    display_order=3
                ),
                Project(
                    title='Coimbatore Premium Elevation',
                    short_description='High-end duplex elevation design with cantilever balconies and textured concrete walls.',
                    description='A contemporary masterpiece under construction in Coimbatore. The project features unique geometric structures, wooden facade panels, and an open deck terrace. Designed to offer a premium luxury living experience for the client.',
                    category='current',
                    client='Mr. Venkatesan',
                    location='Coimbatore, Tamil Nadu',
                    area_sqft='4,200 sq.ft',
                    floors='G+2',
                    project_type='Duplex Villa',
                    start_date=date(2024, 5, 10),
                    completion_date=date(2025, 9, 30),
                    image='images/exteriors/venkatesan_venkat_sir_final_elevations_f2.jpg',
                    youtube_url='https://youtu.be/pQo_NwYYL4Y?si=HOruPJfat-YzSnjp',
                    status='active',
                    display_order=4
                )
            ]
            
            for project in projects:
                db.session.add(project)
            db.session.flush()  # get IDs
            
            # Add gallery photos to the first project using local images
            if projects:
                gallery_images = [
                    'exteriors/kavitha_elevation_1.png',
                    'exteriors/kavitha_elevation_2.png',
                    'interiors/kavitha_liv_01.jpg',
                    'interiors/kavitha_kitchen_01.jpg',
                    'interiors/kavitha_dining_01.jpg',
                    'interiors/kavitha_pooja_01.jpg',
                ]
                for i, fname in enumerate(gallery_images):
                    photo = ProjectPhoto(
                        project_id=projects[0].id,
                        filename=fname.split('/')[-1],
                        file_path=f'images/{fname}',
                        caption=f'Project view {i+1}',
                        display_order=i+1
                    )
                    db.session.add(photo)
            
            print("Sample projects created.")
        else:
            print("Projects already exist.")
        
        # Check if sample services exist
        if db.session.query(Service).count() == 0:
            services = [
                Service(
                    title='Construction',
                    description='End-to-end residential and commercial building construction from foundation to completion.',
                    icon='home',
                    image='images/workersonsite.jpg',
                    status='active',
                    display_order=1
                ),
                Service(
                    title='Elevation Designing',
                    description='Modern 2D and 3D front elevations, architectural layouts, and premium structural styling.',
                    icon='layout',
                    image='images/exteriors/ansath_building_elevation.jpg',
                    status='active',
                    display_order=2
                ),
                Service(
                    title='Planning',
                    description='Custom floor layouts and architectural blueprints complying with modern and traditional Vaastu principles.',
                    icon='map',
                    image='images/1 architectural line drawing  blueprint style graphic.jpg',
                    status='active',
                    display_order=3
                ),
                Service(
                    title='Approval',
                    description='Fast planning approvals and building license arrangements from municipal corporations and government bodies.',
                    icon='file-check',
                    image='images/1 architectural line drawing  blueprint style graphic.jpg',
                    status='active',
                    display_order=4
                ),
                Service(
                    title='Interior Design',
                    description='Stunning modular kitchens, wooden panels, wardrobes, and high-end styling details.',
                    icon='palette',
                    image='images/interiors/kavitha_liv_01.jpg',
                    status='active',
                    display_order=5
                ),
                Service(
                    title='Bank Loan Assistance',
                    description='Seamless arrangements for bank loans with or without IT returns, and documentation processing.',
                    icon='credit-card',
                    image='images/costructed completed buildign.jpg',
                    status='active',
                    display_order=6
                )
            ]
            
            for service in services:
                db.session.add(service)
            
            print("Sample services created.")
        else:
            print("Services already exist.")
        
        # Check if sample testimonials exist
        if db.session.query(Testimonial).count() == 0:
            testimonials = [
                Testimonial(
                    client_name='Kavitha Arumugam',
                    company='Homeowner, Tiruppur',
                    quote='Alnitak Constructions built our dream villa with outstanding quality. Every step of the construction was transparent, and the final finishing is absolutely premium.',
                    rating=5,
                    featured=True,
                    status='active'
                ),
                Testimonial(
                    client_name='Sumathi R',
                    company='Homeowner, Tiruppur',
                    quote='From the modular kitchen layout to the final front elevation, they showed pure professionalism. The construction quality is top-notch, and they delivered exactly on time.',
                    rating=5,
                    featured=True,
                    status='active'
                ),
                Testimonial(
                    client_name='Barath K',
                    company='Homeowner, Ramanathapuram',
                    quote='We are extremely pleased with our new residence. The design utilizes ventilation, light, and Vaastu principles efficiently. A highly trusted builder.',
                    rating=5,
                    featured=True,
                    status='active'
                ),
                Testimonial(
                    client_name='Ponnusamy M',
                    company='Businessman, Uthukuli',
                    quote='Their elevation design and planning are outstanding. They assisted us in securing bank loans and approvals quickly without any hassle.',
                    rating=5,
                    featured=True,
                    status='active'
                )
            ]
            
            for testimonial in testimonials:
                db.session.add(testimonial)
            
            print("Sample testimonials created.")
        else:
            print("Testimonials already exist.")
        
        # Commit all changes
        db.session.commit()
        
        print("\nDatabase initialization completed successfully!")
        print("\nDefault Admin Credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nPlease change the admin password after first login.")


def reset_database():
    """
    Reset database by dropping all tables and recreating them
    WARNING: This will delete all existing data!
    """
    app = create_app('development')
    
    with app.app_context():
        db.drop_all()
        print("All tables dropped.")
        
        init_database()


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--reset':
        print("WARNING: This will delete all existing data!")
        confirm = input("Are you sure you want to reset the database? (yes/no): ")
        
        if confirm.lower() == 'yes':
            reset_database()
        else:
            print("Database reset cancelled.")
    else:
        init_database()
