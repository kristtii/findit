from flask import Flask, render_template, request, session, redirect
from flask_app.models.user import User

app = Flask(__name__)

app.secret_key = "3dcars"