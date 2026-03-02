from django.db import models
from django.utils.translation import gettext_lazy as _


class Message(models.Model):
    """Direct messages between users"""
    
    sender = models.ForeignKey(
        'users.User',
        related_name='messages_sent',
        on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        'users.User',
        related_name='messages_received',
        on_delete=models.CASCADE
    )
    exchange = models.ForeignKey(
        'exchanges.SkillExchange',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    
    content = models.TextField()
    
    # Message status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Attachments
    attachment = models.FileField(upload_to='message_attachments/', null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['sender', 'recipient']),
            models.Index(fields=['is_read']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = models.functions.Now()
            self.save(update_fields=['is_read', 'read_at'])


class Conversation(models.Model):
    """Conversation threads between two users"""
    
    user1 = models.ForeignKey(
        'users.User',
        related_name='conversations_as_user1',
        on_delete=models.CASCADE
    )
    user2 = models.ForeignKey(
        'users.User',
        related_name='conversations_as_user2',
        on_delete=models.CASCADE
    )
    
    exchange = models.ForeignKey(
        'exchanges.SkillExchange',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='conversation'
    )
    
    last_message = models.ForeignKey(
        Message,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    # Unread counts
    user1_unread_count = models.IntegerField(default=0)
    user2_unread_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user1', 'user2')
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user1']),
            models.Index(fields=['user2']),
        ]
    
    def __str__(self):
        return f"Conversation between {self.user1.username} and {self.user2.username}"
    
    def get_other_user(self, user):
        """Get the other user in the conversation"""
        return self.user2 if self.user1 == user else self.user1


class Notification(models.Model):
    """Notifications for users"""
    
    NOTIFICATION_TYPE_CHOICES = (
        ('exchange_proposed', _('Exchange Proposed')),
        ('exchange_accepted', _('Exchange Accepted')),
        ('exchange_completed', _('Exchange Completed')),
        ('exchange_cancelled', _('Exchange Cancelled')),
        ('message_received', _('Message Received')),
        ('skill_liked', _('Skill Liked')),
        ('skill_endorsed', _('Skill Endorsed')),
        ('user_followed', _('User Followed')),
        ('nearby_skill', _('Nearby Skill')),
        ('system_announcement', _('System Announcement')),
    )
    
    user = models.ForeignKey(
        'users.User',
        related_name='notifications',
        on_delete=models.CASCADE
    )
    
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Related objects
    related_user = models.ForeignKey(
        'users.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='notifications_about'
    )
    exchange = models.ForeignKey(
        'exchanges.SkillExchange',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    skill = models.ForeignKey(
        'skills.Skill',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Icon/Image
    icon = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='notification_images/', null=True, blank=True)
    
    # Action
    action_url = models.CharField(max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['is_read']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = models.functions.Now()
            self.save(update_fields=['is_read', 'read_at'])


class NotificationPreference(models.Model):
    """User preferences for notifications"""
    
    user = models.OneToOneField(
        'users.User',
        related_name='notification_preferences',
        on_delete=models.CASCADE
    )
    
    # Email notifications
    email_on_exchange = models.BooleanField(default=True)
    email_on_message = models.BooleanField(default=True)
    email_on_skill_like = models.BooleanField(default=True)
    email_on_nearby_skill = models.BooleanField(default=False)
    email_on_weekly_digest = models.BooleanField(default=True)
    
    # Push notifications
    push_on_exchange = models.BooleanField(default=True)
    push_on_message = models.BooleanField(default=True)
    push_on_skill_like = models.BooleanField(default=True)
    push_on_nearby_skill = models.BooleanField(default=False)
    
    # SMS notifications
    sms_on_important = models.BooleanField(default=False)
    
    # Quiet hours
    quiet_hours_enabled = models.BooleanField(default=False)
    quiet_hours_start = models.TimeField(default='22:00')
    quiet_hours_end = models.TimeField(default='08:00')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Notification preferences for {self.user.username}"
