from odoo import models, fields, api


class gym_exercises(models.Model):
    _name = 'easy-gym.exercises'
    _description = 'General and default exercises for all users '
    name = fields.Char()
    image = fields.Image()

class gym_custom_exercises(models.Model):
    _name = 'easy-gym.custom_exercises'
    _description = 'Exercises created per user '
    name = fields.Char()
    image = fields.Image(required=False)

class gym_custom_routines(models.Model):
    _name = 'easy-gym.custom_routines'
    _description = 'Exercises created per user '
    name = fields.Char()

class gym_exercises_record(models.Model):
    _name = 'easy-gym.custom_routines'
    _description = 'Exercises created per user '
    name = fields.Char()

class gym_routines_record(models.Model):
    _name = 'easy-gym.custom_routines'
    _description = 'Exercises created per user '
    name = fields.Char()