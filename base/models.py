from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default.jpg',  # Fixed default filename
        blank=True,
        null=True
    )
    phone_number = models.CharField(max_length=20, blank=True)
    
    def remove_profile_picture(self):
        """Remove the current profile picture and reset to default"""
        if self.profile_picture and self.profile_picture.name != 'profile_pics/default.jpg':
            # Delete the file from storage
            if os.path.isfile(self.profile_picture.path):
                os.remove(self.profile_picture.path)
            # Set to default
            self.profile_picture = 'profile_pics/default.jpg'
            self.save()
            
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def save(self, *args, **kwargs):
        # Delete old file when updating
        try:
            old = Profile.objects.get(id=self.id)
            if old.profile_picture and old.profile_picture != self.profile_picture:
                if os.path.isfile(old.profile_picture.path):
                    os.remove(old.profile_picture.path)
        except Profile.DoesNotExist:
            pass
        
        super().save(*args, **kwargs)
        
        # Resize image if exists
        if self.profile_picture:
            try:
                img = Image.open(self.profile_picture.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.profile_picture.path)
            except Exception as e:
                # Handle image processing errors gracefully
                print(f"Error processing image: {e}")

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()