"""
Celery tasks for the blog app.
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Post, BlogComment
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def cleanup_old_draft_posts():
    """
    Periodic task to delete draft posts older than 30 days.
    This task runs daily to keep the database clean.
    """
    try:
        cutoff_date = timezone.now() - timedelta(days=30)
        old_drafts = Post.objects.filter(
            status='D',
            date__lt=cutoff_date
        )
        count = old_drafts.count()
        old_drafts.delete()
        print(f"Cleaned up {count} old draft posts")
        return f"Successfully deleted {count} old draft posts"
    except Exception as e:
        print(f"Error cleaning up draft posts: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def send_daily_blog_summary():
    """
    Periodic task to send a daily summary of blog activity.
    This task runs daily and sends an email with blog statistics.
    """
    try:
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        # Get statistics
        new_posts = Post.objects.filter(date=yesterday, status='P').count()
        new_comments = BlogComment.objects.filter(timestamp__date=yesterday).count()
        total_posts = Post.objects.filter(status='P').count()
        total_comments = BlogComment.objects.count()
        
        # Prepare email content
        subject = f'Daily Blog Summary - {today}'
        message = f"""
Daily Blog Summary for {yesterday}

New Published Posts: {new_posts}
New Comments: {new_comments}

Total Published Posts: {total_posts}
Total Comments: {total_comments}

---
This is an automated message from your CMS.
        """
        
        # Send email to admin (you can modify this to send to multiple recipients)
        if settings.EMAIL_HOST_USER:
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[],  # Send to admin email
                    fail_silently=False,
                )
                print(f"Daily blog summary sent successfully")
                return "Daily blog summary sent successfully"
            except Exception as email_error:
                error_msg = str(email_error)
                # Provide helpful error message for Gmail authentication issues
                if 'Application-specific password' in error_msg or 'InvalidSecondFactor' in error_msg:
                    helpful_msg = (
                        "Gmail authentication failed. Please ensure:\n"
                        "1. 2-Step Verification is enabled on your Google account\n"
                        "2. You're using an App-Specific Password (not your regular password)\n"
                        "3. The app password has NO SPACES (16 characters without spaces)\n"
                        "4. Generate a new app password at: https://myaccount.google.com/apppasswords\n"
                        f"Original error: {error_msg}"
                    )
                    print(f"Email error: {helpful_msg}")
                    return f"Error: {helpful_msg}"
                else:
                    print(f"Error sending daily blog summary: {error_msg}")
                    return f"Error: {error_msg}"
        else:
            print("Email not configured. Skipping email send.")
            return "Email not configured"
    except Exception as e:
        print(f"Error sending daily blog summary: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def count_total_likes():
    """
    Periodic task to count and log total likes across all posts.
    This is an example of a simple scheduled task.
    """
    try:
        total_likes = 0
        posts = Post.objects.all()
        for post in posts:
            total_likes += post.total_likes()
        
        print(f"Total likes across all posts: {total_likes}")
        return f"Total likes: {total_likes}"
    except Exception as e:
        print(f"Error counting likes: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def example_one_time_task(message):
    """
    Example of a one-time task that can be called from views or other parts of the app.
    Usage: example_one_time_task.delay("Hello from Celery!")
    """
    print(f"Received message: {message}")
    return f"Task completed with message: {message}"

