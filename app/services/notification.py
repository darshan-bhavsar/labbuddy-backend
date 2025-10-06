from typing import List
from sqlalchemy.orm import Session
from ..models.notification import Notification
from ..models.user import User, UserRole
from ..models.report import Report, ReportStatus


class NotificationService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_notification(self, user_id: int, message: str, report_id: int = None) -> Notification:
        """Create a new notification."""
        notification = Notification(
            user_id=user_id,
            message=message,
            report_id=report_id
        )
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification
    
    def send_report_created_notifications(self, report: Report):
        """Send notifications when a new report is created."""
        # Notify lab admin and lab staff
        lab_users = self.db.query(User).filter(
            User.lab_id == report.lab_id,
            User.role.in_([UserRole.LAB_ADMIN, UserRole.LAB_STAFF, UserRole.LAB_BOY])
        ).all()
        
        message = f"New report booking created for patient {report.patient.name} (Report ID: {report.report_id})"
        
        for user in lab_users:
            self.create_notification(
                user_id=user.user_id,
                message=message,
                report_id=report.report_id
            )
        
        # Notify hospital if report is from hospital
        if report.hospital_id:
            hospital_users = self.db.query(User).filter(
                User.hospital_id == report.hospital_id,
                User.role == UserRole.HOSPITAL_USER
            ).all()
            
            hospital_message = f"Report booking confirmed for patient {report.patient.name} (Report ID: {report.report_id})"
            
            for user in hospital_users:
                self.create_notification(
                    user_id=user.user_id,
                    message=hospital_message,
                    report_id=report.report_id
                )
    
    def send_status_change_notifications(self, report: Report, old_status: ReportStatus):
        """Send notifications when report status changes."""
        new_status = report.status
        
        # Status change messages
        status_messages = {
            ReportStatus.SAMPLE_COLLECTED: "Sample collected for report",
            ReportStatus.IN_PROCESS: "Report processing started",
            ReportStatus.REPORT_READY: "Report is ready for delivery",
            ReportStatus.DELIVERED: "Report has been delivered"
        }
        
        if new_status in status_messages:
            message = f"{status_messages[new_status]} - Patient: {report.patient.name} (Report ID: {report.report_id})"
            
            # Notify hospital users
            if report.hospital_id:
                hospital_users = self.db.query(User).filter(
                    User.hospital_id == report.hospital_id,
                    User.role == UserRole.HOSPITAL_USER
                ).all()
                
                for user in hospital_users:
                    self.create_notification(
                        user_id=user.user_id,
                        message=message,
                        report_id=report.report_id
                    )
            
            # Notify lab staff for important status changes
            if new_status in [ReportStatus.REPORT_READY, ReportStatus.DELIVERED]:
                lab_users = self.db.query(User).filter(
                    User.lab_id == report.lab_id,
                    User.role.in_([UserRole.LAB_ADMIN, UserRole.LAB_STAFF])
                ).all()
                
                for user in lab_users:
                    self.create_notification(
                        user_id=user.user_id,
                        message=message,
                        report_id=report.report_id
                    )
    
    def get_user_notifications(self, user_id: int, limit: int = 50) -> List[Notification]:
        """Get notifications for a specific user."""
        return self.db.query(Notification).filter(
            Notification.user_id == user_id
        ).order_by(Notification.sent_at.desc()).limit(limit).all()
    
    def mark_notification_as_read(self, notification_id: int, user_id: int) -> bool:
        """Mark a notification as read."""
        notification = self.db.query(Notification).filter(
            Notification.notification_id == notification_id,
            Notification.user_id == user_id
        ).first()
        
        if notification:
            from ..models.notification import NotificationStatus
            notification.status = NotificationStatus.READ
            self.db.commit()
            return True
        return False
    
    def send_email_notification(self, user_email: str, subject: str, message: str):
        """Send email notification (placeholder for email service integration)."""
        # TODO: Integrate with email service (SendGrid, AWS SES, etc.)
        print(f"Email to {user_email}: {subject} - {message}")
        pass
