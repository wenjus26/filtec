#!/usr/bin/env python
"""
FILTEC Polyplast — Production Database Seed Script
===================================================
Usage:
    # Locally (dev):
    python seed_db.py

    # In production via Docker:
    sudo docker compose exec web python seed_db.py

    # Force re-seed (wipes and re-creates everything):
    sudo docker compose exec web python seed_db.py --force

Flags:
    --force     Wipe all existing products and events before seeding.
    --products  Seed only products.
    --events    Seed only events.
    --check     Dry-run: check source images exist and print a report.
"""

import os
import sys
import shutil
import argparse
import django

# ─── Django Setup ────────────────────────────────────────────────────────────
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'filtec_site.settings')
django.setup()

from core.models import Product, Event, EventImage

# ─── Paths ────────────────────────────────────────────────────────────────────
STATIC_DIR  = os.path.join(base_dir, "static")
MEDIA_DIR   = os.path.join(base_dir, "media")

PRODUCTS_MEDIA  = os.path.join(MEDIA_DIR, "products")
EVENTS_MAIN     = os.path.join(MEDIA_DIR, "events", "main")
EVENTS_GALLERY  = os.path.join(MEDIA_DIR, "events", "gallery")

# ─── Colors / Helpers ─────────────────────────────────────────────────────────
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def ok(msg):    print(f"{GREEN}  ✔  {msg}{RESET}")
def warn(msg):  print(f"{YELLOW}  ⚠  {msg}{RESET}")
def err(msg):   print(f"{RED}  ✘  {msg}{RESET}")
def info(msg):  print(f"{CYAN}  →  {msg}{RESET}")
def title(msg): print(f"\n{BOLD}{msg}{RESET}")

def copy_image(src, dest_dir, filename):
    """Copy image from static to media. Returns relative media path or None."""
    dest = os.path.join(dest_dir, filename)
    if os.path.exists(src):
        shutil.copy(src, dest)
        return True
    else:
        warn(f"Source image not found: {src}")
        return False

# ─── Products Data ────────────────────────────────────────────────────────────
PRODUCTS = [
    {
        "name": "uPVC Piping",
        "category": "upvc",
        "description": (
            "Flexible, lightweight pipelines designed for water networks, municipal sewage, "
            "chemical transport, and sub-zero temperature environments. "
            "Resistant to stress cracking and soil shift."
        ),
        "src_img": os.path.join(STATIC_DIR, "images", "products", "upvc_pipes.webp"),
        "filename": "upvc_pipes.webp",
        "specs": (
            "IS 4984 compliant\n"
            "SDR 11, SDR 13.6, SDR 17, SDR 21\n"
            "Standard size: 20mm to 200mm"
        ),
    },
    {
        "name": "PVC Piping",
        "category": "pvc",
        "description": (
            "Rigid, highly cost-effective piping suitable for agricultural irrigation grids, "
            "pressure mains, potable water logistics, and building ventilation drainage setups. "
            "Excellent hydraulic flow capacity."
        ),
        "src_img": os.path.join(STATIC_DIR, "images", "products", "pvc_pipes.webp"),
        "filename": "pvc_pipes.webp",
        "specs": (
            "IS 4985 compliant\n"
            "Class 1 (0.25 MPa), Class 2 (0.4 MPa), Class 3 (0.6 MPa)\n"
            "Standard size: 40mm to 160mm"
        ),
    },
    {
        "name": "CPVC Piping",
        "category": "cpvc",
        "description": (
            "Co-polymer systems engineered for hot & cold water plumbing, industrial central "
            "heating layouts, and air conditioning pipes. Highly thermal stable and jointed "
            "through fusion welding."
        ),
        "src_img": os.path.join(STATIC_DIR, "images", "products", "cpvc_pipes.webp"),
        "filename": "cpvc_pipes.webp",
        "specs": (
            "IS 15801 compliant\n"
            "SDR 11 (PN 20), SDR 13.5 (PN 16)\n"
            "Standard size: 15mm to 50mm"
        ),
    },
    {
        "name": "Ball Valve & Fittings",
        "category": "fittings",
        "description": (
            "Precision-molded elbow bends, equal tees, reducers, coupler sockets, end caps, "
            "and heavy-duty control valves. Designed to guarantee full joint pressure rating continuity."
        ),
        "src_img": os.path.join(STATIC_DIR, "images", "products", "upvc_cvpc_valve.webp"),
        "filename": "upvc_cvpc_valve.webp",
        "specs": (
            "IS 7834 compliant\n"
            "Pressure rating: PN 16\n"
            "Standard size: 15mm to 100mm"
        ),
    },
    {
        "name": "SWR Piping",
        "category": "swr",
        "description": (
            "Robust grey pipes and fittings designed for efficient drainage and wastewater "
            "management in residential and commercial complexes."
        ),
        "src_img": os.path.join(STATIC_DIR, "images", "product_swr.webp"),
        "filename": "product_swr.webp",
        "specs": (
            "IS 13592 compliant\n"
            "Type A (Thin wall for ventilation), Type B (Thick wall for soil/waste)\n"
            "Standard size: 75mm and 110mm"
        ),
    },
]

