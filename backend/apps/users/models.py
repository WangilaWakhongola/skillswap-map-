from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Extended User model with skill exchange profile"""
    
    EXPERTISE_LEVEL_CHOICES = (
        ('beginner', _('Beginner')),
        ('intermediate', _('Intermediate')),
        ('expert', _('Expert')),
        ('master', _('Master')),
    )
    
    # Profile Information
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    
    # Location
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Profile Statistics
    total_exchanges = models.IntegerField(default=0)
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_reviews = models.IntegerField(default=0)
    
    # Settings
    is_verified = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    allow_notifications = models.BooleanField(default=True)
    allow_messaging = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            models.Index(fields=['latitude', 'longitude']),
        ]
    
    def __str__(self):
        return f"{self.get_full_name()} (@{self.username})"
    
    def get_average_rating(self):
        if self.total_reviews == 0:
            return 0
        return self.rating / self.total_reviews


class UserFollowing(models.Model):
    """Track which users follow each other"""
    
    follower = models.ForeignKey(
        User, 
        related_name='following',
        on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        User, 
        related_name='followers',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'followed')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"


class UserVerification(models.Model):
    """Track user verification and identity"""
    
    VERIFICATION_TYPE_CHOICES = (
        ('email', _('Email')),
        ('phone', _('Phone')),
        ('id', _('ID Document')),
        ('social', _('Social Media')),
    )
    
    user = models.OneToOneField(
        User, 
        related_name='verification',
        on_delete=models.CASCADE
    )
    verification_type = models.CharField(max_length=20, choices=VERIFICATION_TYPE_CHOICES)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_document = models.FileField(
        upload_to='verifications/',
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name_plural = "User Verifications"
    
    def __str__(self):
        return f"{self.user.username} - {self.verification_type}"


class UserPreferences(models.Model):
    """User preferences and settings"""
    
    user = models.OneToOneField(
        User,
        related_name='preferences',
        on_delete=models.CASCADE
    )
    
    # Communication Preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    
    # Privacy
    show_location = models.BooleanField(default=True)
    show_profile_publicly = models.BooleanField(default=True)
    search_radius_km = models.IntegerField(default=50, validators=[MinValueValidator(1), MaxValueValidator(100)])
    
    # Content Preferences
    skill_languages = models.CharField(max_length=255, default='en', help_text='Comma-separated language codes')
    exchange_frequency = models.CharField(
        max_length=50,
        default='flexible',
        choices=[
            ('flexible', 'Flexible'),
            ('weekends', 'Weekends Only'),
            ('evenings', 'Evenings Only'),
            ('daytime', 'Daytime Only'),
        ]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "User Preferences"
    
    def __str__(self):
        return f"Preferences for {self.user.username}"


class Review(models.Model):
    """Reviews and ratings for users"""
    
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )
    
    reviewer = models.ForeignKey(
        User,
        related_name='reviews_given',
        on_delete=models.CASCADE
    )
    reviewed_user = models.ForeignKey(
        User,
        related_name='reviews_received',
        on_delete=models.CASCADE
    )
    exchange = models.ForeignKey(
        'exchanges.SkillExchange',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='reviews'
    )
    
    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    comment = models.TextField(max_length=1000)
    
    # Review aspects
    would_exchange_again = models.BooleanField(default=True)
    communication_rating = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    reliability_rating = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    skill_quality_rating = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('reviewer', 'exchange')
    
    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.reviewed_user.username}"
