from django.db import models
from django.utils import timezone

# Try to import Cloudinary storage, fallback to default
try:
    from cloudinary_storage.storage import MediaCloudinaryStorage
    cloudinary_storage = MediaCloudinaryStorage()
except ImportError:
    cloudinary_storage = None

# Create your models here.

class AcademicProgram(models.Model):
    """Model for academic programs offered by CCB"""
    
    PROGRAM_TYPES = [
        ('BS', 'Bachelor of Science'),
        ('BA', 'Bachelor of Arts'),
        ('MA', 'Master of Arts'),
        ('MS', 'Master of Science'),
    ]
    
    title = models.CharField(max_length=200, help_text="Full program title (e.g., Bachelor of Science in Information Technology)")
    short_title = models.CharField(max_length=100, help_text="Short version of the title")
    program_type = models.CharField(max_length=2, choices=PROGRAM_TYPES, default='BS')
    description = models.TextField(help_text="Brief description of the program")
    duration_years = models.PositiveIntegerField(default=4, help_text="Duration in years")
    total_units = models.PositiveIntegerField(default=120, help_text="Total number of units")
    with_enhancements = models.PositiveIntegerField(default=0, help_text="Number of enhancements")
    
    # Program Details
    program_overview = models.TextField(blank=True, help_text="Detailed program overview and objectives")
    core_courses = models.TextField(blank=True, help_text="Core courses (one per line)")
    career_prospects = models.TextField(blank=True, help_text="Career prospects and opportunities")
    
    # Metadata
    is_active = models.BooleanField(default=True, help_text="Whether this program is currently offered")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Display order
    display_order = models.PositiveIntegerField(default=0, help_text="Order for display on website")
    
    class Meta:
        ordering = ['display_order', 'title']
        verbose_name = "Academic Program"
        verbose_name_plural = "Academic Programs"
    
    def __str__(self):
        return self.title
    
    @property
    def duration_text(self):
        """Return duration as formatted text"""
        return f"{self.duration_years} {'Year' if self.duration_years == 1 else 'Years'}"
    
    @property
    def units_text(self):
        """Return units as formatted text"""
        return f"{self.total_units} Units"
    
    @property
    def enhancements_text(self):
        """Return enhancements as formatted text"""
        if self.with_enhancements == 0:
            return "No Enhancements"
        elif self.with_enhancements == 1:
            return "With 1 Enhancement"
        else:
            return f"With {self.with_enhancements} Enhancements"

class ProgramSpecialization(models.Model):
    """Model for program specializations"""
    
    program = models.ForeignKey(AcademicProgram, on_delete=models.CASCADE, related_name='specializations')
    name = models.CharField(max_length=100, help_text="Specialization name")
    description = models.TextField(blank=True, help_text="Description of the specialization")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Program Specialization"
        verbose_name_plural = "Program Specializations"
    
    def __str__(self):
        return f"{self.program.short_title} - {self.name}"


class Announcement(models.Model):
    """News & Events announcements shown on the site."""
    title = models.CharField(max_length=200)
    date = models.DateField()
    body = models.TextField()
    details = models.TextField(blank=True, help_text="Full details shown in modal; falls back to body if empty")
    image = models.ImageField(
        upload_to='announcements/',
        blank=True,
        null=True,
        help_text="Announcement image",
        storage=cloudinary_storage
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-date', 'title']
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'

    def __str__(self):
        return f"{self.title} ({self.date})"


class Event(models.Model):
    """School Events and Activities shown on the site."""
    title = models.CharField(max_length=200, help_text="Event title")
    description = models.TextField(help_text="Brief description of the event")
    details = models.TextField(blank=True, help_text="Full details shown in modal; falls back to description if empty")
    event_date = models.DateField(help_text="Date of the event")
    start_time = models.TimeField(help_text="Start time of the event")
    end_time = models.TimeField(help_text="End time of the event")
    location = models.CharField(max_length=200, blank=True, help_text="Event location")
    image = models.ImageField(
        upload_to='events/',
        blank=True,
        null=True,
        help_text="Event image",
        storage=cloudinary_storage
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0, help_text="Order for display on website")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'event_date', 'start_time', 'title']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return f"{self.title} ({self.event_date})"
    
    @property
    def formatted_time(self):
        """Return formatted time range"""
        return f"{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"
    
    @property
    def formatted_date(self):
        """Return formatted date for display"""
        return self.event_date.strftime('%d %b').upper()


