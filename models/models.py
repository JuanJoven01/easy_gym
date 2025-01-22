from odoo import models, fields, api
import base64

class Exercises(models.Model):
    _name = 'easy_gym.exercises'
    _description = 'General and default exercises for all users '
    name = fields.Char(translate=True)
    
    image = fields.Image(required=False)

    # @api.model
    # def init(self):
    #     """
    #     Create default exercises when the module is installed or updated.
    #     """
    #     default_exercises = [
    #         {'name': 'Push Ups'},
    #         {'name': 'Squats'},
    #         {'name': 'Pull Ups'},
    #         {'name': 'Lunges'},
    #     ]
    #     for exercise in default_exercises:
    #         if not self.env['easy_gym.exercises'].search([('name', '=', exercise['name'])]):
    #             self.create(exercise)

class CustomExercises(models.Model):
    _name = 'easy_gym.custom_exercises'
    _description = 'Exercises created per user '
    name = fields.Char()
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