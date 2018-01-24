__author__ = 'rudolf_han'
from flask import Flask, request, render_template
from . import job_value
from .. import scheduler
__author__ = 'rudolf_han'

# def jobfromparm(**jobargs):
#     # scheduler = APScheduler()
#     id = jobargs['id']
#     func = 'APP:job1'
#     args = eval(jobargs['args'])
#     trigger = jobargs['trigger']
#     seconds = jobargs['seconds']
#     job = scheduler.add_job(func=func, id=id, args=args, trigger=trigger, seconds=seconds, replace_existing=True)
#     print(job)
#     return 'sucess'
@job_value.route('/', methods=['GET', 'POST'])
def index():
    return 'test hoello '
@job_value.route('/pause')
def pausejob():
    scheduler.pause_job('job2')
    return "Success!"
@job_value.route('/resume')
def resumejob():
    scheduler.resume_job('job1')
    return "Success!"

@job_value.route('/addjob', methods=['GET', 'POST'])
def addjob():
    #id = jobargs['id']
    id = 'run_id'
    func = 'APP:run_case'
    args = (a,b,c)
    trigger = 'cron'
    day_of_week = 0
    hour = 0
    minute= 0
    seconds = 0
    job = scheduler.add_job(func=func, id=id, args=args, trigger=trigger, seconds=seconds, replace_existing=True)


    #
    # data = request.get_json(force=True)
    # job = jobfromparm(**data)
    return job



