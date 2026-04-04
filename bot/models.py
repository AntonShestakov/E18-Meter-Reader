"""
Tortoise ORM model definitions for E18 Meter Reader Bot.
"""

from tortoise import fields, Model


class User(Model):
    """User account model. ID is Telegram user ID."""

    id = fields.BigIntField(pk=True)  # Telegram user ID
    username = fields.CharField(max_length=255, null=True)
    full_name = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "users"

    def __str__(self):
        return f"User({self.id}, {self.full_name})"


class Apartment(Model):
    """Apartment model."""

    id = fields.IntField(pk=True)
    number = fields.CharField(max_length=32)
    floor = fields.IntField(null=True)
    notes = fields.TextField(null=True)

    class Meta:
        table = "apartments"

    def __str__(self):
        return f"Apartment({self.number})"


class Meter(Model):
    """Meter model."""

    id = fields.IntField(pk=True)
    apartment = fields.ForeignKeyField(
        "models.Apartment", related_name="meters", on_delete="CASCADE"
    )
    meter_number = fields.CharField(max_length=128)
    installed_at = fields.DateField(null=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "meters"

    def __str__(self):
        return f"Meter({self.meter_number})"


class UserRole(Model):
    """User role assignment model with time-scoped validity."""

    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        "models.User", related_name="roles", on_delete="CASCADE"
    )
    role = fields.CharField(
        max_length=32, choices=["administrator", "grayhound", "tenant"]
    )
    apartment = fields.ForeignKeyField(
        "models.Apartment",
        related_name="role_assignments",
        on_delete="SET NULL",
        null=True,
    )
    valid_from = fields.DateField()
    valid_to = fields.DateField(null=True)  # NULL = indefinite
    assigned_by = fields.ForeignKeyField(
        "models.User", related_name="assigned_roles", on_delete="SET NULL", null=True
    )
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "user_roles"

    def __str__(self):
        return f"UserRole({self.user_id}, {self.role})"


class Reading(Model):
    """Meter reading model."""

    id = fields.IntField(pk=True)
    meter = fields.ForeignKeyField(
        "models.Meter", related_name="readings", on_delete="CASCADE"
    )
    value = fields.DecimalField(max_digits=10, decimal_places=2)
    read_at = fields.DatetimeField(auto_now_add=True)
    submitted_by = fields.ForeignKeyField(
        "models.User", related_name="readings", on_delete="RESTRICT"
    )
    source = fields.CharField(max_length=32, choices=["numeric", "photo"])
    photo_file_id = fields.CharField(max_length=255, null=True)  # Telegram file_id
    notes = fields.TextField(null=True)

    class Meta:
        table = "readings"

    def __str__(self):
        return f"Reading({self.meter_id}, {self.value})"
