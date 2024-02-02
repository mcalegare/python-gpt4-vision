# src/Categories.py

class Category:
    rows = [
        {
            'id': 1,
            'name': 'Meals & Foodstuffs',
            'keywords': 'meals, food, groceries, snacks',
            'slug': 'food',
            'qualified': True
        },
        {
            'id': 2,
            'name': 'Textbooks & Supplies',
            'keywords': 'textbooks, school supplies, office supplies, room decorations, educational materials',
            'slug': 'supplies',
            'qualified': True
        },
        {
            'id': 3,
            'name': 'Room & Board',
            'keywords': 'rent, utilities',
            'slug': 'rent',
            'qualified': True
        },
        {
            'id': 4,
            'name': 'Transportation',
            'keywords': 'transportation, public transit, airfare, rideshare',
            'slug': 'transportation',
            'qualified': False
        },
        {
            'id': 999,
            'name': 'Other',
            'keywords': 'all other expenses',
            'slug': 'other',
            'qualified': False
        }
    ]

    @staticmethod
    def all():
        return Category.rows