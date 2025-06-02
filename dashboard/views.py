from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date
import random
from nutrition.models import MealEntry, UserProfile, WaterIntake, WorkoutLog


def generate_daily_meal_plan(user_profile=None, target_date=None):
    """Generate a dynamic daily meal plan based on user profile and date"""
    if target_date is None:
        target_date = date.today()

    # Use date as seed for consistent daily plans
    random.seed(target_date.toordinal())

    # Default nutritional targets
    calorie_goal = user_profile.daily_calorie_goal if user_profile else 2000
    protein_goal = user_profile.daily_protein_goal if user_profile else 150
    carbs_goal = user_profile.daily_carbs_goal if user_profile else 250
    fat_goal = user_profile.daily_fat_goal if user_profile else 65

    # Meal plan database with various options
    breakfast_options = [
        {
            'name': 'Oatmeal Power Bowl',
            'items': [
                {'name': 'Steel-cut oats with blueberries', 'calories': 320, 'protein': 12, 'carbs': 58, 'fat': 6},
                {'name': 'Greek yogurt with honey', 'calories': 150, 'protein': 15, 'carbs': 20, 'fat': 3},
                {'name': 'Almonds (handful)', 'calories': 160, 'protein': 6, 'carbs': 6, 'fat': 14},
            ]
        },
        {
            'name': 'Protein Breakfast',
            'items': [
                {'name': 'Scrambled eggs (2 large)', 'calories': 180, 'protein': 12, 'carbs': 2, 'fat': 14},
                {'name': 'Whole grain toast', 'calories': 120, 'protein': 4, 'carbs': 22, 'fat': 2},
                {'name': 'Avocado (half)', 'calories': 160, 'protein': 2, 'carbs': 9, 'fat': 15},
                {'name': 'Orange juice (small)', 'calories': 80, 'protein': 1, 'carbs': 20, 'fat': 0},
            ]
        },
        {
            'name': 'Smoothie Bowl',
            'items': [
                {'name': 'Banana protein smoothie', 'calories': 280, 'protein': 25, 'carbs': 35, 'fat': 8},
                {'name': 'Granola topping', 'calories': 150, 'protein': 4, 'carbs': 25, 'fat': 6},
                {'name': 'Fresh berries', 'calories': 60, 'protein': 1, 'carbs': 15, 'fat': 0},
            ]
        }
    ]

    lunch_options = [
        {
            'name': 'Mediterranean Bowl',
            'items': [
                {'name': 'Grilled chicken breast', 'calories': 350, 'protein': 35, 'carbs': 0, 'fat': 8},
                {'name': 'Quinoa salad with vegetables', 'calories': 280, 'protein': 10, 'carbs': 45, 'fat': 8},
                {'name': 'Hummus with pita', 'calories': 180, 'protein': 8, 'carbs': 20, 'fat': 8},
                {'name': 'Mixed greens', 'calories': 40, 'protein': 2, 'carbs': 8, 'fat': 0},
            ]
        },
        {
            'name': 'Asian Fusion',
            'items': [
                {'name': 'Teriyaki salmon', 'calories': 320, 'protein': 28, 'carbs': 12, 'fat': 18},
                {'name': 'Brown rice', 'calories': 220, 'protein': 5, 'carbs': 45, 'fat': 2},
                {'name': 'Steamed vegetables', 'calories': 80, 'protein': 3, 'carbs': 16, 'fat': 1},
                {'name': 'Miso soup', 'calories': 60, 'protein': 4, 'carbs': 8, 'fat': 2},
            ]
        },
        {
            'name': 'Power Salad',
            'items': [
                {'name': 'Mixed greens with chickpeas', 'calories': 200, 'protein': 12, 'carbs': 30, 'fat': 4},
                {'name': 'Grilled turkey breast', 'calories': 250, 'protein': 30, 'carbs': 0, 'fat': 8},
                {'name': 'Sweet potato cubes', 'calories': 180, 'protein': 2, 'carbs': 40, 'fat': 1},
                {'name': 'Olive oil dressing', 'calories': 120, 'protein': 0, 'carbs': 2, 'fat': 14},
            ]
        }
    ]

    dinner_options = [
        {
            'name': 'Lean & Green',
            'items': [
                {'name': 'Baked cod with herbs', 'calories': 300, 'protein': 35, 'carbs': 2, 'fat': 8},
                {'name': 'Roasted Brussels sprouts', 'calories': 120, 'protein': 4, 'carbs': 20, 'fat': 4},
                {'name': 'Wild rice pilaf', 'calories': 200, 'protein': 6, 'carbs': 40, 'fat': 2},
                {'name': 'Side salad', 'calories': 80, 'protein': 2, 'carbs': 12, 'fat': 3},
            ]
        },
        {
            'name': 'Comfort Classic',
            'items': [
                {'name': 'Lean beef stir-fry', 'calories': 320, 'protein': 28, 'carbs': 15, 'fat': 16},
                {'name': 'Steamed broccoli', 'calories': 60, 'protein': 4, 'carbs': 12, 'fat': 1},
                {'name': 'Quinoa', 'calories': 180, 'protein': 6, 'carbs': 32, 'fat': 3},
                {'name': 'Green tea', 'calories': 5, 'protein': 0, 'carbs': 1, 'fat': 0},
            ]
        },
        {
            'name': 'Plant Power',
            'items': [
                {'name': 'Lentil and vegetable curry', 'calories': 280, 'protein': 18, 'carbs': 45, 'fat': 6},
                {'name': 'Brown rice', 'calories': 180, 'protein': 4, 'carbs': 36, 'fat': 2},
                {'name': 'Naan bread (small)', 'calories': 150, 'protein': 5, 'carbs': 28, 'fat': 3},
                {'name': 'Cucumber raita', 'calories': 80, 'protein': 4, 'carbs': 8, 'fat': 4},
            ]
        }
    ]

    snack_options = [
        {
            'name': 'Energy Boost',
            'items': [
                {'name': 'Apple with almond butter', 'calories': 190, 'protein': 4, 'carbs': 25, 'fat': 8},
                {'name': 'Green tea', 'calories': 5, 'protein': 0, 'carbs': 1, 'fat': 0},
            ]
        },
        {
            'name': 'Protein Pack',
            'items': [
                {'name': 'Greek yogurt parfait', 'calories': 180, 'protein': 15, 'carbs': 20, 'fat': 6},
                {'name': 'Mixed berries', 'calories': 60, 'protein': 1, 'carbs': 15, 'fat': 0},
            ]
        },
        {
            'name': 'Healthy Crunch',
            'items': [
                {'name': 'Hummus with vegetables', 'calories': 120, 'protein': 6, 'carbs': 15, 'fat': 5},
                {'name': 'Whole grain crackers', 'calories': 80, 'protein': 2, 'carbs': 16, 'fat': 2},
            ]
        }
    ]

    # Select random options for the day
    selected_breakfast = random.choice(breakfast_options)
    selected_lunch = random.choice(lunch_options)
    selected_dinner = random.choice(dinner_options)
    selected_snacks = random.choice(snack_options)

    # Calculate totals
    def calculate_meal_totals(meal):
        return {
            'calories': sum(item['calories'] for item in meal['items']),
            'protein': sum(item['protein'] for item in meal['items']),
            'carbs': sum(item['carbs'] for item in meal['items']),
            'fat': sum(item['fat'] for item in meal['items'])
        }

    breakfast_totals = calculate_meal_totals(selected_breakfast)
    lunch_totals = calculate_meal_totals(selected_lunch)
    dinner_totals = calculate_meal_totals(selected_dinner)
    snacks_totals = calculate_meal_totals(selected_snacks)

    daily_totals = {
        'calories': breakfast_totals['calories'] + lunch_totals['calories'] + dinner_totals['calories'] + snacks_totals['calories'],
        'protein': breakfast_totals['protein'] + lunch_totals['protein'] + dinner_totals['protein'] + snacks_totals['protein'],
        'carbs': breakfast_totals['carbs'] + lunch_totals['carbs'] + dinner_totals['carbs'] + snacks_totals['carbs'],
        'fat': breakfast_totals['fat'] + lunch_totals['fat'] + dinner_totals['fat'] + snacks_totals['fat']
    }

    return {
        'breakfast': {**selected_breakfast, 'totals': breakfast_totals},
        'lunch': {**selected_lunch, 'totals': lunch_totals},
        'dinner': {**selected_dinner, 'totals': dinner_totals},
        'snacks': {**selected_snacks, 'totals': snacks_totals},
        'daily_totals': daily_totals
    }


