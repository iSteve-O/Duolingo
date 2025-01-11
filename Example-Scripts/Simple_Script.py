import duolingo

# This block gets the info from the owl.
lingo  = duolingo.Duolingo('username', jwt='YOUR_JWT_TOKEN_FROM_BROWSER')
streak_info = lingo.get_streak_info()
site_streak = streak_info.get('site_streak', 0)
streak_extended_today = streak_info.get('streak_extended_today', False)

# This block prints the info nicely in the CLI.
print(f"Site Streak: {site_streak}")
print(f"Streak Extended Today: {streak_extended_today}")
