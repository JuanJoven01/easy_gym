from odoo import models, fields, api

class Exercises(models.Model):
    _name = 'easy_gym.exercises'
    _description = 'General and default exercises for all users'
    
    name = fields.Char(translate=True, string='Exercise Name')
    focus_area = fields.Char(required=True, string='Main Area Worked', translate=True)

    @api.model
    def init(self):
        """
        Create default exercises when the module is installed or updated.
        """
        default_exercises = [
            # Chest
            {'name': 'Barbell Bench Press', 'focus_area': 'Chest'},
            {'name': 'Incline Dumbbell Bench Press', 'focus_area': 'Chest'},
            {'name': 'Pec Deck', 'focus_area': 'Chest'},
            {'name': 'Cable Crossover', 'focus_area': 'Chest'},
            {'name': 'Incline Barbell Bench Press', 'focus_area': 'Chest'},
            {'name': 'Dumbbell Bench Press', 'focus_area': 'Chest'},
            {'name': 'Dumbbell Fly', 'focus_area': 'Chest'},
            {'name': 'Incline Dumbbell Fly', 'focus_area': 'Chest'},
            {'name': 'Chest Press Machine', 'focus_area': 'Chest'},
            {'name': 'Barbell Declined Bench Press', 'focus_area': 'Chest'},
            {'name': 'Dumbbell Declined Bench Press', 'focus_area': 'Chest'},
            {'name': 'Push Ups', 'focus_area': 'Chest'},

            # Back
            {'name': 'Dumbbell Bent-Over Row (Single Arm)', 'focus_area': 'Back'},
            {'name': 'Wide-Grip Pulldown', 'focus_area': 'Back'},
            {'name': 'Seated Cable Row', 'focus_area': 'Back'},
            {'name': 'Close-Grip Pulldown', 'focus_area': 'Back'},
            {'name': 'Barbell Row', 'focus_area': 'Back'},
            {'name': 'Behind-Neck Pulldown', 'focus_area': 'Back'},
            {'name': 'Reverse-Grip Pulldown', 'focus_area': 'Back'},
            {'name': 'Rope Pulldown', 'focus_area': 'Back'},
            {'name': 'T-Bar Rows', 'focus_area': 'Back'},
            {'name': 'Pull Up', 'focus_area': 'Back'},

            # Shoulders
            {'name': 'Dumbbell Shoulder Press', 'focus_area': 'Shoulders'},
            {'name': 'Dumbbell Lateral Raise', 'focus_area': 'Shoulders'},
            {'name': 'Dumbbell Front Raise', 'focus_area': 'Shoulders'},
            {'name': 'Cable One-Arm Lateral Raise', 'focus_area': 'Shoulders'},

            # Biceps
            {'name': 'Barbell Curl', 'focus_area': 'Biceps'},
            {'name': 'Alternating Dumbbell Curl', 'focus_area': 'Biceps'},
            {'name': 'Rope Cable Curl', 'focus_area': 'Biceps'},
            {'name': 'Hammer Curl', 'focus_area': 'Biceps'},

            # Triceps
            {'name': 'Lying Triceps Extension', 'focus_area': 'Triceps'},
            {'name': 'Triceps Pressdown', 'focus_area': 'Triceps'},
            {'name': 'Cable Rope Pushdown', 'focus_area': 'Triceps'},

            # Abdominals
            {'name': 'Crunch', 'focus_area': 'Abdominals'},
            {'name': 'Oblique Crunch', 'focus_area': 'Abdominals'},
            {'name': 'Crunch Machine', 'focus_area': 'Abdominals'},
            {'name': 'Rope Ab Pulldown', 'focus_area': 'Abdominals'},

            # Legs
            {'name': 'Squat', 'focus_area': 'Legs'},
            {'name': 'Leg Press', 'focus_area': 'Legs'},
            {'name': 'Lunge', 'focus_area': 'Legs'},
            {'name': 'Barbell Stiff-Leg Deadlift', 'focus_area': 'Legs'},

            # Calves
            {'name': 'Seated Calf Raise', 'focus_area': 'Calves'},
            {'name': 'Standing Calf Raise', 'focus_area': 'Calves'}
        ]

        for exercise in default_exercises:
            if not self.env['easy_gym.exercises'].search([('name', '=', exercise['name'])]):
                self.create(exercise)


class CustomExercises(models.Model):
    _name = 'easy_gym.custom_exercises'
    _description = 'Exercises created per user '
    name = fields.Char()
    focus_area = fields.Char(required=True)
    image = fields.Image(required=False)
    
class CustomRoutines(models.Model):
    _name = 'easy_gym.custom_routines'
    _description = 'Exercises created per user '
    name = fields.Char()

class ExercisesRecords(models.Model):
    _name = 'easy_gym.exercises_records'
    _description = 'Exercises created per user '
    name = fields.Char()

class RoutinesRecords(models.Model):
    _name = 'easy_gym.routines_records'
    _description = 'Exercises created per user '
    name = fields.Char()

def load_image_as_base64(image_path):
    """
    Load an image file and return its Base64 encoded content.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')