import db
import db.user_settings

def migrate_notification_settings():
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT user_uuid, notification_login, notification_door_access FROM user_link_kakaowork WHERE notification_login IS NOT NULL OR notification_door_access IS NOT NULL')
        users_with_notifications = cursor.fetchall()
        
        migrated_count = 0
        
        for user in users_with_notifications:
            user_uuid = user['user_uuid']
            notification_login = user['notification_login']
            notification_door_access = user['notification_door_access']
            
            if notification_login is not None:
                result = db.user_settings.set_setting(user_uuid, 'notification_login', notification_login, 'boolean')
                if result.success:
                    migrated_count += 1
            
            if notification_door_access is not None:
                result = db.user_settings.set_setting(user_uuid, 'notification_door_access', notification_door_access, 'boolean')
                if result.success:
                    migrated_count += 1
        
        cursor.execute('ALTER TABLE user_link_kakaowork DROP COLUMN notification_login')
        cursor.execute('ALTER TABLE user_link_kakaowork DROP COLUMN notification_door_access')
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
    finally:
        db.close_connection(conn)

if __name__ == "__main__":
    migrate_notification_settings()
