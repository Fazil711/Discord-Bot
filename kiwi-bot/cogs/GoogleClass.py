from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import discord 
from discord.ext import commands
from discord.ext.commands.core import has_permissions
import json

SCOPES = ['https://www.googleapis.com/auth/classroom.courses', 'https://www.googleapis.com/auth/classroom.coursework.students']

creds = None
if os.path.exists('token.json'):
  creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if not creds or not creds.valid:
  if creds and creds.expired and creds.refresh_token:
    creds.refresh(Request())
  else:
    flow = InstalledAppFlow.from_client_secrets_file('cogs/credentials.json', SCOPES)
    creds = flow.run_local_server(port = 0)
  with open('token.json', 'w') as token:
      token.write(creds.to_json())
service = build('classroom', 'v1', credentials=creds)

class Goclass(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def listCourses(self, ctx):
    try:
      results = service.courses().list(pageSize=10).execute()
      courses = results.get('courses', [])

      if not courses:
          await ctx.send('No courses found')
          return
      for course in courses:
          embed = discord.Embed(
              title=course['name'],
              colour=0x2859B8,
              description = "Course Link: %s \nCourse ID: %s \nEnrollment Code: %s" % (course.get('alternateLink'), course.get('id'), course.get('enrollmentCode'))
          )
          await ctx.send(embed = embed)

    except HttpError as error:
      await ctx.send('An error occured: %s' % error)

  @commands.command()
  @has_permissions(administrator = True)
  async def addCourse(self, ctx, * , arg):
    course = {
        'name': '{}'.format(arg),
        'section': 'Period 2',
        'descriptionHeading': 'Welcome to {}'.format(arg),
        'description': """Just created""",
        'room': '301',
        'ownerId': 'me',
        'courseState': 'PROVISIONED'
    }
    course = service.courses().create(body=course).execute()
    embed = discord.Embed(
              title="Course Created Successfully!",
              colour=0x2859B8,
              description = 'Course created: %s %s \nLink: %s \nEnrollment Code: %s' % (course.get('name'), course.get('id'), course.get('alternateLink'), course.get('enrollmentCode'))
          )
    await ctx.send(embed = embed)
  @addCourse.error
  async def course_error(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
              title="Lol",
              colour=0x2859B8,
              description="You don't even have perms for that!",
        )
        await ctx.send(embed = embed)


  @commands.command()
  @has_permissions(administrator = True)
  async def CreateCourseWork(self, ctx, course_id, title):
    coursework = {
      'title': '{}'.format(title),
      'description': '''Made directly from discord''',
      'workType': 'ASSIGNMENT',
      'state': 'PUBLISHED',
    }
    coursework = service.courses().courseWork().create(courseId=course_id, body=coursework).execute()
    embed = discord.Embed(
              title="Assignment created Successfully!",
              colour=0x2859B8,
              description = 'Assignment created: %s \nLink: %s' % (coursework.get('id'), coursework.get('alternateLink'))
          )
    await ctx.send(embed = embed)
  @CreateCourseWork.error
  async def Creation_error(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
              title="Lol",
              colour=0x2859B8,
              description="You don't even have perms for that!",
        )
        await ctx.send(embed = embed)

  @commands.command()
  @has_permissions(administrator = True)
  async def CreateCourseWorkLink(self, ctx, course_id, title, *, args):
    coursework = {
      'title': '{}'.format(title),
      'description': '''Made directly from discord''',
      'materials': [
          {'link': {'url': '{}'.format(args)}}
      ],
      'workType': 'ASSIGNMENT',
      'state': 'PUBLISHED',
    }
    coursework = service.courses().courseWork().create(courseId=course_id, body=coursework).execute()
    embed = discord.Embed(
              title="Assignment created Successfully!",
              colour=0x2859B8,
              description = 'Assignment created: %s \nLink: %s' % (coursework.get('id'), coursework.get('alternateLink'))
          )
    await ctx.send(embed = embed)
  @CreateCourseWorkLink.error
  async def Creation_error(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
              title="Lol",
              colour=0x2859B8,
              description="You don't even have perms for that!",
        )
        await ctx.send(embed = embed)

  @commands.command()
  @has_permissions(administrator = True)
  async def listCourseWork(self, ctx, course_id, coursework_id):
    submissions = []
    page_token = None

    while True:
        coursework = service.courses().courseWork()
        response = coursework.studentSubmissions().list(
            pageToken=page_token,
            courseId=course_id,
            courseWorkId=coursework_id,
            pageSize=10).execute()
        submissions.extend(response.get('studentSubmissions', []))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break

    if not submissions:
        await ctx.send('No student submissions found.')
    else:
        for submission in submissions:
            embed = discord.Embed(
                title="Submission By: {}".format(submission.get('userId')),
                colour=0x2859B8,
                description = 'Submission creationTime: %s' % (submission.get('creationTime'))
            )
            await ctx.send(embed = embed)
  @listCourseWork.error
  async def submission_error(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
              title="Lol",
              colour=0x2859B8,
              description="You don't even have perms for that!",
        )
        await ctx.send(embed = embed)



def setup(bot):
  bot.add_cog(Goclass(bot))
