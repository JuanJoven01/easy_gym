import base64
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ExerciseFocusArea(models.Model):
    _name = 'easy_gym.focus_area'
    _description = 'Exercise Focus Areas'
    name = fields.Char(required=True, translate=True, string='Focus Area Name')
    image = fields.Image(required=False)

class Exercises(models.Model):
    _name = 'easy_gym.exercises'
    _description = 'General and default exercises for all users'
    
    name = fields.Char(translate=True, string='Exercise Name')
    focus_area_id = fields.Many2one('easy_gym.focus_area', string='Main Area Worked', required=True)
    image = fields.Image(required=False)

    @api.model
    def init(self):
        """
        Create default focus areas and exercises when the module is installed or updated.
        """
        # Define the focus areas
        default_focus_areas = ['Chest', 'Back', 'Shoulders', 'Biceps', 'Triceps', 'Abdominals', 'Legs', 'Calves']
        
        focus_area_map = {}
        for area in default_focus_areas:
            focus_area = self.env['easy_gym.focus_area'].search([('name', '=', area)], limit=1)
            if not focus_area:
                focus_area = self.env['easy_gym.focus_area'].create({'name': area})
            focus_area_map[area] = focus_area.id

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
                self.create({
                    'name': exercise['name'],
                    'focus_area_id': focus_area_map[exercise['focus_area']]
                })


class CustomExercises(models.Model):
    _name = 'easy_gym.custom_exercises'
    _description = 'Exercises created per user '
    name = fields.Char()
    focus_area_id = fields.Many2one('easy_gym.focus_area', string='Main Area Worked', required=True)
    image = fields.Image(required=False)

    
class CustomRoutines(models.Model):
    _name = 'easy_gym.custom_routines'
    _description = 'Custom routines created per user'

    name = fields.Char(required=True, string='Routine Name')
    user_id = fields.Many2one('res.users', string='User', required=True)
    routine_exercise_ids = fields.One2many('easy_gym.routine_exercise', 'routine_id', string='Exercises with order and series')

class RoutineExercise(models.Model):
    _name = 'easy_gym.routine_exercise'
    _description = 'Exercises included in a routine with order and sequence'

    routine_id = fields.Many2one('easy_gym.custom_routines', string='Routine', required=True, ondelete='cascade')
    exercise_id = fields.Many2one('easy_gym.exercises', string='Exercise', required=False, ondelete='cascade')
    custom_exercise_id = fields.Many2one('easy_gym.custom_exercises', string='Exercise', required=False, ondelete='cascade')
    order = fields.Integer(string='Order')  # Order of exercises in the routine
    superserie_group = fields.Integer(string='Superserie Group', default=0)  # Group exercises together in superseries

class ExercisesRecords(models.Model):
    _name = 'easy_gym.exercises_records'
    _description = 'Records of exercises performed by users'

    user_id = fields.Many2one('res.users', string='User', required=True)
    routine_exercise_id = fields.Many2one('easy_gym.routine_exercise', string='Routine Exercise', required=True)
    routine_record_id = fields.Many2one('easy_gym.routines_records', string='Routine Record', ondelete='cascade')
    date = fields.Date(string='Date', default=fields.Date.today)
    repetitions = fields.Integer(string='Repetitions')
    weight = fields.Float(string='Weight (kg)')
    duration = fields.Float(string='Duration (min)')

class RoutinesRecords(models.Model):
    _name = 'easy_gym.routines_records'
    _description = 'Records of routines performed by users'

    user_id = fields.Many2one('res.users', string='User', required=True)
    routine_id = fields.Many2one('easy_gym.custom_routines', string='Routine', required=True)
    exercise_records_ids = fields.One2many('easy_gym.exercises_records', 'routine_record_id', string='Exercise Records')
    date = fields.Date(string='Date', default=fields.Date.today)
    notes = fields.Text(string='Notes')
    duration = fields.Float(string='Duration (min)')

def load_image_as_base64(image_path):
    """
    Load an image file and return its Base64 encoded content.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')