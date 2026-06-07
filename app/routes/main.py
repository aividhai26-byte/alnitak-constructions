"""
Main public routes for Thendral City Developers Website
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from app import db
from app.models import Project, Service, Testimonial, ContactMessage
from app.models.job_application import JobApplication
from datetime import datetime
import os

main_bp = Blueprint('main', __name__)

STATIC_PROJECTS = [
    {
        'id': 1,
        'title': 'Tiruppur Residential Villa',
        'short_description': 'Premium contemporary villa featuring double height ceilings and customized styling details.',
        'description': 'A landmark residential villa featuring a sleek double-height foyer, premium granite finishes, and highly efficient architectural design. Crafted for maximum ventilation and light, this home sits in the heart of Tiruppur and has been completed to the absolute highest quality standards.',
        'category': 'completed',
        'client': 'Mrs. Kavitha Arumugam',
        'location': 'Tiruppur, Tamil Nadu',
        'area_sqft': '3,200 sq.ft',
        'floors': 'G+2',
        'project_type': 'Residential Villa',
        'image': 'images/exteriors/kavitha_elevation_3.png',
        'photos': [
            {'file_path': 'images/exteriors/kavitha_elevation_1.png', 'caption': 'Front Elevation View'},
            {'file_path': 'images/exteriors/kavitha_elevation_2.png', 'caption': 'Side Elevation View'},
            {'file_path': 'images/interiors/kavitha_liv_01.jpg', 'caption': 'Living Area Decor'},
            {'file_path': 'images/interiors/kavitha_kitchen_01.jpg', 'caption': 'Modular Kitchen Design'},
            {'file_path': 'images/interiors/kavitha_dining_01.jpg', 'caption': 'Dining Space'},
            {'file_path': 'images/interiors/kavitha_pooja_01.jpg', 'caption': 'Pooja Room Layout'}
        ]
    },
    {
        'id': 2,
        'title': 'Modern Commercial Elevation',
        'short_description': 'A state-of-the-art multi-storey commercial complex built for premium business and retail suites.',
        'description': 'Featuring a sharp glass facade, column-free floor plans, and a custom steel-reinforced structure, this commercial building in Mettupalayam represents modern civil construction at its finest. Equipped with multi-car basement parking and modular retail divisions.',
        'category': 'current',
        'client': 'Magesh Builders',
        'location': 'Mettupalayam, Tiruppur',
        'area_sqft': '18,500 sq.ft',
        'floors': 'G+4',
        'project_type': 'Commercial Complex',
        'image': 'images/exteriors/ansath_building_elevation.jpg',
        'photos': [
            {'file_path': 'images/exteriors/ansath_an_3.jpg', 'caption': 'Commercial Exterior Perspective'},
            {'file_path': 'images/exteriors/ansath_an_4.jpg', 'caption': 'Structure Framing Detail'}
        ]
    },
    {
        'id': 3,
        'title': 'Uthukuli Modern Home',
        'short_description': 'Vibrant minimalist residential structure built in Uthukuli using natural stones and bricks.',
        'description': 'A beautiful single-family residence designed around traditional Vaastu principles. Built with premium reinforced cement concrete and adorned with natural slate stone highlights, this completed home boasts a premium modular kitchen and smart automation systems.',
        'category': 'completed',
        'client': 'Mr. Ponnusamy',
        'location': 'Uthukuli, Tamil Nadu',
        'area_sqft': '2,400 sq.ft',
        'floors': 'G+1',
        'project_type': 'Residential Villa',
        'image': 'images/exteriors/ponnusamy_uthukuli_elevation_1.1.jpg',
        'photos': [
            {'file_path': 'images/exteriors/ponnusamy_uthukuli_elevation_1.2.jpg', 'caption': 'Elevation Night View'}
        ]
    },
    {
        'id': 4,
        'title': 'Coimbatore Premium Elevation',
        'short_description': 'High-end duplex elevation design with cantilever balconies and textured concrete walls.',
        'description': 'A contemporary masterpiece under construction in Coimbatore. The project features unique geometric structures, wooden facade panels, and an open deck terrace. Designed to offer a premium luxury living experience for the client.',
        'category': 'current',
        'client': 'Mr. Venkatesan',
        'location': 'Coimbatore, Tamil Nadu',
        'area_sqft': '4,200 sq.ft',
        'floors': 'G+2',
        'project_type': 'Duplex Villa',
        'image': 'images/exteriors/venkatesan_venkat_sir_final_elevations_f2.jpg',
        'photos': [
            {'file_path': 'images/exteriors/venkatesan_venkat_sir_final_elevations_f1.jpg', 'caption': 'Duplex Elevation Side perspective'},
            {'file_path': 'images/exteriors/venkatesan_venkat_sir_final_elevations_f3.jpg', 'caption': 'Geometric concrete facade details'}
        ]
    }
]


@main_bp.route('/')
def index():
    """
    Home page route
    """
    projects_list = []
    try:
        projects_list = db.session.query(Project).filter_by(
            status='active'
        ).order_by(Project.display_order.asc()).limit(6).all()
    except Exception:
        pass
        
    if not projects_list:
        projects_list = STATIC_PROJECTS[:6]
        
    return render_template('index.html', projects=projects_list)


@main_bp.route('/about')
def about():
    """
    About Us page route
    """
    return render_template('about.html')


@main_bp.route('/process')
def process_page():
    """
    Process page route
    """
    return render_template('process.html')


@main_bp.route('/pricing')
def pricing():
    """
    Pricing page route
    """
    return render_template('pricing.html')


@main_bp.route('/faq')
def faq():
    """
    FAQ page route
    """
    return render_template('faq.html')


@main_bp.route('/promotings')
def promotings():
    """
    Promotings page route
    
    Returns:
        Rendered promotings.html template
    """
    return render_template('promotings.html')


@main_bp.route('/quality')
def quality():
    """
    Quality page route
    
    Returns:
        Rendered quality.html template
    """
    return render_template('quality.html')


@main_bp.route('/nri')
def nri():
    """
    NRI page route
    
    Returns:
        Rendered nri.html template
    """
    return render_template('nri.html')


@main_bp.route('/residential')
def residential():
    """
    Residential page route
    
    Returns:
        Rendered residential.html template
    """
    return render_template('residential.html')


@main_bp.route('/careers')
def careers():
    """
    Careers page route
    
    Returns:
        Rendered careers.html template
    """
    return render_template('careers.html')


@main_bp.route('/careers/apply', methods=['POST'])
def careers_apply():
    """
    Process career application form with resume upload
    """
    try:
        from flask import current_app
        from werkzeug.utils import secure_filename

        first_name = request.form.get('first_name', '').strip()
        last_name  = request.form.get('last_name', '').strip()
        email      = request.form.get('email', '').strip()
        phone      = request.form.get('phone', '').strip()
        role       = request.form.get('role', '').strip()
        cover      = request.form.get('cover_letter', '').strip()

        resume_filename = None
        resume_path     = None

        if 'resume' in request.files:
            file = request.files['resume']
            if file and file.filename:
                allowed = {'pdf', 'doc', 'docx'}
                ext = file.filename.rsplit('.', 1)[-1].lower()
                if ext in allowed:
                    fname = secure_filename(file.filename)
                    upload_dir = os.path.join(current_app.static_folder, 'uploads', 'resumes')
                    os.makedirs(upload_dir, exist_ok=True)
                    file.save(os.path.join(upload_dir, fname))
                    resume_filename = fname
                    resume_path     = f'uploads/resumes/{fname}'

        application = JobApplication(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            role=role,
            cover_letter=cover,
            resume_filename=resume_filename,
            resume_path=resume_path
        )
        db.session.add(application)
        db.session.commit()

        flash('Application submitted successfully! Our HR team will contact you shortly.', 'success')
        return redirect(url_for('main.careers'))

    except Exception as e:
        db.session.rollback()
        print(f'Career apply error: {e}')
        flash('There was an error submitting your application. Please try again.', 'danger')
        return redirect(url_for('main.careers'))


@main_bp.route('/services')
def services():
    """
    Services page route
    
    Returns:
        Rendered services.html template
    """
    return render_template('services.html')


@main_bp.route('/projects')
def projects():
    """
    Projects page route
    """
    category = request.args.get('category')
    if category == 'ongoing':
        category = 'current'
    
    projects_list = []
    try:
        if category in ['current', 'completed']:
            projects_list = db.session.query(Project).filter_by(
                category=category,
                status='active'
            ).order_by(Project.display_order.asc()).all()
        else:
            projects_list = db.session.query(Project).filter_by(
                status='active'
            ).order_by(Project.display_order.asc()).all()
    except Exception:
        pass
    
    if not projects_list:
        if category == 'current':
            projects_list = [p for p in STATIC_PROJECTS if p['category'] == 'current']
        elif category == 'completed':
            projects_list = [p for p in STATIC_PROJECTS if p['category'] == 'completed']
        else:
            projects_list = STATIC_PROJECTS
            
    return render_template('projects.html', projects=projects_list, active_tab=category or 'all')


@main_bp.route('/projects/<int:project_id>')
def project_detail(project_id):
    """
    Single project detail page with gallery and YouTube embed
    """
    project = None
    photos = []
    related = []
    
    try:
        from app.models.project import ProjectPhoto
        project = db.session.query(Project).filter_by(id=project_id, status='active').first()
        if project:
            photos = db.session.query(ProjectPhoto).filter_by(project_id=project_id).order_by(ProjectPhoto.display_order).all()
            related = db.session.query(Project).filter(
                Project.category == project.category,
                Project.status == 'active',
                Project.id != project_id
            ).limit(3).all()
    except Exception:
        pass
        
    if not project:
        # Find in static projects fallback
        static_p = next((p for p in STATIC_PROJECTS if p['id'] == project_id), None)
        if not static_p:
            from flask import abort
            abort(404)
        project = static_p
        photos = static_p.get('photos', [])
        # Similar projects from static projects
        related = [p for p in STATIC_PROJECTS if p['category'] == static_p['category'] and p['id'] != project_id][:3]
        
    return render_template('project_detail.html', project=project, photos=photos, related=related)


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Contact page route
    """
    if request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'error': 'No data provided'}), 400
                
            from app.utils.validators import sanitize_string
            
            # Create new contact message with sanitized input
            message = ContactMessage(
                name=sanitize_string(data.get('name'), 100),
                email=sanitize_string(data.get('email'), 100),
                phone=sanitize_string(data.get('phone'), 20),
                subject=sanitize_string(data.get('subject'), 200),
                message=sanitize_string(data.get('message'), 2000),
                is_read=False,
                is_responded=False
            )
            
            db.session.add(message)
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Message sent successfully'}), 200
            
        except Exception as e:
            db.session.rollback()
            # Log the error but don't leak details to the client
            print(f"Contact form error: {e}") 
            return jsonify({'success': False, 'error': 'An internal error occurred. Please try again later.'}), 500
    
    return render_template('contact.html')


