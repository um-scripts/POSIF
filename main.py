import json
import os.path

import pandas as pd
from zipfile import ZipFile
import random
import string
import os
import shutil
from datetime import datetime, timedelta

from celery import Celery
from celery.schedules import crontab
from flask import Flask, request, jsonify, abort
from flask import make_response, send_from_directory

from Iforest import detectSRNA, annotate

app = Flask(__name__)
celery = Celery(app.name, backend='redis://localhost:6379', broker='redis://localhost:6379')
celery.conf.update(app.config)
ALPHA_NUMERIC = string.ascii_uppercase + string.ascii_lowercase + string.digits
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


@app.route('/')
def index():
    return make_response(send_from_directory('templates', 'index.html'))


@app.route('/example')
def example():
    return send_from_directory('files', 'Exampleinput.zip', as_attachment=True, download_name='ExampleInput.zip')


@app.route('/data', methods=['POST'])
def data():
    params = request.form.to_dict()
    if 'cf' not in params or 'organism' not in params or \
            'strand_type' not in params or 'out_name' not in params:
        return '', 400

    files = request.files.to_dict()
    if params['strand_type'] == 'non_strand_spec' and 'perbase' not in files.keys():
        return '', 400
    if params['strand_type'] == 'strand_spec' and \
            ('fwd_perbase' not in files.keys() or 'rev_perbase' not in files.keys()):
        return '', 400

    request_id = ''
    exists = True
    while exists:
        request_id = ''.join(random.choice(ALPHA_NUMERIC) for _ in range(30))
        exists = os.path.exists(os.path.join('files/requests', request_id))

    os.mkdir(os.path.join('files/requests', request_id))
    for n, file in files.items():
        file.save(os.path.join('files/requests', request_id, '{0}.bed'.format(n)))

    task_id = run_main.apply_async(args=[request_id, params])
    return jsonify({'id': request_id, 'task_id': task_id.id}), 200


@app.route('/status', methods=['POST'])
def status():
    args = json.loads(request.data)
    if 'id' not in args or 'task_id' not in args:
        return '', 400
    task = celery.AsyncResult(args['task_id'])
    if task.state == 'IN_PROGRESS':
        return jsonify({'state': 'IN_PROGRESS', 'progress': task.info.get('progress')}), 200
    elif task.state == 'SUCCESS':
        return jsonify({'state': 'SUCCESS', 'id': args["id"]}), 200
    else:
        return jsonify({'state': task.state}), 200


@app.route('/download')
def download():
    request_id = request.args['id']
    target_path = os.path.join('files/results', request_id, 'POSIF_results_{0}.zip'.format(request_id))
    if not os.path.exists(target_path):
        return abort(404)

    return send_from_directory(
        'files/results/{0}'.format(request_id), 'POSIF_results_{0}.zip'.format(request_id),
        as_attachment=True,
        download_name='POSIF_results_{0}.zip'.format(request_id))


@celery.task(bind=True, name='main')
def run_main(self, request_id, params):

    self.update_state(self.request.id, state='IN_PROGRESS', meta={'progress': 'Initializing'})
    anno_file = os.path.join('annotations', '{0}.gff'.format(params["organism"]))
    annotation_data = pd.read_csv(anno_file, sep='\t', comment='#', usecols=[2, 3, 4, 6, 8],
                                  names=['type', 'start', 'end', 'strand', 'gene_id'])
    gene_annotations = annotation_data[annotation_data['type'] == 'gene'].copy()
    del annotation_data

    if params['strand_type'] == 'strand_spec':
        fwd_data = pd.read_csv(
            os.path.join('files/requests', request_id, 'fwd_perbase.bed'),
            sep='\t', names=['position', 'readcount'], usecols=[1, 2])
        rev_data = pd.read_csv(
            os.path.join('files/requests', request_id, 'rev_perbase.bed'),
            sep='\t', names=['position', 'readcount'], usecols=[1, 2])
        self.update_state(self.request.id, state='IN_PROGRESS', meta={'progress': 'Processing Forward Perbase File'})
        fwd_regions = detectSRNA(fwd_data, float(params['cf']))
        self.update_state(self.request.id, state='IN_PROGRESS', meta={'progress': 'Processing Reverse Perbase File'})
        rev_regions = detectSRNA(rev_data, float(params['cf']))
        self.update_state(self.request.id, state='IN_PROGRESS', meta={'progress': 'Annotating the Predictions'})
        fwd_output = annotate(fwd_regions, gene_annotations, '+')
        rev_output = annotate(rev_regions, gene_annotations, '-')

        self.update_state(self.request.id, state='IN_PROGRESS', meta={'progress': 'Preparing files for Download'})
        out_path = os.path.join('files/results', request_id)
        os.mkdir(out_path)
        fwd_output.to_csv(os.path.join(out_path, 'sRNA_fwd_output.csv'), index=False)
        rev_output.to_csv(os.path.join(out_path, 'sRNA_rev_output.csv'), index=False)

        with ZipFile(os.path.join(out_path, 'POSIF_results_{0}.zip'.format(request_id)), 'w') as zip_object:
            zip_object.write(os.path.join(out_path, 'sRNA_fwd_output.csv'),
                             arcname='{0}_forward.csv'.format(params["out_name"]))
            zip_object.write(os.path.join(out_path, 'sRNA_rev_output.csv'),
                             arcname='{0}_reverse.csv'.format(params["out_name"]))

        os.remove(os.path.join(out_path, 'sRNA_fwd_output.csv'))
        os.remove(os.path.join(out_path, 'sRNA_rev_output.csv'))

    else:
        perbase_data = pd.read_csv(
            os.path.join('files/requests', request_id, 'perbase.bed'),
            sep='\t', names=['position', 'readcount'], usecols=[1, 2])

        self.update_state(self.request.id, state='IN_PROGRESS', meta={'progress': 'Processing Perbase file'})
        regions = detectSRNA(perbase_data, float(params['cf']))

        self.update_state(self.request.id, state='IN_PROGRESS', meta={'progress': 'Annotating the Predictions'})
        output = annotate(regions, gene_annotations)

        out_path = os.path.join('files/results', request_id)
        os.mkdir(out_path)
        output.to_csv(os.path.join(out_path, 'sRNA_output.csv'), index=False)

        with ZipFile(os.path.join(out_path, 'POSIF_results_{0}.zip'.format(request_id)), 'w') as zip_object:
            zip_object.write(os.path.join(out_path, 'sRNA_output.csv'), arcname='{0}.csv'.format(params["out_name"]))

        os.remove(os.path.join(out_path, 'sRNA_output.csv'))


@celery.task(name='clean_up')
def clean_up():
    folders_to_remove = []
    for root_folder in ['files/requests', 'files/results']:
        for ids in os.listdir(root_folder):
            folder = os.path.join(root_folder, ids)
            dt = datetime.now() - datetime.fromtimestamp(os.path.getmtime(folder))
            if dt > timedelta(hours=24):
                folders_to_remove.append(folder)
    for f in folders_to_remove:
        shutil.rmtree(f)


# =============================================================================================
celery.conf.beat_schedule = {
    'delete_older_files': {
        'task': 'clean_up',
        'schedule': crontab(minute=0)
    }
}
celery.conf.timezone = 'UTC'
# =============================================================================================