class Achievement(models.Model):
    """Achievements and Press Releases shown on the site."""
    title = models.CharField(max_length=200, help_text="Achievement title")
    description = models.TextField(help_text="Brief description of the achievement")
    details = models.TextField(blank=True, help_text="Full details shown in modal; falls back to description if empty")
    achievement_date = models.DateField(help_text="Date of the achievement")
    category = models.CharField(max_length=50, default='Achievement', help_text="Category (e.g., Achievement, Press Release, Award)")
    image = models.ImageField(
        upload_to='achievements/',
        blank=True,
        null=True,
        help_text="Achievement image",
        storage=cloudinary_storage
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0, help_text="Order for display on website")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-achievement_date', 'title']
        verbose_name = 'Achievement'
        verbose_name_plural = 'Achievements'

    def __str__(self):
        return f"{self.title} ({self.achievement_date})"
    
    @property
    def formatted_date(self):
        """Return formatted date for display"""
        return self.achievement_date.strftime('%B %d, %Y')


class ContactSubmission(models.Model):
    SUBJECT_CHOICES = [
        ('admissions', 'Admissions Inquiry'),
        ('academics', 'Academic Programs'),
        ('student-services', 'Student Services'),
        ('faculty', 'Faculty & Staff'),
        ('general', 'General Information'),
        ('complaint', 'Complaint'),
        ('suggestion', 'Suggestion'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('replied', 'Replied'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    message = models.TextField()
    verification_token = models.CharField(max_length=64, unique=True, blank=True)
    is_verified = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'

    def __str__(self):
        return f"{self.name} <{self.email}> ({self.subject})"


class EmailVerification(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=64, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Email Verification'
        verbose_name_plural = 'Email Verifications'

    def __str__(self):
        return f"{self.email} ({'used' if self.is_used else 'new'})"


class Department(models.Model):
    """Model for academic departments and administrative offices"""
    
    DEPARTMENT_TYPES = [
        ('academic', 'Academic Department'),
        ('administrative', 'Administrative Office'),
    ]
    
    name = models.CharField(max_length=200, help_text="Department or office name")
    department_type = models.CharField(max_length=20, choices=DEPARTMENT_TYPES, default='academic')
    description = models.TextField(blank=True, help_text="Brief description of the department")
    
    # Contact Information
    office_location = models.CharField(max_length=200, blank=True, help_text="Office location/room")
    phone = models.CharField(max_length=20, blank=True, help_text="Phone number")
    email = models.EmailField(blank=True, help_text="Email address")
    
    # Head/Dean Information
    head_name = models.CharField(max_length=100, blank=True, help_text="Department head/dean name")
    head_title = models.CharField(max_length=100, blank=True, help_text="Title (Dean, Director, etc.)")
    
    # Display settings
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0, help_text="Order for display on website")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['department_type', 'display_order', 'name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
    
    def __str__(self):
        return self.name


class Personnel(models.Model):
    """Model for faculty and staff members"""
    
    POSITION_TYPES = [
        ('faculty', 'Faculty'),
        ('administrative', 'Administrative Staff'),
        ('support', 'Support Staff'),
    ]
    
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='personnel')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    position_type = models.CharField(max_length=20, choices=POSITION_TYPES, default='faculty')
    title = models.CharField(max_length=100, help_text="Job title or position")
    specialization = models.CharField(max_length=200, blank=True, help_text="Area of specialization or expertise")
    
    # Contact Information
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    office_location = models.CharField(max_length=100, blank=True)
    
    # Additional Information
    bio = models.TextField(blank=True, help_text="Brief biography or background")
    qualifications = models.TextField(blank=True, help_text="Educational qualifications")
    
    # Display settings
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['department', 'position_type', 'display_order', 'last_name', 'first_name']
        verbose_name = 'Personnel'
        verbose_name_plural = 'Personnel'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.title}"
    
    @property
    def full_name(self):
        """Return full name"""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    @property
    def display_title(self):
        """Return formatted title with specialization"""
        if self.specialization:
            return f"{self.title} - {self.specialization}"
        return self.title


class AdmissionRequirement(models.Model):
    """Model for admission requirements by category"""
    
    CATEGORY_CHOICES = [
        ('new-scholar', 'New Student (Scholar)'),
        ('new-non-scholar', 'New Student (Non-Scholar)'),
        ('continuing-scholar', 'Continuing Student (Scholar)'),
        ('continuing-non-scholar', 'Continuing Student (Non-Scholar)'),
    ]
    
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, help_text="Student category")
    requirement_text = models.TextField(help_text="Requirement description")
    display_order = models.PositiveIntegerField(default=0, help_text="Order for display")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'display_order', 'requirement_text']
        verbose_name = 'Admission Requirement'
        verbose_name_plural = 'Admission Requirements'
    
    def __str__(self):
        return f"{self.get_category_display()}: {self.requirement_text[:50]}..."


