from flask_restful import Resource
from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for


class Basic(Resource):

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('home.html'),200,headers)



    def post(self):
        pass