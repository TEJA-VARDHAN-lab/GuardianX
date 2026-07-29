import logging

logger = logging.getLogger("uvicorn.error")


class NotificationDispatcher:
    @staticmethod
    def send(departments, message, snapshot=None):
        if not departments:
            logger.info("No departments selected for notification.")
            return

        if isinstance(departments, str):
            departments = [departments]

        for department in departments:
            NotificationDispatcher._dispatch_single(department, message, snapshot)

    @staticmethod
    def _dispatch_single(department, message, snapshot=None):
        logger.info("📨 Sending alert to %s", department)

        if department == "fire_department":
            NotificationDispatcher.send_fire(message, snapshot)
        elif department == "police":
            NotificationDispatcher.send_police(message, snapshot)
        elif department == "ambulance":
            NotificationDispatcher.send_ambulance(message, snapshot)
        else:
            logger.warning("Unknown department: %s", department)

    @staticmethod
    def send_fire(message, snapshot=None):
        logger.info("🔥 FIRE DEPARTMENT ALERT\n%s", message)

    @staticmethod
    def send_police(message, snapshot=None):
        logger.info("👮 POLICE ALERT\n%s", message)

    @staticmethod
    def send_ambulance(message, snapshot=None):
        logger.info("🚑 AMBULANCE ALERT\n%s", message)