@login_required
def dashboard_home(request):
    """Main dashboard view"""
    today = date.today()

    # Get user profile
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    # Get today's meals
    today_meals = MealEntry.objects.filter(
        user=request.user,
        date__date=today
    )

    # Calculate today's totals
    total_calories = sum(meal.get_total_calories() for meal in today_meals)
    total_protein = sum(meal.get_total_protein() for meal in today_meals)
    total_carbs = sum(meal.get_total_carbs() for meal in today_meals)
    total_fat = sum(meal.get_total_fat() for meal in today_meals)

    # Get goals from user profile
    calorie_goal = user_profile.daily_calorie_goal if user_profile else 2000
    protein_goal = user_profile.daily_protein_goal if user_profile else 150
    carbs_goal = user_profile.daily_carbs_goal if user_profile else 250
    fat_goal = user_profile.daily_fat_goal if user_profile else 65

    # Calculate percentages
    calorie_percentage = min((total_calories / calorie_goal) * 100, 100) if calorie_goal > 0 else 0
    protein_percentage = min((total_protein / protein_goal) * 100, 100) if protein_goal > 0 else 0
    carbs_percentage = min((total_carbs / carbs_goal) * 100, 100) if carbs_goal > 0 else 0
    fat_percentage = min((total_fat / fat_goal) * 100, 100) if fat_goal > 0 else 0

    # Get water intake for today (automatic daily reset)
    today_water = WaterIntake.objects.filter(
        user=request.user,
        date__date=today
    )
    total_water = sum(water.amount_ml for water in today_water)
    water_goal = user_profile.daily_water_goal if user_profile else 2000
    water_percentage = min((total_water / water_goal) * 100, 100) if water_goal > 0 else 0

    # Count of water entries today
    water_entries_count = today_water.count()

    # Get recent workouts
    recent_workouts = WorkoutLog.objects.filter(user=request.user).order_by('-date')[:5]

    # Generate daily meal plan
    daily_meal_plan = generate_daily_meal_plan(user_profile, today)

    # Pass all meal options to template for editing functionality
    all_meal_options = {
        'breakfast': [
            {
                'name': 'Oatmeal Power Bowl',
                'items': [
                    {'name': 'Steel-cut oats with blueberries', 'calories': 320, 'protein': 12, 'carbs': 58, 'fat': 6},
                    {'name': 'Greek yogurt with honey', 'calories': 150, 'protein': 15, 'carbs': 20, 'fat': 3},
                    {'name': 'Almonds (handful)', 'calories': 160, 'protein': 6, 'carbs': 6, 'fat': 14},
                ]
            },
            {
                'name': 'Protein Breakfast',
                'items': [
                    {'name': 'Scrambled eggs (2 large)', 'calories': 180, 'protein': 12, 'carbs': 2, 'fat': 14},
                    {'name': 'Whole grain toast', 'calories': 120, 'protein': 4, 'carbs': 22, 'fat': 2},
                    {'name': 'Avocado (half)', 'calories': 160, 'protein': 2, 'carbs': 9, 'fat': 15},
                    {'name': 'Orange juice (small)', 'calories': 80, 'protein': 1, 'carbs': 20, 'fat': 0},
                ]
            },
            {
                'name': 'Smoothie Bowl',
                'items': [
                    {'name': 'Banana protein smoothie', 'calories': 280, 'protein': 25, 'carbs': 35, 'fat': 8},
                    {'name': 'Granola topping', 'calories': 150, 'protein': 4, 'carbs': 25, 'fat': 6},
                    {'name': 'Fresh berries', 'calories': 60, 'protein': 1, 'carbs': 15, 'fat': 0},
                ]
            }
        ],
        'lunch': [
            {
                'name': 'Mediterranean Bowl',
                'items': [
                    {'name': 'Grilled chicken breast', 'calories': 350, 'protein': 35, 'carbs': 0, 'fat': 8},
                    {'name': 'Quinoa salad with vegetables', 'calories': 280, 'protein': 10, 'carbs': 45, 'fat': 8},
                    {'name': 'Hummus with pita', 'calories': 180, 'protein': 8, 'carbs': 20, 'fat': 8},
                    {'name': 'Mixed greens', 'calories': 40, 'protein': 2, 'carbs': 8, 'fat': 0},
                ]
            },
            {
                'name': 'Asian Fusion',
                'items': [
                    {'name': 'Teriyaki salmon', 'calories': 320, 'protein': 28, 'carbs': 12, 'fat': 18},
                    {'name': 'Brown rice', 'calories': 220, 'protein': 5, 'carbs': 45, 'fat': 2},
                    {'name': 'Steamed vegetables', 'calories': 80, 'protein': 3, 'carbs': 16, 'fat': 1},
                    {'name': 'Miso soup', 'calories': 60, 'protein': 4, 'carbs': 8, 'fat': 2},
                ]
            },
            {
                'name': 'Power Salad',
                'items': [
                    {'name': 'Mixed greens with chickpeas', 'calories': 200, 'protein': 12, 'carbs': 30, 'fat': 4},
                    {'name': 'Grilled turkey breast', 'calories': 250, 'protein': 30, 'carbs': 0, 'fat': 8},
                    {'name': 'Sweet potato cubes', 'calories': 180, 'protein': 2, 'carbs': 40, 'fat': 1},
                    {'name': 'Olive oil dressing', 'calories': 120, 'protein': 0, 'carbs': 2, 'fat': 14},
                ]
            }
        ],
        'dinner': [
            {
                'name': 'Lean & Green',
                'items': [
                    {'name': 'Baked cod with herbs', 'calories': 300, 'protein': 35, 'carbs': 2, 'fat': 8},
                    {'name': 'Roasted Brussels sprouts', 'calories': 120, 'protein': 4, 'carbs': 20, 'fat': 4},
                    {'name': 'Wild rice pilaf', 'calories': 200, 'protein': 6, 'carbs': 40, 'fat': 2},
                    {'name': 'Side salad', 'calories': 80, 'protein': 2, 'carbs': 12, 'fat': 3},
                ]
            },
            {
                'name': 'Comfort Classic',
                'items': [
                    {'name': 'Lean beef stir-fry', 'calories': 320, 'protein': 28, 'carbs': 15, 'fat': 16},
                    {'name': 'Steamed broccoli', 'calories': 60, 'protein': 4, 'carbs': 12, 'fat': 1},
                    {'name': 'Quinoa', 'calories': 180, 'protein': 6, 'carbs': 32, 'fat': 3},
                    {'name': 'Green tea', 'calories': 5, 'protein': 0, 'carbs': 1, 'fat': 0},
                ]
            },
            {
                'name': 'Plant Power',
                'items': [
                    {'name': 'Lentil and vegetable curry', 'calories': 280, 'protein': 18, 'carbs': 45, 'fat': 6},
                    {'name': 'Brown rice', 'calories': 180, 'protein': 4, 'carbs': 36, 'fat': 2},
                    {'name': 'Naan bread (small)', 'calories': 150, 'protein': 5, 'carbs': 28, 'fat': 3},
                    {'name': 'Cucumber raita', 'calories': 80, 'protein': 4, 'carbs': 8, 'fat': 4},
                ]
            }
        ],
        'snacks': [
            {
                'name': 'Energy Boost',
                'items': [
                    {'name': 'Apple with almond butter', 'calories': 190, 'protein': 4, 'carbs': 25, 'fat': 8},
                    {'name': 'Green tea', 'calories': 5, 'protein': 0, 'carbs': 1, 'fat': 0},
                ]
            },
            {
                'name': 'Protein Pack',
                'items': [
                    {'name': 'Greek yogurt parfait', 'calories': 180, 'protein': 15, 'carbs': 20, 'fat': 6},
                    {'name': 'Mixed berries', 'calories': 60, 'protein': 1, 'carbs': 15, 'fat': 0},
                ]
            },
            {
                'name': 'Healthy Crunch',
                'items': [
                    {'name': 'Hummus with vegetables', 'calories': 120, 'protein': 6, 'carbs': 15, 'fat': 5},
                    {'name': 'Whole grain crackers', 'calories': 80, 'protein': 2, 'carbs': 16, 'fat': 2},
                ]
            }
        ]
    }

    context = {
        'user_profile': user_profile,
        'today_meals': today_meals,
        'total_calories': total_calories,
        'total_protein': total_protein,
        'total_carbs': total_carbs,
        'total_fat': total_fat,
        'calorie_goal': calorie_goal,
        'protein_goal': protein_goal,
        'carbs_goal': carbs_goal,
        'fat_goal': fat_goal,
        'calorie_percentage': calorie_percentage,
        'protein_percentage': protein_percentage,
        'carbs_percentage': carbs_percentage,
        'fat_percentage': fat_percentage,
        'total_water': total_water,
        'water_goal': water_goal,
        'water_percentage': water_percentage,
        'water_entries_count': water_entries_count,
        'recent_workouts': recent_workouts,
        'today': today,
        'daily_meal_plan': daily_meal_plan,
        'all_meal_options': all_meal_options,
    }

    return render(request, 'dashboard/home.html', context)
