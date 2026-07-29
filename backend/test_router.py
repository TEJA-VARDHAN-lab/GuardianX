from app.services.emergency_router import EmergencyRouter


print(
    EmergencyRouter.get_departments(
        "fire"
    )
)


print(
    EmergencyRouter.get_departments(
        "weapon"
    )
)