class EnrollmentProcessStep(models.Model):
    """Model for enrollment process steps"""
    
    CATEGORY_CHOICES = [
        ('new-scholar', 'New Student (Scholar)'),
        ('new-non-scholar', 'New Student (Non-Scholar)'),
        ('continuing-scholar', 'Continuing Student (Scholar)'),
        ('continuing-non-scholar', 'Continuing Student (Non-Scholar)'),
    ]
    
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='new-scholar', help_text="Student category")
    step_number = models.PositiveIntegerField(help_text="Step number in the process")
    title = models.CharField(max_length=200, help_text="Step title")
    description = models.TextField(help_text="Step description")
    display_order = models.PositiveIntegerField(default=0, help_text="Order for display")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'display_order', 'step_number']
        verbose_name = 'Enrollment Process Step'
        verbose_name_plural = 'Enrollment Process Steps'
    
    def __str__(self):
        return f"{self.get_category_display()}: Step {self.step_number}: {self.title}"


class AdmissionNote(models.Model):
    """Model for important admission notes"""
    
    title = models.CharField(max_length=200, help_text="Note title")
    note_text = models.TextField(help_text="Note content")
    display_order = models.PositiveIntegerField(default=0, help_text="Order for display")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', 'title']
        verbose_name = 'Admission Note'
        verbose_name_plural = 'Admission Notes'
    
    def __str__(self):
        return self.title


