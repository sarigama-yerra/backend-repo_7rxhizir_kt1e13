"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
import datetime as dt

# Example schemas (you can keep these if needed):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Fitness Tracker Schemas

class Workout(BaseModel):
    """
    Workouts performed by the user
    Collection name: "workout"
    """
    model_config = ConfigDict(populate_by_name=True)

    date: dt.date = Field(..., description="Date of the workout")
    workout_type: Literal[
        "Cardio",
        "Strength",
        "HIIT",
        "Yoga",
        "Pilates",
        "Sports",
        "Other",
    ] = Field("Cardio", description="Workout category", alias="type")
    duration_min: int = Field(..., ge=1, le=1440, description="Duration in minutes")
    calories: Optional[int] = Field(None, ge=0, description="Estimated calories burned")
    notes: Optional[str] = Field(None, description="Optional notes about the session")

class Metric(BaseModel):
    """
    Body metrics tracked over time
    Collection name: "metric"
    """
    date: dt.date = Field(..., description="Date of the measurement")
    weight_kg: Optional[float] = Field(None, ge=0, description="Weight in kilograms")
    body_fat_pct: Optional[float] = Field(None, ge=0, le=100, description="Body fat percentage")
    resting_hr: Optional[int] = Field(None, ge=0, le=300, description="Resting heart rate (bpm)")