# ─── Events Data ──────────────────────────────────────────────────────────────
EVENTS = [
    {
        "title": "Mega Plumber Meet 2026",
        "category": "plumber",
        "cover_src": os.path.join(STATIC_DIR, "images", "galerie", "plumber_1.webp"),
        "cover_dest_filename": "plumber_1.webp",
        "description": (
            "Our annual mega plumber training and support meet held at Bhubaneswar, "
            "bringing together 500+ pipeline and plumbing technicians from across the region."
        ),
        "rich_description": (
            '<p>Our Bhubaneswar plant hosted the annual mega plumber training and technical instruction workshop, '
            'bringing together over 500+ plumbing and pipeline technicians across Odisha and neighboring states.</p>'
            '<p><img src="/media/events/gallery/plumber_2.webp" alt="Plumber Training Workshop" '
            'style="max-width:100%; height:auto; border-radius:8px; margin:15px 0; border:1px solid #ddd;" /></p>'
            '<p>The session focused on high-performance CPVC joint fusion, leak-proof solvent application, '
            'and compliance standards with Bureau of Indian Standards (BIS) guidelines. '
            'Participants engaged in hands-on hydrostatic pressure tests and pipe stress simulations.</p>'
            '<p><img src="/media/events/gallery/plumber_3.webp" alt="Hydrostatic Pressure Testing" '
            'style="max-width:100%; height:auto; border-radius:8px; margin:15px 0; border:1px solid #ddd;" /></p>'
            '<p><img src="/media/events/gallery/plumber_4.webp" alt="Technicians at Workshop" '
            'style="max-width:100%; height:auto; border-radius:8px; margin:15px 0; border:1px solid #ddd;" /></p>'
            '<p>FILTEC Polyplast also introduced the new SWR drainage system range with live product demonstrations '
            'and provided installation kits to the top-performing technicians. This meet is part of our long-term '
            'commitment to improving regional plumbing skills and building B2B quality awareness.</p>'
        ),
        "gallery": [
            {"src": os.path.join(STATIC_DIR, "images", "galerie", f"plumber_{i}.webp"), "filename": f"plumber_{i}.webp"}
            for i in range(1, 9)
        ],
    },
    {
        "title": "FILTEC Dealer Meet 2026",
        "category": "dealer",
        "cover_src": os.path.join(STATIC_DIR, "images", "galerie", "dealer_1.webp"),
        "cover_dest_filename": "dealer_1.webp",
        "description": (
            "B2B dealer association and feedback meet for regional distributors, "
            "featuring product presentations, exclusive agreements, and factory floor tours."
        ),
        "rich_description": (
            '<p>FILTEC Polyplast hosted the national B2B Dealer and Regional Distributor Meet at Bhubaneswar, '
            'highlighting raw material supply agreements, new product specifications, and logistics upgrades.</p>'
            '<p><img src="/media/events/gallery/dealer_2.webp" alt="Dealer Business Summit" '
            'style="max-width:100%; height:auto; border-radius:8px; margin:15px 0; border:1px solid #ddd;" /></p>'
            '<p>Partners discussed exclusive regional dealership agreements, commercial margins, and wholesale '
            'supply line optimization. A factory floor tour demonstrated our German automated extrusion lines '
            'with a live BIS testing demonstration.</p>'
            '<p><img src="/media/events/gallery/dealer_3.webp" alt="Factory Floor Tour" '
            'style="max-width:100%; height:auto; border-radius:8px; margin:15px 0; border:1px solid #ddd;" /></p>'
            '<p><img src="/media/events/gallery/dealer_4.webp" alt="Awards Ceremony" '
            'style="max-width:100%; height:auto; border-radius:8px; margin:15px 0; border:1px solid #ddd;" /></p>'
            '<p>The event concluded with awards for top-performing regional distributors and a presentation of '
            'FILTEC\'s strategic plan for expanding leak-proof pipeline installations nationwide in 2026–2027.</p>'
        ),
        "gallery": [
            {"src": os.path.join(STATIC_DIR, "images", "galerie", f"dealer_{i}.webp"), "filename": f"dealer_{i}.webp"}
            for i in range(1, 9)
        ],
    },
]

