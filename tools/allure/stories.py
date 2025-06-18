from enum import Enum


class AllureStory(str, Enum):
    COURSES = "Courses"
    DASHBOARD = "Dashboard"
    AUTHORIZATION = "Authorization"
    REGISTRATION = "Registration"
