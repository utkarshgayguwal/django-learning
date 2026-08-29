from django.core.management.base import BaseCommand
from app.models import Service, Testimonial


class Command(BaseCommand):
    help = "Seed the database with initial dummy data (Service, Testimonial entries)"

    def handle(self, *args, **options):
        self.seed_services()
        self.seed_testimonials()

    def seed_services(self):
        services = [
            {
                "icon": "bi bi-activity",
                "title": "Digital Marketing Mastery",
                "description": (
                    "Elevate your online presence with our comprehensive digital "
                    "marketing solutions."
                ),
            },
            {
                "icon": "bi bi-broadcast",
                "title": "Public Relations Powerhouse",
                "description": (
                    "Shape your narrative and build strong relationships with our "
                    "public relations expertise. From crafting compelling press "
                    "releases to managing crisis communications, we help you "
                    "maintain a positive public image."
                ),
            },
            {
                "icon": "bi bi-easel",
                "title": "Creative Design Solutions",
                "description": (
                    "Unleash the potential of visually stunning design. Our "
                    "creative team specializes in crafting compelling graphics, "
                    "logos, and branding materials that captivate your audience."
                ),
            },
            {
                "icon": "bi bi-bounding-box-circles",
                "title": "Web Development Wizardry",
                "description": (
                    "Transform your digital footprint with our expert web "
                    "development services. Whether you need a responsive website, "
                    "e-commerce platform, or custom web application."
                ),
            },
            {
                "icon": "bi bi-calendar4-week",
                "title": "Data Analytics Excellence",
                "description": (
                    "Unlock the power of data with our advanced analytics "
                    "services. From gathering valuable insights to making "
                    "data-driven decisions, our analytics team is equipped to "
                    "turn raw data into actionable intelligence."
                ),
            },
            {
                "icon": "bi bi-chat-square-text",
                "title": "Strategic Consultancy Services",
                "description": (
                    "Navigate the complexities of business with our strategic "
                    "consultancy services. We offer tailored solutions to "
                    "optimize your operations, enhance efficiency, and fuel "
                    "sustainable growth."
                ),
            },
        ]

        created_count = 0
        for data in services:
            _, created = Service.objects.get_or_create(
                title=data["title"], defaults=data
            )
            created_count += created

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeding complete: {created_count} Service row(s) created, "
                f"{len(services) - created_count} already existed."
            )
        )

    def seed_testimonials(self):
        testimonials = [
            {
                "user_image": "assets/img/testimonials/testimonials-1.jpg",
                "username": "Saul Goodman",
                "user_job_title": "Ceo & Founder",
                "rating_count": 5,
                "review": (
                    "Working with [Your Agency Name] was a game-changer for our "
                    "business. Their team's strategic approach and attention to "
                    "detail significantly boosted our online presence. They're not "
                    "just an agency; they're a partner dedicated to our success."
                ),
            },
            {
                "user_image": "assets/img/testimonials/testimonials-4.jpg",
                "username": "Adam",
                "user_job_title": "Designer",
                "rating_count": 5,
                "review": (
                    "Incredible results, exceptional service! [Your Agency Name] "
                    "delivered beyond our expectations. Their creativity and "
                    "expertise transformed our marketing strategy, resulting in "
                    "increased leads and revenue. Highly recommended."
                ),
            },
            {
                "user_image": "assets/img/testimonials/testimonials-2.jpg",
                "username": "Sarah Johnson",
                "user_job_title": "Marketing Director",
                "rating_count": 5,
                "review": (
                    "[Your Agency Name] completely transformed how we approach "
                    "marketing. Their data-driven strategies and clear reporting "
                    "gave us the confidence to scale campaigns we'd been "
                    "hesitant to try before. The results speak for themselves."
                ),
            },
            {
                "user_image": "assets/img/testimonials/testimonials-3.jpg",
                "username": "Michael Chen",
                "user_job_title": "Product Manager",
                "rating_count": 4,
                "review": (
                    "Professional, responsive, and genuinely invested in our "
                    "success. [Your Agency Name] took the time to understand our "
                    "product before proposing solutions, which made all the "
                    "difference in how well the final work fit our needs."
                ),
            },
            {
                "user_image": "assets/img/testimonials/testimonials-5.jpg",
                "username": "Emily Rodriguez",
                "user_job_title": "Small Business Owner",
                "rating_count": 5,
                "review": (
                    "As a small business, we needed a partner who could work "
                    "within our budget without cutting corners. [Your Agency "
                    "Name] delivered exactly that, and our online presence has "
                    "never looked better."
                ),
            },
        ]

        created_count = 0
        for data in testimonials:
            _, created = Testimonial.objects.get_or_create(
                username=data["username"], defaults=data
            )
            created_count += created

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeding complete: {created_count} Testimonial row(s) created, "
                f"{len(testimonials) - created_count} already existed."
            )
        )