# ─── Seed Functions ───────────────────────────────────────────────────────────
def create_media_dirs():
    title("📁  Creating media directories...")
    for d in [PRODUCTS_MEDIA, EVENTS_MAIN, EVENTS_GALLERY]:
        os.makedirs(d, exist_ok=True)
        ok(d)

def seed_products(force=False):
    title("🏭  Seeding Products...")
    if force:
        count = Product.objects.count()
        Product.objects.all().delete()
        warn(f"Deleted {count} existing product(s).")

    for p in PRODUCTS:
        copied = copy_image(p["src_img"], PRODUCTS_MEDIA, p["filename"])
        prod, created = Product.objects.get_or_create(
            name=p["name"],
            defaults={
                "category": p["category"],
                "description": p["description"],
                "image": f"products/{p['filename']}",
                "technical_specifications": p["specs"],
            }
        )
        if not created and copied:
            # Update image path in case it was missing
            prod.image = f"products/{p['filename']}"
            prod.save()
        status = "CREATED" if created else "SKIPPED (already exists)"
        ok(f"{prod.name} → {status}")

def seed_events(force=False):
    title("🎪  Seeding Events & Gallery Images...")
    if force:
        count = Event.objects.count()
        Event.objects.all().delete()
        warn(f"Deleted {count} existing event(s) and their gallery images.")

    for ev in EVENTS:
        # Copy cover image
        copy_image(ev["cover_src"], EVENTS_MAIN, ev["cover_dest_filename"])

        # Create event
        event, created = Event.objects.get_or_create(
            title=ev["title"],
            defaults={
                "category": ev["category"],
                "main_image": f"events/main/{ev['cover_dest_filename']}",
                "description": ev["description"],
                "rich_description": ev["rich_description"],
            }
        )
        status = "CREATED" if created else "SKIPPED (already exists)"
        ok(f"Event: {event.title} → {status}")

        # Seed gallery images
        img_count = 0
        for g in ev["gallery"]:
            copied = copy_image(g["src"], EVENTS_GALLERY, g["filename"])
            if copied:
                rel_path = f"events/gallery/{g['filename']}"
                if not EventImage.objects.filter(event=event, image=rel_path).exists():
                    EventImage.objects.create(event=event, image=rel_path)
                    img_count += 1
        info(f"  Gallery: {img_count} new image(s) linked to '{event.title}'")

def check_sources():
    title("🔍  Dry-run: Checking source image files...")
    missing = 0

    for p in PRODUCTS:
        exists = os.path.exists(p["src_img"])
        if exists:
            ok(f"[PRODUCT] {p['name']} → {p['src_img']}")
        else:
            err(f"[PRODUCT] {p['name']} → MISSING: {p['src_img']}")
            missing += 1

    for ev in EVENTS:
        exists = os.path.exists(ev["cover_src"])
        if exists:
            ok(f"[EVENT COVER] {ev['title']} → {ev['cover_src']}")
        else:
            err(f"[EVENT COVER] {ev['title']} → MISSING: {ev['cover_src']}")
            missing += 1
        for g in ev["gallery"]:
            gexists = os.path.exists(g["src"])
            if gexists:
                ok(f"  [GALLERY] {g['filename']}")
            else:
                err(f"  [GALLERY] MISSING: {g['src']}")
                missing += 1

    print()
    if missing == 0:
        ok(f"All source images verified. Ready to seed.")
    else:
        err(f"{missing} missing source image(s) found. Fix them before seeding.")
    return missing

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="FILTEC Polyplast Production Database Seeder")
    parser.add_argument("--force",    action="store_true", help="Wipe and re-seed all data.")
    parser.add_argument("--products", action="store_true", help="Seed only products.")
    parser.add_argument("--events",   action="store_true", help="Seed only events.")
    parser.add_argument("--check",    action="store_true", help="Dry-run: verify source images exist.")
    args = parser.parse_args()

    print(f"\n{BOLD}{'='*55}{RESET}")
    print(f"{BOLD}  FILTEC Polyplast — Production Database Seeder{RESET}")
    print(f"{BOLD}{'='*55}{RESET}")

    if args.check:
        missing = check_sources()
        sys.exit(1 if missing > 0 else 0)

    create_media_dirs()

    seed_all = not args.products and not args.events

    if args.products or seed_all:
        seed_products(force=args.force)

    if args.events or seed_all:
        seed_events(force=args.force)

    title("✅  Seeding complete!")
    print(f"\n  Products in DB : {Product.objects.count()}")
    print(f"  Events   in DB : {Event.objects.count()}")
    print(f"  Gallery  in DB : {EventImage.objects.count()}\n")

if __name__ == "__main__":
    main()
