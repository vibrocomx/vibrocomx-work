from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, current_user
import os
from models import db, User, Post, PageContent, SocialLink, SiteSetting, Founder
from admin_routes import admin_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vibrocomx-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vibrocomx.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'images')

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'admin.login'
login_manager.init_app(app)

from sqlalchemy import text
with app.app_context():
    db.create_all()
    try:
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE post ADD COLUMN is_published BOOLEAN DEFAULT 1;"))
            conn.commit()
    except Exception:
        pass # Column already exists or table issue
    try:
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE post ADD COLUMN views INTEGER DEFAULT 0;"))
            conn.commit()
    except Exception:
        pass # Column already exists or table issue

@app.before_request
def check_maintenance_mode():
    if request.path.startswith('/admin') or request.path.startswith('/static'):
        return
        
    maintenance_setting = SiteSetting.query.filter_by(setting_key='maintenance_mode').first()
    if maintenance_setting and maintenance_setting.setting_value == 'true':
        return render_template('maintenance.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_globals():
    social_links = SocialLink.query.all()
    
    banner_setting = SiteSetting.query.filter_by(setting_key='breaking_banner').first()
    show_banner = banner_setting.setting_value == 'true' if banner_setting else True
    
    breaking_text_setting = SiteSetting.query.filter_by(setting_key='breaking_text').first()
    breaking_text = breaking_text_setting.setting_value if breaking_text_setting else "Global South unites against sanctions"
    
    developing_text_setting = SiteSetting.query.filter_by(setting_key='developing_stories_text').first()
    developing_stories_text = developing_text_setting.setting_value if developing_text_setting else "Developing Stories"
    
    critical_text_setting = SiteSetting.query.filter_by(setting_key='critical_updates_text').first()
    critical_updates_text = critical_text_setting.setting_value if critical_text_setting else "Critical Updates"
    
    # Dynamic Text Elements
    hero_tagline_setting = SiteSetting.query.filter_by(setting_key='hero_tagline').first()
    hero_tagline = hero_tagline_setting.setting_value if hero_tagline_setting else "Truth Beyond the Noise"
    
    hero_subtext_setting = SiteSetting.query.filter_by(setting_key='hero_subtext').first()
    hero_subtext = hero_subtext_setting.setting_value if hero_subtext_setting else "Delivering objective, rigorous analysis on global security, politics, and economics. We cut through the noise to bring you unfiltered facts."

    mission_tagline_setting = SiteSetting.query.filter_by(setting_key='mission_tagline').first()
    mission_tagline = mission_tagline_setting.setting_value if mission_tagline_setting else "We dismantle narratives, decode global shifts, and deliver rigorous, unapologetic analysis on the forces shaping our world."

    featured_quote_setting = SiteSetting.query.filter_by(setting_key='featured_quote').first()
    featured_quote = featured_quote_setting.setting_value if featured_quote_setting else "Truth acts as a vibration through the noise. We bring our rigorous reporting directly to the platforms you use."
    
    quote_author_setting = SiteSetting.query.filter_by(setting_key='quote_author').first()
    quote_author = quote_author_setting.setting_value if quote_author_setting else "VibrocomX Editorial Board"

    # Using the provided link as the default fallback for YouTube
    youtube_embed_setting = SiteSetting.query.filter_by(setting_key='youtube_embed').first()
    youtube_embed = youtube_embed_setting.setting_value if youtube_embed_setting else "https://youtube.com/@vibrocomx?si=Jw6-Wy_Sr38VAKwc"

    # Using the provided link as the default fallback for Instagram
    instagram_embed_setting = SiteSetting.query.filter_by(setting_key='instagram_embed').first()
    instagram_embed = instagram_embed_setting.setting_value if instagram_embed_setting else "https://www.instagram.com/vibrocomx?igsh=MTdreGJnYnlhb2Vlbw=="

    # Using the provided link as the default fallback for LinkedIn
    linkedin_embed_setting = SiteSetting.query.filter_by(setting_key='linkedin_embed').first()
    linkedin_embed = linkedin_embed_setting.setting_value if linkedin_embed_setting else "https://www.linkedin.com/in/vibrocomx"

    site_logo_setting = SiteSetting.query.filter_by(setting_key='site_logo').first()
    site_logo = site_logo_setting.setting_value if site_logo_setting else url_for('static', filename='logo.png')
    
    homepage_layout_setting = SiteSetting.query.filter_by(setting_key='homepage_layout').first()
    homepage_layout = homepage_layout_setting.setting_value if homepage_layout_setting else "featured"
    
    maintenance_mode_setting = SiteSetting.query.filter_by(setting_key='maintenance_mode').first()
    maintenance_mode = maintenance_mode_setting.setting_value if maintenance_mode_setting else 'false'
    
    # Broadcast configuration
    show_broadcast_setting = SiteSetting.query.filter_by(setting_key='show_broadcast').first()
    show_broadcast = show_broadcast_setting.setting_value if show_broadcast_setting else 'true'
    
    broadcast_title_setting = SiteSetting.query.filter_by(setting_key='broadcast_title').first()
    broadcast_title = broadcast_title_setting.setting_value if broadcast_title_setting else 'Neo-Colonialism in the Digital Age'
    
    broadcast_subtitle_setting = SiteSetting.query.filter_by(setting_key='broadcast_subtitle').first()
    broadcast_subtitle = broadcast_subtitle_setting.setting_value if broadcast_subtitle_setting else 'with Dr. Ayesha Khan'
    
    broadcast_datetime_setting = SiteSetting.query.filter_by(setting_key='broadcast_datetime').first()
    broadcast_datetime = broadcast_datetime_setting.setting_value if broadcast_datetime_setting else '2026-10-15T14:30'
    
    broadcast_fallback_quote_setting = SiteSetting.query.filter_by(setting_key='broadcast_fallback_quote').first()
    broadcast_fallback_quote = broadcast_fallback_quote_setting.setting_value if broadcast_fallback_quote_setting else 'Technology must serve humanity, not subjugate it.'

    return dict(
        social_links=social_links, 
        show_banner=show_banner, 
        breaking_text=breaking_text,
        developing_stories_text=developing_stories_text,
        critical_updates_text=critical_updates_text,
        hero_tagline=hero_tagline,
        hero_subtext=hero_subtext,
        mission_tagline=mission_tagline,
        featured_quote=featured_quote,
        quote_author=quote_author,
        youtube_embed=youtube_embed,
        instagram_embed=instagram_embed,
        linkedin_embed=linkedin_embed,
        site_logo=site_logo,
        homepage_layout=homepage_layout,
        maintenance_mode=maintenance_mode,
        show_broadcast=show_broadcast,
        broadcast_title=broadcast_title,
        broadcast_subtitle=broadcast_subtitle,
        broadcast_datetime=broadcast_datetime,
        broadcast_fallback_quote=broadcast_fallback_quote
    )

@app.route('/')
def index():
    posts = Post.query.filter_by(is_published=True).order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/mission')
def mission():
    content = PageContent.query.filter_by(page_name='mission').first()
    founders = Founder.query.all()
    mission_text = content.content if content else "Mission content not set."
    return render_template('mission.html', mission_text=mission_text, founders=founders)

@app.route('/analysis')
def analysis():
    category = request.args.get('category')
    
    if category:
        # Filter by category, assuming category is stored with correct casing/matching logic
        posts = Post.query.filter(Post.category.ilike(category)).order_by(Post.date_posted.desc()).all()
        page_title = f"{category.capitalize()} Analysis"
    else:
        posts = Post.query.order_by(Post.date_posted.desc()).all()
        page_title = "Latest Analysis"
        
    return render_template('posts.html', posts=posts, title=page_title)

@app.route('/article/<slug>')
def article(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    if post.views is None:
        post.views = 0
    post.views += 1
    db.session.commit()
    return render_template('article.html', post=post)

# Register Blueprint
app.register_blueprint(admin_bp, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
