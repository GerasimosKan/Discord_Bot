import discord
from discord.ext import commands
from flask import Flask, render_template
import threading
import os

class Dashboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # Define the path for the dashboard folder
        dashboard_folder = os.path.join(os.path.dirname(__file__), '..', 'dashboard')

        self.flask_app = Flask(__name__,
                            template_folder=os.path.join(dashboard_folder, 'templates'),
                            static_folder=os.path.join(dashboard_folder, 'static'))

        @self.flask_app.route('/')
        def home():
            return render_template('index.html', bot_name=self.bot.user.name)

        self.start_flask_server()

    def start_flask_server(self):
        """Runs the Flask web server in a separate thread."""
        def run_flask():
            self.flask_app.run(host='0.0.0.0', port=25560, debug=False, use_reloader=False)

        flask_thread = threading.Thread(target=run_flask)
        flask_thread.daemon = True
        flask_thread.start()

async def setup(bot):
    await bot.add_cog(Dashboard(bot))