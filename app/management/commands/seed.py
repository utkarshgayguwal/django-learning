from django.core.management.base import BaseCommand
from app.models import GeneralInfo, Service, Testimonial, FrequentlyAskedQuestion


class Command(BaseCommand):
    help = "Seed the database with initial dummy data (GeneralInfo, Service, Testimonial, FrequentlyAskedQuestion entries)"

    def handle(self, *args, **options):
        general_info = self.seed_general_info()
        self.seed_services()
        self.seed_testimonials(general_info.company_name)
        self.seed_faqs(general_info.company_name)

    def seed_general_info(self):
        general_info, created = GeneralInfo.objects.get_or_create(
            id=1,
            defaults={
                "company_name": "ImpactAz",
                "location": "A108 Adam Street, New York, NY 535022",
                "email": "info@example.com",
                "phone": "+1 5589 55488 55",
                "open_hours": "Mon-Sat: 11AM - 23PM",
                "video_url": "https://www.youtube.com/watch?v=LXb3EKWsInQ",
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Seeding complete: GeneralInfo row created."
                if created
                else "Seeding complete: GeneralInfo row already existed, left untouched."
            )
        )
        return general_info

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

    def seed_testimonials(self, company_name):
        testimonials = [
            {
                "user_image": "assets/img/testimonials/testimonials-1.jpg",
                "username": "Saul Goodman",
                "user_job_title": "Ceo & Founder",
                "rating_count": 5,
                "review": (
                    f"Working with {company_name} was a game-changer for our "
                    "business. Their team's strategic approach and attention to "
                    "detail significantly boosted our online presence. They're not "
                    "just an agency; they're a partner dedicated to our success."
                ),
            },
            {
                "user_image": "assets/img/testimonials/testimonials-4.jpg",
                "username": "Adam",
                "user_job_title": "Designer",
                "rating_count": 4,
                "review": (
                    f"Incredible results, exceptional service! {company_name} "
                    "delivered beyond our expectations. Their creativity and "
                    "expertise transformed our marketing strategy, resulting in "
                    "increased leads and revenue. Highly recommended."
                ),
            },
            {
                "user_image": "assets/img/testimonials/testimonials-2.jpg",
                "username": "Sarah Johnson",
                "user_job_title": "Marketing Director",
                "rating_count": 3,
                "review": (
                    f"{company_name} completely transformed how we approach "
                    "marketing. Their data-driven strategies and clear reporting "
                    "gave us the confidence to scale campaigns we'd been "
                    "hesitant to try before. The results speak for themselves."
                ),
            },
            {
                "user_image": "assets/img/testimonials/testimonials-3.jpg",
                "username": "Michael Chen",
                "user_job_title": "Product Manager",
                "rating_count": 2,
                "review": (
                    "Professional, responsive, and genuinely invested in our "
                    f"success. {company_name} took the time to understand our "
                    "product before proposing solutions, which made all the "
                    "difference in how well the final work fit our needs."
                ),
            },
            {
                "user_image": "assets/img/testimonials/testimonials-5.jpg",
                "username": "Emily Rodriguez",
                "user_job_title": "Small Business Owner",
                "rating_count": 1,
                "review": (
                    "As a small business, we needed a partner who could work "
                    f"within our budget without cutting corners. {company_name} "
                    "delivered exactly that, and our online presence has "
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

    def seed_faqs(self, company_name):
        faqs = [
            {
                "question": "What services does your agency provide?",
                "answer": (
                    "Our agency offers a range of services, including [brief "
                    "description of services]. Whether you need [specific service] "
                    "or [another service], we have the expertise to meet your "
                    "needs."
                ),
            },
            {
                "question": "How can I contact your agency for assistance?",
                "answer": (
                    "You can reach us through our Contact Us page on the website, "
                    "where you'll find our phone number and email address. "
                    "Additionally, we welcome you to visit our office during "
                    "business hours for face-to-face assistance."
                ),
            },
            {
                "question": "What sets your agency apart from others in the industry?",
                "answer": (
                    f"At {company_name}, we pride ourselves on [highlight unique "
                    "aspects such as expertise, customer service, or innovative "
                    "solutions]. Our commitment to [core values] distinguishes us, "
                    "ensuring that we deliver exceptional results for our clients."
                ),
            },
            {
                "question": "How does the billing process work?",
                "answer": (
                    "Our billing process is straightforward. Once we've provided "
                    "you with a detailed proposal and you've accepted it, we will "
                    "send you an invoice for the agreed-upon services. Our billing "
                    "terms are [mention payment terms], and we accept payments "
                    "through [list payment methods]."
                ),
            },
            {
                "question": "Can I see examples of your agency's previous work?",
                "answer": (
                    "Absolutely! We showcase a portfolio of our work on our "
                    "website under the \"Projects\" or \"Portfolio\" section. "
                    "There, you can explore a variety of projects we've "
                    "successfully completed, giving you a sense of the quality "
                    "and diversity of our work."
                ),
            },
        ]

        created_count = 0
        for data in faqs:
            _, created = FrequentlyAskedQuestion.objects.get_or_create(
                question=data["question"], defaults=data
            )
            created_count += created

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeding complete: {created_count} FrequentlyAskedQuestion row(s) "
                f"created, {len(faqs) - created_count} already existed."
            )
        )
