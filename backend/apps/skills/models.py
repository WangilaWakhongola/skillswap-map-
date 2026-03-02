from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

class SkillCategory(models.Model):
    """Skill categories for organization"""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    color = models.CharField(max_length=7, default='#3B82F6', help_text="Hex color code")
    
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )
    
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = "Skill Categories"
    
    def __str__(self):
        return self.name


class Skill(models.Model):
    """User skill offerings and requests"""
    
    SKILL_TYPE_CHOICES = (
        ('offer', _('Offering')),
        ('request', _('Requesting')),
    )
    
    EXPERTISE_LEVEL_CHOICES = (
        ('beginner', _('Beginner')),
        ('intermediate', _('Intermediate')),
        ('advanced', _('Advanced')),
        ('expert', _('Expert')),
    )
    
    EXCHANGE_TYPE_CHOICES = (
        ('barter', _('Skill Barter')),
        ('paid', _('Paid')),
        ('both', _('Both')),
    )
    
    # Basic Information
    user = models.ForeignKey(
        'users.User',
        related_name='skills',
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        SkillCategory,
        related_name='skills',
        on_delete=models.PROTECT
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    skill_type = models.CharField(max_length=10, choices=SKILL_TYPE_CHOICES)
    
    # Details
    expertise_level = models.CharField(max_length=20, choices=EXPERTISE_LEVEL_CHOICES)
    experience_years = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    
    # Images
    image = models.ImageField(upload_to='skills/', null=True, blank=True)
    gallery = models.JSONField(default=list, blank=True, help_text="List of image URLs")
    
    # Exchange Information
    exchange_type = models.CharField(max_length=10, choices=EXCHANGE_TYPE_CHOICES, default='barter')
    price_per_hour = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    currency = models.CharField(max_length=3, default='USD')
    
    # Availability
    available_monday = models.BooleanField(default=True)
    available_tuesday = models.BooleanField(default=True)
    available_wednesday = models.BooleanField(default=True)
    available_thursday = models.BooleanField(default=True)
    available_friday = models.BooleanField(default=True)
    available_saturday = models.BooleanField(default=True)
    available_sunday = models.BooleanField(default=True)
    
    start_time = models.TimeField(default='08:00')
    end_time = models.TimeField(default='20:00')
    
    # Location
    available_online = models.BooleanField(default=False)
    available_in_person = models.BooleanField(default=True)
    max_distance_km = models.IntegerField(default=50, validators=[MinValueValidator(1)])
    
    # Status and Engagement
    is_active = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    
    # Ratings
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_exchanges = models.IntegerField(default=0)
    
    # Search (PostgreSQL full-text search)
    search_vector = SearchVectorField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['user']),
            models.Index(fields=['skill_type']),
            models.Index(fields=['is_active']),
            models.Index(fields=['-created_at']),
            GinIndex(fields=['search_vector']),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.user.username}"
    
    def get_availability_days(self):
        """Return list of available days"""
        days = []
        day_map = {
            0: 'available_monday',
            1: 'available_tuesday',
            2: 'available_wednesday',
            3: 'available_thursday',
            4: 'available_friday',
            5: 'available_saturday',
            6: 'available_sunday',
        }
        for day_num, field_name in day_map.items():
            if getattr(self, field_name):
                days.append(day_num)
        return days


class SkillLike(models.Model):
    """Track users liking skills"""
    
    user = models.ForeignKey(
        'users.User',
        related_name='liked_skills',
        on_delete=models.CASCADE
    )
    skill = models.ForeignKey(
        Skill,
        related_name='liked_by',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'skill')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} likes {self.skill.title}"


class SkillImage(models.Model):
    """Additional images for skills"""
    
    skill = models.ForeignKey(
        Skill,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='skill_images/')
    caption = models.CharField(max_length=200, blank=True)
    display_order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_order', 'uploaded_at']
    
    def __str__(self):
        return f"Image for {self.skill.title}"


class SkillEndorsement(models.Model):
    """Users can endorse each other's skills"""
    
    endorser = models.ForeignKey(
        'users.User',
        related_name='endorsements_given',
        on_delete=models.CASCADE
    )
    skill = models.ForeignKey(
        Skill,
        related_name='endorsements',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('endorser', 'skill')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.endorser.username} endorses {self.skill.title}"
