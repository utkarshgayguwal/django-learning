from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from app.models import GeneralInfo, Service, Testimonial, FrequentlyAskedQuestion, Blog, Author


class Command(BaseCommand):
    help = "Seed the database with initial dummy data (GeneralInfo, Service, Testimonial, FrequentlyAskedQuestion, Author, Blog entries)"

    def handle(self, *args, **options):
        general_info = self.seed_general_info()
        self.seed_services()
        self.seed_testimonials(general_info.company_name)
        self.seed_faqs(general_info.company_name)
        authors = self.seed_authors()
        self.seed_blogs(authors)

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

    def seed_authors(self):
        now = timezone.now()
        authors = [
            {
                "first_name": "Jane",
                "last_name": "Cooper",
                "country": "United States",
                "joined_at": now - timedelta(days=365 * 3),
            },
            {
                "first_name": "Marcus",
                "last_name": "Reed",
                "country": "United Kingdom",
                "joined_at": now - timedelta(days=365 * 2),
            },
            {
                "first_name": "Elena",
                "last_name": "Petrova",
                "country": "Ukraine",
                "joined_at": now - timedelta(days=365),
            },
            {
                "first_name": "Kenji",
                "last_name": "Watanabe",
                "country": "Japan",
                "joined_at": now - timedelta(days=200),
            },
            {
                "first_name": "Amara",
                "last_name": "Okafor",
                "country": "Nigeria",
                "joined_at": now - timedelta(days=90),
            },
        ]

        created_count = 0
        author_objs = []
        for data in authors:
            author, created = Author.objects.get_or_create(
                first_name=data["first_name"],
                last_name=data["last_name"],
                defaults=data,
            )
            author_objs.append(author)
            created_count += created

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeding complete: {created_count} Author row(s) created, "
                f"{len(authors) - created_count} already existed."
            )
        )
        return author_objs

    def seed_blogs(self, authors):
        now = timezone.now()
        blog_images = [f"assets/img/blog/blog-{n}.jpg" for n in range(1, 7)]

        blogs = [
            {
                "title": "10 Digital Marketing Trends to Watch This Year",
                "category": "Marketing",
                "content": (
                    "From AI-driven personalization to short-form video, the "
                    "digital marketing landscape keeps shifting. Here's a look "
                    "at the trends shaping how brands reach their audiences."
                ),
            },
            {
                "title": "Why Your Business Needs a Content Strategy",
                "category": "Content",
                "content": (
                    "Publishing without a plan wastes effort. A clear content "
                    "strategy aligns what you write with what your audience "
                    "actually wants to read, and what moves the business "
                    "forward."
                ),
            },
            {
                "title": "The Art of Building Brand Identity",
                "category": "Branding",
                "content": (
                    "A strong brand identity is more than a logo. It's the "
                    "consistent voice, visuals, and values that make a "
                    "company instantly recognizable."
                ),
            },
            {
                "title": "SEO Basics Every Small Business Should Know",
                "category": "SEO",
                "content": (
                    "Search engine optimization doesn't have to be "
                    "overwhelming. These fundamentals will help your site "
                    "rank without needing a full-time specialist."
                ),
            },
            {
                "title": "How to Measure Marketing ROI That Actually Matters",
                "category": "Analytics",
                "content": (
                    "Vanity metrics look good in a slide deck but rarely "
                    "explain business impact. Here's how to track the "
                    "numbers that tie back to revenue."
                ),
            },
            {
                "title": "Social Media Strategies for Small Businesses",
                "category": "Social Media",
                "content": (
                    "You don't need a huge budget to build a presence on "
                    "social media. Consistency and a clear voice go further "
                    "than paid reach alone."
                ),
            },
            {
                "title": "Email Marketing Is Not Dead: Here's Proof",
                "category": "Marketing",
                "content": (
                    "Despite predictions of its demise, email remains one of "
                    "the highest-ROI marketing channels. The key is "
                    "segmentation and timing, not volume."
                ),
            },
            {
                "title": "Design Principles That Improve Conversion Rates",
                "category": "Design",
                "content": (
                    "Good design isn't just about looking polished. Layout, "
                    "contrast, and clear calls to action all directly "
                    "influence whether visitors convert."
                ),
            },
            {
                "title": "Building Customer Trust Through Transparency",
                "category": "Branding",
                "content": (
                    "Customers reward companies that are upfront about "
                    "pricing, sourcing, and mistakes. Transparency builds "
                    "trust that outlasts any single campaign."
                ),
            },
            {
                "title": "A Beginner's Guide to Web Development Wizardry",
                "category": "Web Development",
                "content": (
                    "Whether you're commissioning a website or building your "
                    "own, understanding the basics of front-end and back-end "
                    "development helps you make better decisions."
                ),
            },
        ]

        created_count = 0
        for index, data in enumerate(blogs):
            data["blog_image"] = blog_images[index % len(blog_images)]
            data["author"] = authors[index % len(authors)]
            # spread posts across the last 10 days, oldest first, so the
            # last entries are the most recently created
            data["created_at"] = now - timedelta(days=len(blogs) - index)
            _, created = Blog.objects.get_or_create(
                title=data["title"], defaults=data
            )
            created_count += created

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeding complete: {created_count} Blog row(s) created, "
                f"{len(blogs) - created_count} already existed."
            )
        )
