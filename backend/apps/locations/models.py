from django.db import models
from django.contrib.gis.db import models as gis_models
from django.utils.translation import gettext_lazy as _


class UserLocation(models.Model):
    """Track user current location"""
    
    user = models.OneToOneField(
        'users.User',
        related_name='current_location',
        on_delete=models.CASCADE
    )
    
    # Geographic location (using PostGIS)
    location = gis_models.PointField(null=True, blank=True)
    
    # Human readable address
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Accuracy info
    accuracy_radius_meters = models.IntegerField(null=True, blank=True)
    
    # Status
    is_precise = models.BooleanField(default=False, help_text="Is this GPS-level precision?")
    is_approximate = models.BooleanField(default=False, help_text="Is this approximate city-level?")
    
    # Privacy
    is_public = models.BooleanField(default=True)
    
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "User Locations"
    
    def __str__(self):
        return f"Location for {self.user.username}"


class LocationHistory(models.Model):
    """Track user location history"""
    
    user = models.ForeignKey(
        'users.User',
        related_name='location_history',
        on_delete=models.CASCADE
    )
    
    location = gis_models.PointField()
    address = models.CharField(max_length=255, blank=True)
    
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-recorded_at']
        verbose_name_plural = "Location Histories"
    
    def __str__(self):
        return f"Location history for {self.user.username}"


class GeometryZone(models.Model):
    """Define geographic zones for filtering"""
    
    ZONE_TYPE_CHOICES = (
        ('city', _('City')),
        ('district', _('District')),
        ('region', _('Region')),
        ('country', _('Country')),
        ('custom', _('Custom')),
    )
    
    name = models.CharField(max_length=200)
    zone_type = models.CharField(max_length=20, choices=ZONE_TYPE_CHOICES)
    
    # Geometry
    geometry = gis_models.PolygonField(null=True, blank=True)
    center_point = gis_models.PointField(null=True, blank=True)
    
    # Metadata
    country_code = models.CharField(max_length=2, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class NearbySkillAlert(models.Model):
    """Alert users when nearby skills match their interests"""
    
    user = models.ForeignKey(
        'users.User',
        related_name='nearby_alerts',
        on_delete=models.CASCADE
    )
    
    skill_category = models.ForeignKey(
        'skills.SkillCategory',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='nearby_alerts'
    )
    
    radius_km = models.IntegerField(default=50)
    is_active = models.BooleanField(default=True)
    
    # Notification settings
    notify_via_email = models.BooleanField(default=True)
    notify_via_push = models.BooleanField(default=True)
    
    # Trigger settings
    minimum_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'skill_category')
    
    def __str__(self):
        return f"Nearby alert for {self.user.username}"


class SavedLocation(models.Model):
    """Users can save favorite locations"""
    
    LOCATION_TYPE_CHOICES = (
        ('home', _('Home')),
        ('work', _('Work')),
        ('favorite', _('Favorite Spot')),
        ('custom', _('Custom')),
    )
    
    user = models.ForeignKey(
        'users.User',
        related_name='saved_locations',
        on_delete=models.CASCADE
    )
    
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPE_CHOICES)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    
    # Geographic location
    location = gis_models.PointField()
    
    is_primary = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_primary', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"


class Landmark(models.Model):
    """Popular landmarks and meeting points"""
    
    LANDMARK_TYPE_CHOICES = (
        ('park', _('Park')),
        ('cafe', _('Café')),
        ('library', _('Library')),
        ('community_center', _('Community Center')),
        ('plaza', _('Plaza')),
        ('other', _('Other')),
    )
    
    name = models.CharField(max_length=200)
    landmark_type = models.CharField(max_length=30, choices=LANDMARK_TYPE_CHOICES)
    description = models.TextField(blank=True)
    
    # Geographic location
    location = gis_models.PointField()
    
    # Details
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    
    # Ratings
    popularity_score = models.IntegerField(default=0)
    
    image = models.ImageField(upload_to='landmarks/', null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['landmark_type']),
        ]
    
    def __str__(self):
        return self.name
