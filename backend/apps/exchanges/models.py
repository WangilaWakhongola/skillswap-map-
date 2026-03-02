from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

class SkillExchange(models.Model):
    """Main model for skill exchanges between users"""
    
    STATUS_CHOICES = (
        ('proposed', _('Proposed')),
        ('accepted', _('Accepted')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
        ('disputed', _('Disputed')),
    )
    
    EXCHANGE_MODE_CHOICES = (
        ('barter', _('Skill Barter')),
        ('paid', _('Paid Exchange')),
    )
    
    # Participants
    initiator = models.ForeignKey(
        'users.User',
        related_name='exchanges_initiated',
        on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        'users.User',
        related_name='exchanges_received',
        on_delete=models.CASCADE
    )
    
    # Skills involved
    initiator_skill = models.ForeignKey(
        'skills.Skill',
        related_name='offered_in_exchanges',
        on_delete=models.CASCADE
    )
    recipient_skill = models.ForeignKey(
        'skills.Skill',
        related_name='requested_in_exchanges',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='proposed')
    exchange_mode = models.CharField(max_length=10, choices=EXCHANGE_MODE_CHOICES, default='barter')
    
    # Exchange Details
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Scheduling
    proposed_date = models.DateTimeField(null=True, blank=True)
    confirmed_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    duration_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1,
        validators=[MinValueValidator(0.5)]
    )
    
    # Payment (if applicable)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    currency = models.CharField(max_length=3, default='USD')
    payment_status = models.CharField(
        max_length=20,
        default='pending',
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('refunded', 'Refunded'),
            ('disputed', 'Disputed'),
        ]
    )
    
    # Location
    exchange_location = models.CharField(max_length=255, blank=True)
    is_online = models.BooleanField(default=False)
    
    # Ratings
    initiator_rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)]
    )
    recipient_rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)]
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['initiator']),
            models.Index(fields=['recipient']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"Exchange: {self.initiator.username} ↔ {self.recipient.username}"
    
    def is_pending_response(self):
        return self.status == 'proposed'
    
    def can_be_completed(self):
        return self.status == 'accepted'


class ExchangeProposal(models.Model):
    """Track individual exchange proposals"""
    
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('accepted', _('Accepted')),
        ('rejected', _('Rejected')),
        ('expired', _('Expired')),
    )
    
    exchange = models.OneToOneField(
        SkillExchange,
        related_name='proposal',
        on_delete=models.CASCADE
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True)
    
    responded_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Proposal for {self.exchange}"


class ExchangeSession(models.Model):
    """Track individual sessions of an exchange"""
    
    STATUS_CHOICES = (
        ('scheduled', _('Scheduled')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
        ('rescheduled', _('Rescheduled')),
    )
    
    exchange = models.ForeignKey(
        SkillExchange,
        related_name='sessions',
        on_delete=models.CASCADE
    )
    
    session_number = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    # Timing
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    actual_start_time = models.DateTimeField(null=True, blank=True)
    actual_end_time = models.DateTimeField(null=True, blank=True)
    
    # Details
    location = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    
    # Attendance
    initiator_confirmed = models.BooleanField(default=False)
    recipient_confirmed = models.BooleanField(default=False)
    initiator_attended = models.BooleanField(null=True, blank=True)
    recipient_attended = models.BooleanField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['start_time']
        unique_together = ('exchange', 'session_number')
    
    def __str__(self):
        return f"Session {self.session_number} - {self.exchange}"


class ExchangeDocument(models.Model):
    """Attach documents or evidence to exchanges"""
    
    DOCUMENT_TYPE_CHOICES = (
        ('contract', _('Contract')),
        ('certificate', _('Certificate')),
        ('proof', _('Proof')),
        ('receipt', _('Receipt')),
        ('other', _('Other')),
    )
    
    exchange = models.ForeignKey(
        SkillExchange,
        related_name='documents',
        on_delete=models.CASCADE
    )
    
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    file = models.FileField(upload_to='exchange_documents/')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    uploaded_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True
    )
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.exchange}"


class ExchangeDispute(models.Model):
    """Handle disputes between users"""
    
    STATUS_CHOICES = (
        ('open', _('Open')),
        ('investigating', _('Investigating')),
        ('resolved', _('Resolved')),
        ('closed', _('Closed')),
    )
    
    RESOLUTION_CHOICES = (
        ('favor_initiator', _('In Favor of Initiator')),
        ('favor_recipient', _('In Favor of Recipient')),
        ('mutual_agreement', _('Mutual Agreement')),
        ('no_resolution', _('No Resolution')),
    )
    
    exchange = models.OneToOneField(
        SkillExchange,
        related_name='dispute',
        on_delete=models.CASCADE
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    
    # Complaint
    complaint_by = models.ForeignKey(
        'users.User',
        related_name='disputes_filed',
        on_delete=models.CASCADE
    )
    complaint_reason = models.TextField()
    
    # Resolution
    resolution = models.CharField(
        max_length=20,
        choices=RESOLUTION_CHOICES,
        null=True,
        blank=True
    )
    resolution_notes = models.TextField(blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        'users.User',
        related_name='disputes_resolved',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Dispute - {self.exchange}"
