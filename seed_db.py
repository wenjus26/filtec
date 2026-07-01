import os
import sys
import shutil
import django

# Dynamically set base directory
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.append(base_dir)

# Setup Django configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'filtec_site.settings')
django.setup()

from core.models import Product, Event, EventImage

def seed_database():
    static_dir = os.path.join(base_dir, "static")
    media_dir = os.path.join(base_dir, "media")
    
    # 1. Create media directories
    products_media_dir = os.path.join(media_dir, "products")
    events_main_media_dir = os.path.join(media_dir, "events", "main")
    events_gal_media_dir = os.path.join(media_dir, "events", "gallery")
    
    os.makedirs(products_media_dir, exist_ok=True)
    os.makedirs(events_main_media_dir, exist_ok=True)
    os.makedirs(events_gal_media_dir, exist_ok=True)
    
    print("Created media directories.")
    
    # Purge existing database entries to force a fresh seed with updated rich content
    Product.objects.all().delete()
    Event.objects.all().delete()
    print("Purged old database entries for clean seeding.")
    
    # 2. Seed Products
    products_data = [
        {
            'name': 'uPVC Piping',
            'category': 'upvc',
            'description': 'Flexible, lightweight pipelines designed for water networks, municipal sewage, chemical transport, and sub-zero temperature environments. Resistant to stress cracking and soil shift.',
            'src_img': os.path.join(static_dir, "images", "products", "upvc_pipes.webp"),
            'dest_filename': 'upvc_pipes.webp',
            'specs': 'IS 4984 compliant\nSDR 11, SDR 13.6, SDR 17, SDR 21\nStandard size: 20mm to 200mm'
        },
        {
            'name': 'PVC Piping',
            'category': 'pvc',
            'description': 'Rigid, highly cost-effective piping suitable for agricultural irrigation grids, pressure mains, potable water logistics, and building ventilation drainage setups. Excellent hydraulic flow capacity.',
            'src_img': os.path.join(static_dir, "images", "products", "pvc_pipes.webp"),
            'dest_filename': 'pvc_pipes.webp',
            'specs': 'IS 4985 compliant\nClass 1 (0.25 MPa), Class 2 (0.4 MPa), Class 3 (0.6 MPa)\nStandard size: 40mm to 160mm'
        },
        {
            'name': 'CPVC Piping',
            'category': 'cpvc',
            'description': 'Co-polymer systems engineered for hot & cold water plumbing, industrial central heating layouts, and air conditioning pipes. Highly thermal stable and jointed through fusion welding.',
            'src_img': os.path.join(static_dir, "images", "products", "cpvc_pipes.webp"),
            'dest_filename': 'cpvc_pipes.webp',
            'specs': 'IS 15801 compliant\nSDR 11 (PN 20), SDR 13.5 (PN 16)\nStandard size: 15mm to 50mm'
        },
        {
            'name': 'Ball Valve',
            'category': 'fittings',
            'description': 'Precision-molded elbow bends, equal tees, reducers, coupler sockets, end caps, and heavy-duty control valves. Designed to guarantee full joint pressure rating continuity.',
            'src_img': os.path.join(static_dir, "images", "products", "upvc_cvpc_valve.webp"),
            'dest_filename': 'upvc_cvpc_valve.webp',
            'specs': 'IS 7834 compliant\nPressure rating: PN 16\nStandard size: 15mm to 100mm'
        },
        {
            'name': 'SWR Piping',
            'category': 'swr',
            'description': 'Robust grey pipes and fittings designed for efficient drainage and wastewater management in residential and commercial complexes.',
            'src_img': os.path.join(static_dir, "images", "product_swr.webp"),
            'dest_filename': 'product_swr.webp',
            'specs': 'IS 13592 compliant\nType A (Thin wall for ventilation), Type B (Thick wall for soil/waste)\nStandard size: 75mm and 110mm'
        }
    ]
    
    for p in products_data:
        # Copy image file
        dest_img_path = os.path.join(products_media_dir, p['dest_filename'])
        if os.path.exists(p['src_img']):
            shutil.copy(p['src_img'], dest_img_path)
            
        # Create Product
        prod, created = Product.objects.get_or_create(
            name=p['name'],
            defaults={
                'category': p['category'],
                'description': p['description'],
                'image': f"products/{p['dest_filename']}",
                'technical_specifications': p['specs']
            }
        )
        print(f"Product '{prod.name}' seeded (created={created}).")
        
    # 3. Seed Events
    # Event 1: Mega Plumber Meet
    plumber_cover_src = os.path.join(static_dir, "images", "galerie", "plumber_1.webp")
    plumber_cover_dest = os.path.join(events_main_media_dir, "plumber_1.webp")
    if os.path.exists(plumber_cover_src):
        shutil.copy(plumber_cover_src, plumber_cover_dest)
        
    plumber_event, created = Event.objects.get_or_create(
        title="Mega Plumber Meet 2026",
        defaults={
            'category': 'plumber',
            'main_image': 'events/main/plumber_1.webp',
            'description': 'Our annual mega plumber training and support meet held at Bhubaneswar.',
            'rich_description': (
                '<p>Our Bhubaneswar plant hosted the annual mega plumber training and technical instruction workshop, '
                'bringing together over 500+ plumbing and pipeline technicians across the region.</p>'
                '<p><img src="/media/events/gallery/plumber_2.webp" alt="Plumber Training Workshop" style="max-width:100%; height:auto; border-radius:8px; margin: 15px 0; border: 1px solid #ddd;" /></p>'
                '<p>The session focused on training for high-performance CPVC joint fusion, leak-proof solvent application, '
                'and compliance standards with BIS guidelines. Participants engaged in hands-on hydrostatic pressure tests.</p>'
                '<p><img src="/media/events/gallery/plumber_3.webp" alt="Hydrostatic Pressure Testing" style="max-width:100%; height:auto; border-radius:8px; margin: 15px 0; border: 1px solid #ddd;" /></p>'
                '<p>This meet is part of FILTEC Polyplast\'s long-term commitment to improving regional plumbing skills and building B2B quality awareness.</p>'
            )
        }
    )
    print(f"Event Plumber Meet seeded (created={created}).")
    
    # Event 2: Dealer Meet
    dealer_cover_src = os.path.join(static_dir, "images", "galerie", "dealer_1.webp")
    dealer_cover_dest = os.path.join(events_main_media_dir, "dealer_1.webp")
    if os.path.exists(dealer_cover_src):
        shutil.copy(dealer_cover_src, dealer_cover_dest)
        
    dealer_event, created = Event.objects.get_or_create(
        title="FILTEC Dealer Meet 2026",
        defaults={
            'category': 'dealer',
            'main_image': 'events/main/dealer_1.webp',
            'description': 'B2B dealer association and feedback meet for regional distributors.',
            'rich_description': (
                '<p>FILTEC Polyplast hosted the national B2B Dealer and Regional Distributor Meet at Bhubaneswar, '
                'highlighting raw material supply agreements, new product specifications, and logistics upgrades.</p>'
                '<p><img src="/media/events/gallery/dealer_2.webp" alt="Dealer Business Summit" style="max-width:100%; height:auto; border-radius:8px; margin: 15px 0; border: 1px solid #ddd;" /></p>'
                '<p>Partners discussed exclusive regional dealership agreements, commercial margins, and wholesale supply line optimization. '
                'A factory floor tour demonstrated our German automated extrusion lines.</p>'
                '<p><img src="/media/events/gallery/dealer_3.webp" alt="Factory Floor Tour" style="max-width:100%; height:auto; border-radius:8px; margin: 15px 0; border: 1px solid #ddd;" /></p>'
                '<p>The event concluded with awards for top-performing distributors and our strategic plan for building leak-proof pipeline installations nationwide.</p>'
            )
        }
    )
    print(f"Event Dealer Meet seeded (created={created}).")
    
    # 4. Seed Gallery Images
    # Plumber Images
    for i in range(1, 9):
        filename = f"plumber_{i}.webp"
        src_path = os.path.join(static_dir, "images", "galerie", filename)
        dest_path = os.path.join(events_gal_media_dir, filename)
        if os.path.exists(src_path):
            shutil.copy(src_path, dest_path)
            # Create EventImage
            img_rel_path = f"events/gallery/{filename}"
            # Check if already exists
            if not EventImage.objects.filter(event=plumber_event, image=img_rel_path).exists():
                EventImage.objects.create(
                    event=plumber_event,
                    image=img_rel_path
                )
                
    # Dealer Images
    for i in range(1, 9):
        filename = f"dealer_{i}.webp"
        src_path = os.path.join(static_dir, "images", "galerie", filename)
        dest_path = os.path.join(events_gal_media_dir, filename)
        if os.path.exists(src_path):
            shutil.copy(src_path, dest_path)
            # Create EventImage
            img_rel_path = f"events/gallery/{filename}"
            # Check if already exists
            if not EventImage.objects.filter(event=dealer_event, image=img_rel_path).exists():
                EventImage.objects.create(
                    event=dealer_event,
                    image=img_rel_path
                )
                
    print("All gallery images successfully seeded into media folders and database.")

if __name__ == "__main__":
    seed_database()