@main_bp.route('/robots.txt')
def robots():
    """
    Serve robots.txt for SEO and security
    """
    content = "User-agent: *\nDisallow: /admin/\nDisallow: /api/\nSitemap: " + request.url_root + "sitemap.xml"
    return content, 200, {'Content-Type': 'text/plain'}


@main_bp.route('/sitemap.xml')
def sitemap():
    """
    Generate dynamic sitemap for Google indexing
    """
    pages = []
    # Static pages
    for rule in [
        'main.index', 'main.projects', 'main.services', 'main.promotings', 
        'main.quality', 'main.nri', 'main.residential', 'main.careers', 'main.contact'
    ]:
        pages.append({
            'loc': url_for(rule, _external=True),
            'lastmod': datetime.now().strftime('%Y-%m-%d')
        })
    
    # Dynamic projects
    projects_list = db.session.query(Project).filter_by(status='active').all()
    for p in projects_list:
        pages.append({
            'loc': url_for('main.project_detail', project_id=p.id, _external=True),
            'lastmod': datetime.now().strftime('%Y-%m-%d')
        })
        
    sitemap_xml = render_template('sitemap.xml', pages=pages)
    return sitemap_xml, 200, {'Content-Type': 'application/xml'}




@main_bp.route('/api/projects')
def api_projects():
    """
    API endpoint to get projects
    
    Args:
        category: Optional category filter (current/completed)
    
    Returns:
        JSON response with projects data
    """
    category = request.args.get('category')
    
    if category in ['current', 'completed']:
        projects_list = db.session.query(Project).filter_by(
            category=category,
            status='active'
        ).order_by(Project.display_order.asc()).all()
    else:
        projects_list = db.session.query(Project).filter_by(
            status='active'
        ).order_by(Project.display_order.asc()).all()
    
    return jsonify({
        'success': True,
        'projects': [project.to_dict() for project in projects_list]
    })


@main_bp.route('/api/services')
def api_services():
    """
    API endpoint to get services
    
    Returns:
        JSON response with services data
    """
    services_list = db.session.query(Service).filter_by(
        status='active'
    ).order_by(Service.display_order.asc()).all()
    
    return jsonify({
        'success': True,
        'services': [service.to_dict() for service in services_list]
    })


@main_bp.route('/api/testimonials')
def api_testimonials():
    """
    API endpoint to get testimonials
    
    Returns:
        JSON response with testimonials data
    """
    testimonials_list = db.session.query(Testimonial).filter_by(
        status='active',
        featured=True
    ).all()
    
    return jsonify({
        'success': True,
        'testimonials': [testimonial.to_dict() for testimonial in testimonials_list]
    })