class News(models.Model):
    """Model for news articles with images"""
    title = models.CharField(max_length=200, help_text="News title")
    date = models.DateField(help_text="Publication date")
    body = models.TextField(help_text="News content")
    details = models.TextField(blank=True, help_text="Full details shown in modal; falls back to body if empty")
    image = models.ImageField(
        upload_to='news/',
        blank=True,
        null=True,
        help_text="News image",
        storage=cloudinary_storage  # Force Cloudinary storage for images
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-date', 'title']
        verbose_name = 'News'
        verbose_name_plural = 'News'

    def __str__(self):
        return f"{self.title} ({self.date})"


class InstitutionalInfo(models.Model):
    """Model for institutional information: Mission, Vision, Goals, and Core Values"""
    
    # Mission, Vision, Goals
    vision = models.TextField(help_text="Institution vision statement")
    mission = models.TextField(help_text="Institution mission statement")
    goals = models.TextField(help_text="Institution goals (one per line)")
    core_values = models.TextField(help_text="Core values description")
    
    # Metadata
    is_active = models.BooleanField(default=True, help_text="Whether this information is currently active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Institutional Information'
        verbose_name_plural = 'Institutional Information'
        ordering = ['-updated_at']
    
    def __str__(self):
        return "Institutional Information"
    
    def save(self, *args, **kwargs):
        # Ensure only one active record exists
        if self.is_active:
            InstitutionalInfo.objects.exclude(pk=self.pk).filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)


class Download(models.Model):
    """
    Model for downloadable files and documents.
    
    This model manages downloadable resources such as forms, policies, manuals, and other documents
    that can be accessed by users through the Downloads page. Files are organized by category
    and can be enabled/disabled for public visibility.
    
    Attributes:
        category: The category/type of download (forms, HR policies, syllabi, etc.)
        title: Display name for the download
        description: Optional description of the download content
        file: The actual file to be downloaded (PDF, DOC, DOCX, XLS, XLSX, ZIP, RAR)
        file_type: Auto-detected file type based on extension
        is_active: Controls whether the download is visible on the public site
        display_order: Ordering for display within the same category
    """
    
    CATEGORY_CHOICES = [
        ('forms-enrollment', 'Forms - Enrollment'),
        ('forms-clearance', 'Forms - Clearance'),
        ('forms-request', 'Forms - Request'),
        ('forms-shift-change', 'Forms - Shift/Change'),
        ('hr-policies', 'HR Policies'),
        ('hr-forms', 'HR Forms'),
        ('syllabi', 'Syllabi'),
        ('manuals', 'Manuals'),
        ('handbooks', 'Handbooks'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='other', help_text="Download category")
    title = models.CharField(max_length=200, help_text="Download title/name")
    description = models.TextField(blank=True, help_text="Brief description of the download")
    file = models.FileField(upload_to='downloads/', help_text="File to download (PDF, DOC, etc.)")
    file_type = models.CharField(max_length=50, blank=True, help_text="File type (e.g., PDF, DOCX)")
    
    # Metadata
    is_active = models.BooleanField(default=True, help_text="Whether this download is currently available")
    display_order = models.PositiveIntegerField(default=0, help_text="Order for display on website")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'display_order', 'title']
        verbose_name = 'Download'
        verbose_name_plural = 'Downloads'
    
    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
    
    def save(self, *args, **kwargs):
        """
        Override save method to auto-detect file type from filename extension.
        This ensures file_type is automatically set when a file is uploaded,
        improving data consistency and reducing manual input requirements.
        """
        # Auto-detect file type from filename if not set
        if self.file and not self.file_type:
            filename = self.file.name.lower()
            if filename.endswith('.pdf'):
                self.file_type = 'PDF'
            elif filename.endswith(('.doc', '.docx')):
                self.file_type = 'DOC'
            elif filename.endswith(('.xls', '.xlsx')):
                self.file_type = 'XLS'
            elif filename.endswith(('.zip', '.rar')):
                self.file_type = 'ZIP'
            else:
                self.file_type = 'FILE'
        super().save(*args, **kwargs)


class ChatbotSession(models.Model):
    """Track chatbot conversation sessions"""
    session_id = models.CharField(max_length=255, unique=True, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    message_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-last_activity']
        verbose_name = 'Chatbot Session'
        verbose_name_plural = 'Chatbot Sessions'
    
    def __str__(self):
        return f"Session {self.session_id} ({self.message_count} messages)"


class ChatbotMessage(models.Model):
    """Store chatbot conversation messages"""
    session = models.ForeignKey(ChatbotSession, on_delete=models.CASCADE, related_name='messages')
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Chatbot Message'
        verbose_name_plural = 'Chatbot Messages'
    
    def __str__(self):
        return f"Message from {self.session.session_id} at {self.created_at}"